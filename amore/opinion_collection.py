# Counts negarive and positive words of fields 'summary' and 'text'.
# Author: Adrian Wilke https://github.com/adibaba
#
# Results format: [(line-number, [(summary-negative-word, count)], [(summary-positive-word, count)], [(text-negative-word, count)], [(text-positive-word, count)])]
# e.g. (6, [('pointless', 1)], [('pretty', 1)], [('badly', 1), ('revenge', 1)], [('holy', 1), ('good', 1)])
# e.g. (64, [('loss', 1)], [], [('lost', 1), ('loss', 1), ('pain', 1)], [('helpful', 1), ('loved', 2), ('faith', 2), ('stronger', 1), ('love', 1), ('loving', 1)])
from amore.opinion_lexicon import OpinionLexicon
from amore.amazon_reviews_reader import AmazonReviewsReader
from access.file_storage import FileStorage
from access.interim_storage import InterimStorage
from gensim.utils import simple_preprocess
from collections import Counter

class OpinionCollection:
    
    FILE_ID        = 'AMORE-OpinionCollection'
    FILE_ID_COUNTS = 'AMORE-OpinionCounts'
    
    KEY_NUMBER = 0
    KEY_NEGATIVE_SUMMARY = 1
    KEY_POSITIVE_SUMMARY = 2
    KEY_NEGATIVE_TEXT = 3
    KEY_POSITIVE_TEXT = 4

    def __init__(self, filepath_opinion_lexicon=None):
        if filepath_opinion_lexicon is None:
            filepath_opinion_lexicon = FileStorage().get_filepath('opinion-words')
        self.opinion_lexicon = OpinionLexicon(filepath_opinion_lexicon)
        
        self.min_len = min(self.opinion_lexicon.get_extremum_length(maximum=False, positive=True),
                           self.opinion_lexicon.get_extremum_length(maximum=False, positive=False))
        self.max_len = max(self.opinion_lexicon.get_extremum_length(maximum=True,  positive=True),
                           self.opinion_lexicon.get_extremum_length(maximum=True,  positive=False))
        self.results = []
        self.dictionary = {}
        
    # Collects positive and negative words of summaries and texts
    def collect(self, amazon_movie_reviews_file=None, max_docs=-1, min_year=-1, max_year=-1):
        if amazon_movie_reviews_file is None:
            amazon_movie_reviews_file = FileStorage().get_filepath('amazon_gz_file')
        
        self.results = []
        for review in AmazonReviewsReader(amazon_movie_reviews_file,
                                          AmazonReviewsReader.MODE_TYPED,
                                          max_docs=max_docs,
                                          min_year=min_year,
                                          max_year=max_year):

            counter = Counter(simple_preprocess(review[AmazonReviewsReader.KEY_SUMMARY], min_len=self.min_len, max_len=self.max_len))
            sum_counts_neg = self.opinion_lexicon.extract_negative_counts(counter)
            sum_counts_pos = self.opinion_lexicon.extract_positive_counts(counter)

            counter = Counter(simple_preprocess(review[AmazonReviewsReader.KEY_TEXT], min_len=self.min_len, max_len=self.max_len))
            txt_counts_neg = self.opinion_lexicon.extract_negative_counts(counter)
            txt_counts_pos = self.opinion_lexicon.extract_positive_counts(counter)

            self.results.append((review[AmazonReviewsReader.KEY_NUMBER], sum_counts_neg, sum_counts_pos, txt_counts_neg, txt_counts_pos))
        return self
    
    def get_results(self):
        return self.results
    
    def write(self, file_id=None, directory=None, type_=InterimStorage.JSON_GZ):
        if file_id is None:
            file_id = self.FILE_ID
        return InterimStorage(file_id, directory=directory, type_=type_).write(self.results).get_filepath()
    
    def read(self, file_id=None, directory=None, type_=InterimStorage.JSON_GZ):
        if file_id is None:
            file_id = self.FILE_ID
        self.results = InterimStorage(id_=file_id, directory=directory, type_=type_).read()
        return self
    
    # To dictionary for access with get() method
    
    def create_dictionary(self, clear_results=True):
        if(len(self.results) > 0):
            self.dictionary = {}
            for item in self.results:
                self.dictionary[item[self.KEY_NUMBER]] = item
            if(clear_results):
                self.results = []
        return self
    
    def get(self, number):
        return self.dictionary[number]
    
    # Create pos minus neg
    
    def create_positive_minus_negative(self):
        self.pos_neg = {}
        if(len(self.results) > 0):
            for item in self.results:
                tup = self.create_positive_minus_negative_tuple(item)
                self.pos_neg[tup[0]] = (tup[1], tup[2])
        elif(len(self.dictionary) > 0):
            for item in self.dictionary.values():
                tup = self.create_positive_minus_negative_tuple(item)
                self.pos_neg[tup[0]] = (tup[1], tup[2])
        else:
            print('Error creating pos/neg: No data in results/dictionary')
        return self

    def create_positive_minus_negative_tuple(self, tup):
        return (tup[self.KEY_NUMBER],
                sum(c for w, c in tup[self.KEY_POSITIVE_SUMMARY]) +
                sum(c for w, c in tup[self.KEY_POSITIVE_TEXT]) -
                sum(c for w, c in tup[self.KEY_NEGATIVE_SUMMARY]) -
                sum(c for w, c in tup[self.KEY_NEGATIVE_TEXT]),
                
                len({k[0] for k in tup[self.KEY_POSITIVE_SUMMARY]}.union({k[0] for k in tup[self.KEY_POSITIVE_TEXT]})) -
                len({k[0] for k in tup[self.KEY_NEGATIVE_SUMMARY]}.union({k[0] for k in tup[self.KEY_NEGATIVE_TEXT]}))
               )
    
    def get_positive_minus_negative(self):
        return self.pos_neg

    def write_counts(self, file_id=None, directory=None, type_=InterimStorage.JSON_GZ):
        if file_id is None:
            file_id = self.FILE_ID_COUNTS
        return InterimStorage(file_id, directory=directory, type_=type_).write(self.pos_neg).get_filepath()
    
    def read_counts(self, file_id=None, directory=None, type_=InterimStorage.JSON_GZ):
        if file_id is None:
            file_id = self.FILE_ID_COUNTS
        self.pos_neg = InterimStorage(id_=file_id, directory=directory, type_=type_).read()
        return self