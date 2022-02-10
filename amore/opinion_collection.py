from amore.opinion_lexicon import OpinionLexicon
from amore.amazon_reviews_reader import AmazonReviewsReader
from access.file_storage import FileStorage
from access.interim_storage import InterimStorage
from gensim.utils import simple_preprocess
from collections import Counter

class OpinionCollection:
    
    FILE_ID = 'OpinionCollection'
    
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
    
    def write(self, file_id=None, directory=None):
        if file_id is None:
            file_id = self.FILE_ID
        return InterimStorage(file_id, directory=directory).write(self.results).get_filepath()
    
    def read(self, file_id=None, directory=None):
        if file_id is None:
            file_id = self.FILE_ID
        self.results = InterimStorage(id_=file_id, directory=directory).read()
        return self
        