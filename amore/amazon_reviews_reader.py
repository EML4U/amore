# Reader for Amazon movie reviews
#
# https://snap.stanford.edu/data/movies.txt.gz (3321791660 bytes, 3 GB)
# https://snap.stanford.edu/data/web-Movies.html
#
# Notes: Number starts with 1. Mode "text" concatenates fields "summary" and "text"
# Version 2: Changelog: Removed method download(), added mode "typed".
# Version 1: https://github.com/EML4U/Drift-detector-comparison/blob/1.0.0/word2vec/amazon_reviews_reader.py
# Author: Adrian Wilke https://github.com/adibaba
#
# Example:
# from amazon_reviews_reader import AmazonReviewsReader
# for item in AmazonReviewsReader('movies.txt.gz', AmazonReviewsReader.MODE_TYPED, max_docs=3):
#    print(item[AmazonReviewsReader.KEY_SCORE], end=' ')
#    print(item[AmazonReviewsReader.KEY_TIME].year, end=' #')
#    print(item[AmazonReviewsReader.KEY_NUMBER])
#    print(item[AmazonReviewsReader.KEY_SUMMARY], item[AmazonReviewsReader.KEY_TEXT], sep='  |  ')
#    print()

from datetime import datetime
import gensim
import gzip

# Stream corpus (memory efficient)
# See: https://radimrehurek.com/gensim/auto_examples/core/run_corpora_and_vector_spaces.html#corpus-streaming-one-document-at-a-time
class AmazonReviewsReader:
    
    MODE_FIELDS = "fields"
    MODE_TYPED  = "typed"
    MODE_TEXT   = "text"
    MODE_TOKENS = "tokens"
    MODE_TAGDOC = "tagdoc"
    
    KEY_PRODUCT_ID   = 'productId'
    KEY_USER_ID      = 'userId'
    KEY_PROFILE_NAME = 'profileName'
    KEY_HELPFULNESS  = 'helpfulness'
    KEY_SCORE        = 'score'
    KEY_TIME         = 'time'
    KEY_SUMMARY      = 'summary'
    KEY_TEXT         = 'text'
    KEY_NUMBER       = 'number'

    def __init__(self, file, mode, max_docs=-1, min_year=-1, max_year=-1, min_score=-1, max_score=-1):
        self.file = file
        self.mode = mode
        self.max_docs = max_docs
        self.min_year = min_year
        self.max_year = max_year
        self.min_score = min_score
        self.max_score = max_score

    def __iter__(self):
        c = 0
        i = 0
        with gzip.open(self.file, 'rb') as f:
            for line in f:
                if not line.strip():
                    continue
                line_spilt = line.decode(encoding='iso-8859-1').split(':', 1)

                # First key of every entry -> reset values
                if line_spilt[0] == "product/productId":
                    self.exclude = False
                    self.entry = {}
                    
                # Get key/value
                try:
                    self.entry[line_spilt[0].split('/', 1)[1]] = line_spilt[1].strip()
                except IndexError:
                    # Error in amazon movies file: profileName may be splitted into 2 lines (e.g. line 1274403)
                    continue

                # Filter by score
                if (self.min_score!=-1 or self.max_score!=-1) and line_spilt[0] == "review/score":
                    score = float(line_spilt[1].strip())
                    if(self.min_score != -1 and score < self.min_score):
                        self.exclude = True
                    elif(self.max_score != -1 and score > self.max_score):
                        self.exclude = True

                # Filter by year
                elif (self.min_year!=-1 or self.max_year!=-1) and line_spilt[0] == "review/time":
                    year = datetime.fromtimestamp(int(line_spilt[1])).year
                    if(self.min_year != -1 and year < self.min_year):
                        self.exclude = True
                    elif(self.max_year != -1 and year > self.max_year):
                        self.exclude = True

                # Last key -> Process data
                elif line_spilt[0] == "review/text":
                    
                    # Filter
                    i += 1
                    if(self.exclude):
                        continue
                    
                    # Max number of docs
                    c += 1
                    if(self.max_docs != -1 and c > self.max_docs):
                        break
                    
                    # Mode fields
                    if(self.mode == self.MODE_FIELDS):
                        self.entry[self.KEY_NUMBER] = i
                        yield self.entry
                        continue
                    
                    # Mode typed
                    if(self.mode == self.MODE_TYPED):
                        helpfulness = self.entry[self.KEY_HELPFULNESS].split('/')
                        self.entry[self.KEY_HELPFULNESS] = (int(helpfulness[0]), int(helpfulness[1]))
                        self.entry[self.KEY_SCORE] = int(float(self.entry[self.KEY_SCORE]))
                        self.entry[self.KEY_TIME] = datetime.fromtimestamp(int(self.entry[self.KEY_TIME]))
                        self.entry[self.KEY_NUMBER] = i
                        yield self.entry
                        continue
        
                    # Mode text
                    if(self.mode == self.MODE_TEXT):
                        yield self.entry[self.KEY_SUMMARY] + " " + self.entry[self.KEY_TEXT]
                        continue
                    
                    # Mode tokens
                    tokens = gensim.utils.simple_preprocess(self.entry[self.KEY_SUMMARY] + " " + self.entry[self.KEY_TEXT])
                    if(self.mode == self.MODE_TOKENS):
                        yield tokens
                        continue
                    
                    # Mode tagdoc
                    if(self.mode != self.MODE_TAGDOC):
                        raise ValueError("Unknown mode", self.mode)
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [c])