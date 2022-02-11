# Reader for AMORE opinion collection
# DICE group at Paderborn University, https://dice-research.org/
# EML4U project, https://eml4u.github.io/
#
# Example:
# from opinion_collection import OpinionCollection
# oc = OpinionCollection(filepath)
# print(oc.get_negative_summary(1))
#  [['darkness', 1]]
# print(oc.get_positive_summary(1))
#  [['miracle', 1]]
# print(oc.get_negative_text(1))
#  [['raped', 1], ['desert', 2], ['undocumented', 1], ['relentless', 1], ['vicious', 1], ...]
# print(oc.get_positive_text(1))
#  [['enhanced', 1], ['fascination', 1], ['miracles', 1], ['heavenly', 1], ['interesting', 1], ...]
from gzip import GzipFile
import json

class OpinionCollection:
    
    KEY_NUMBER = 0
    KEY_NEGATIVE_SUMMARY = 1
    KEY_POSITIVE_SUMMARY = 2
    KEY_NEGATIVE_TEXT = 3
    KEY_POSITIVE_TEXT = 4
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
        self.number_dict = None
        
    def get_negative_summary(self, number):
        return self.get_number_dict()[number][self.KEY_NEGATIVE_SUMMARY]
        
    def get_positive_summary(self, number):
        return self.get_number_dict()[number][self.KEY_POSITIVE_SUMMARY]
        
    def get_negative_text(self, number):
        return self.get_number_dict()[number][self.KEY_NEGATIVE_TEXT]
        
    def get_positive_text(self, number):
        return self.get_number_dict()[number][self.KEY_POSITIVE_TEXT]

    def get_by_number(self, number):
        return self.get_number_dict()[number]

    def get_number_dict(self):
        if self.number_dict is None:
            self.number_dict = {}
            for t in self.get_data():
                self.number_dict[t[self.KEY_NUMBER]] = t
        return self.number_dict

    def get_data(self):
        if self.data is None:
            with GzipFile(self.filepath, 'r') as file:
                self.data = json.loads(file.read())
        return self.data