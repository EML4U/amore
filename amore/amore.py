import errno
import os
import sys
import timeit
from operator import methodcaller
from gensim.utils import simple_preprocess
from access.file_storage import FileStorage
from access.interim_storage import InterimStorage
from amore.amazon_reviews_reader import AmazonReviewsReader
from amore.opinion_lexicon import OpinionLexicon
from amore.reviews import Reviews
from amore.review import Review
from amore.split import Split

class Amore:
    
    def __init__(self, max_lines=-1, min_year=2001, max_year=2010, stars=[1,5], verbose=True):
        
        # Configuration
        self.max_lines = max_lines
        self.min_year  = min_year
        self.max_year  = max_year
        self.stars     = stars
        self.verbose   = verbose
        
        # Internal
        self.years = range(self.min_year, self.max_year+1)
        self.file_storage = FileStorage()
        self.opinion_lexicon = None
        self.reviews = None
        self.counter = None

    def get_missing_files(self, raise_error=False):
        missing_files = []
        missing_files += self.check_file(self.file_storage.get_filepath('amazon_gz_file'))
        missing_files += self.check_file(self.file_storage.get_filepath('opinion-words'))
        if(raise_error and len(missing_files) > 0):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), missing_files)
        return missing_files
    
    def check_file(self, file):
        if os.path.isfile(file):
            return []
        else:
            return [file]
            
    def extract_opinion_words(self, text, positive=True, min_len=3, max_len=24):
        token_set = set(simple_preprocess(text, min_len=min_len, max_len=max_len))
        if(positive):
            return self.opinion_lexicon.extract_positive_words(token_set)
        else:
            return self.opinion_lexicon.extract_negative_words(token_set)
    
    def select_data(self, write_file_id=None):
        self.get_missing_files(raise_error=True)
        time_begin = timeit.default_timer()
        
        if self.verbose:
            print('Reading data')
            print('max_lines:', self.max_lines)
            print('min_year:', self.min_year)
            print('max_year:', self.max_year)
            
        reviews_reader = AmazonReviewsReader(self.file_storage.get_filepath('amazon_gz_file'),
                                             AmazonReviewsReader.MODE_TYPED,
                                             max_docs=self.max_lines,
                                             min_year=self.min_year,
                                             max_year=self.max_year)
        
        self.opinion_lexicon = OpinionLexicon(self.file_storage.get_filepath('opinion-words'))
        opinion_max_pos = self.opinion_lexicon.get_extremum_length(maximum=True, positive=True)
        opinion_max_neg = self.opinion_lexicon.get_extremum_length(maximum=True, positive=False)
        
        self.reviews = Reviews()
        r = 0
        for review in reviews_reader:
            r += 1
            if(self.verbose and r == 1000):
                print(r, end=' ... ')
            if(self.verbose and r % 100000 == 0):
                print(r, end=' ')
            
            year = review[AmazonReviewsReader.KEY_TIME].year
            if year not in self.years:
                continue
                
            star = review[AmazonReviewsReader.KEY_SCORE]
            if star not in self.stars:
                continue
                
            text = review[AmazonReviewsReader.KEY_SUMMARY] + ' ' + review[AmazonReviewsReader.KEY_TEXT]
            
            self.reviews.add_review(year, star,
                               Review(review[AmazonReviewsReader.KEY_NUMBER],
                                      len(self.extract_opinion_words(text, positive=True, min_len=3, max_len=opinion_max_pos)),
                                      len(self.extract_opinion_words(text, positive=False, min_len=3, max_len=opinion_max_neg))
            ))
        if(self.verbose):
            print()
        
        if(write_file_id is not None):
            self.reviews.write_review_objects(file_id=write_file_id, verbose=self.verbose)
            
        if(self.verbose):
            print('Size:', self.reviews.get_size())
            print('Runtime:', timeit.default_timer() - time_begin)
    
    def sort(self, load_file_id=None, write_file_id=None):
        time_begin = timeit.default_timer()

        if(load_file_id is not None):
            self.reviews.read_review_objects(file_id=load_file_id, verbose=self.verbose)
            
        self.counter = {}
        for year in self.reviews.get_years():
            self.counter[year] = {}
            for star in self.reviews.get_stars(year):
                if(star in [4,5]):
                    self.counter[year][star] = self.reviews.get_positive_sorted_tuple(year, star)
                elif(star in [1,2]):
                    self.counter[year][star] = self.reviews.get_negative_sorted_tuple(year, star)
                elif(self.verbose):
                    print('Skipping' + star)
                if(self.verbose):
                    print(year, star, len(self.counter[year][star]))

        if(write_file_id is not None):
            # Note: JSON does not work for loading+storing, as it converts integer keys to strings
            interim_storage = InterimStorage(id_=write_file_id, type_=InterimStorage.PICKLE_BZ2)
            interim_storage.write(self.counter)
            if self.verbose:
                print('Wrote:', interim_storage.get_filepath())
        
        if(self.verbose):
            print('Runtime:', timeit.default_timer() - time_begin)

    def split(self, splits, load_file_id=None):
        time_begin = timeit.default_timer()

        if(load_file_id is not None):
            interim_storage = InterimStorage(id_=load_file_id, type_=InterimStorage.PICKLE_BZ2)
            self.counter = interim_storage.read()
            if self.verbose:
                print('Read:', interim_storage.get_filepath())
                
        for year in self.counter.keys():
            for star in self.counter[year].keys():
                for tup in self.counter[year][star]:
                    for split in splits:
                        for i in split.count_down(year, star):
                            split.add(tup[0])
                    
        if(self.verbose):
            print('Runtime:', timeit.default_timer() - time_begin)
        
        return splits