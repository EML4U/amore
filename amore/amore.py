import os
import sys
from operator import methodcaller
from gensim.utils import simple_preprocess
from access.file_storage import FileStorage
from amore.amazon_reviews_reader import AmazonReviewsReader
from amore.opinion_lexicon import OpinionLexicon
from amore.review import Review

class Amore:
    
    def __init__(self, max_lines=-1, min_year=2001, max_year=2010):
        
        # Configuration
        self.verbose   = True
        self.max_lines = max_lines
        self.min_year  = min_year
        self.max_year  = max_year
        
        # Internal
        self.stars = [1, 5]
        self.years = range(self.min_year, self.max_year+1)
        self.file_storage = FileStorage()
        self.opinion_lexicon = None
        self.counter = {}

    def check_files(self):
        self.check_file(self.file_storage.get_filepath('amazon_gz_file'))
        self.check_file(self.file_storage.get_filepath('opinion-words'))
        return self
    
    def check_file(self, file):
        if not os.path.isfile(file):
            print('File not found:', file)
            sys.exit(1)
            
    def extract_opinion_words(self, text, positive=True, min_len=3, max_len=24):
        token_set = set(simple_preprocess(text, min_len=min_len, max_len=max_len))
        if(positive):
            return self.opinion_lexicon.extract_positive_words(token_set)
        else:
            return self.opinion_lexicon.extract_negative_words(token_set)
    
    def select_data(self):
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
        
        for year in self.years:
            self.counter[year] = {}
            for star in self.stars:
                self.counter[year][star] = []
                
        for review in reviews:
            year = review[AmazonReviewsReader.KEY_TIME].year
            if year not in self.years:
                continue
                
            star = review[AmazonReviewsReader.KEY_SCORE] - 1
            if star not in self.stars:
                continue
                
            text = review[AmazonReviewsReader.KEY_SUMMARY] + ' ' + review[AmazonReviewsReader.KEY_TEXT]
                        
            self.counter[year][star].append(Review(
                review[AmazonReviewsReader.KEY_NUMBER],
                len(self.extract_opinion_words(text, positive=True)),
                len(self.extract_opinion_words(text, positive=False))))
            
        return self
    
    def get_counter_overview(self):
        result = {}
        for year in self.counter.keys():
            result[year] = {}
            for star in self.counter[year].keys():
                result[year][star] = len(self.counter[year][star])
        return result
    
    def get_positive_sorted(self, year, star):
        return sorted(self.counter[year][star], key=methodcaller('get_positive_sort_value'))
    
    def get_negative_sorted(self, year, star):
        return sorted(self.counter[year][star], key=methodcaller('get_negative_sort_value'))