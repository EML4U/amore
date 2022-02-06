# Opinion Lexicon
#
# http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar
# https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon
# Author: Adrian Wilke https://github.com/adibaba
#
# Example:
# from opinion_lexicon_reader import OpinionLexiconReader
# OpinionLexiconReader('opinion-lexicon-English.rar').get_positive_set()

from rarfile import RarFile

class OpinionLexicon:
        
    def __init__(self, file):
        self.file = file
        self.positive_set = None
        self.negative_set = None
    
    def get_positive_word(self):
        with RarFile(self.file) as rf:
            with rf.open('opinion-lexicon-English/positive-words.txt') as f:
                for line in f:
                    line = line.decode('iso-8859-1').strip()
                    if line and not line.startswith(';'):
                        yield line
    
    def get_negative_word(self):
        with RarFile(self.file) as rf:
            with rf.open('opinion-lexicon-English/negative-words.txt') as f:
                for line in f:
                    line = line.decode('iso-8859-1').strip()
                    if line and not line.startswith(';'):
                        yield line
                        
    def get_positive_set(self):
        if(self.positive_set is None):
             self.positive_set = {word for word in self.get_positive_word()}
        return self.positive_set
    
    def get_negative_set(self):
        if(self.negative_set is None):
            self.negative_set = {word for word in self.get_negative_word()}
        return self.negative_set
    
    def extract_positive_words(self, set_):
        return [word for word in set_ if word in self.positive_set]
    
    def extract_negative_words(self, set_):
        return [word for word in set_ if word in self.negative_set]