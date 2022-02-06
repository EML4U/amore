import errno
import os
import sys
from operator import methodcaller
from gensim.utils import simple_preprocess
from access.file_storage import FileStorage
from access.interim_storage import InterimStorage
from amore.amazon_reviews_reader import AmazonReviewsReader
from amore.opinion_lexicon import OpinionLexicon
from amore.review import Review

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
        self.counter = {}

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
        
        if self.verbose:
            print('Reading data')
            print('max_lines:', self.max_lines)
            print('min_year:', self.min_year)
            print('max_year:', self.max_year)
            
        reviews = AmazonReviewsReader(self.file_storage.get_filepath('amazon_gz_file'),
                                      AmazonReviewsReader.MODE_TYPED,
                                      max_docs=self.max_lines,
                                      min_year=self.min_year,
                                      max_year=self.max_year)
        
        self.opinion_lexicon = OpinionLexicon(self.file_storage.get_filepath('opinion-words'))
        opinion_max_pos = self.opinion_lexicon.get_extremum_length(maximum=True, positive=True)
        opinion_max_neg = self.opinion_lexicon.get_extremum_length(maximum=True, positive=False)
        
        for year in self.years:
            self.counter[year] = {}
            for star in self.stars:
                self.counter[year][star] = []
        
        r = 0
        for review in reviews:
            r += 1
            year = review[AmazonReviewsReader.KEY_TIME].year
            if year not in self.years:
                continue
                
            star = review[AmazonReviewsReader.KEY_SCORE] - 1
            if star not in self.stars:
                continue
                
            text = review[AmazonReviewsReader.KEY_SUMMARY] + ' ' + review[AmazonReviewsReader.KEY_TEXT]
                        
            self.counter[year][star].append(Review(
                review[AmazonReviewsReader.KEY_NUMBER],
                len(self.extract_opinion_words(text, positive=True, min_len=3, max_len=opinion_max_pos)),
                len(self.extract_opinion_words(text, positive=False, min_len=3, max_len=opinion_max_neg))))
            
            if(self.verbose and r % 100000 == 0): # TODO seems not to work
                print(r, end=' ')
        if(self.verbose):
            print()
        
        if write_file_id is not None:
            interim_storage = InterimStorage(write_file_id)
            if self.verbose:
                print('Writing:', interim_storage.get_filepath())
            interim_storage.write(self.counter)
        
        return self
    
    def get_positive_sorted(self, year, star):
        return sorted(self.counter[year][star], key=methodcaller('get_positive_sort_value'))
    
    def get_negative_sorted(self, year, star):
        return sorted(self.counter[year][star], key=methodcaller('get_negative_sort_value'))