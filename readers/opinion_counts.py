# Reader for AMORE opinion counts
# DICE group at Paderborn University, https://dice-research.org/
# EML4U project, https://eml4u.github.io/
#
# Example:
# from opinion_counts import OpinionCounts
# ocounts = OpinionCounts(filepath)
# print(ocounts.get(1))
#  [-5, -4]
# print(ocounts.get_existent(1))
#  -5
# print(ocounts.get_occurences(1))
#  -4
from gzip import GzipFile
import json

class OpinionCounts:

    KEY_EXISTENT = 0
    KEY_OCCURENCES = 1
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
        
    def get_existent(self, number):
        return self.get(number)[self.KEY_EXISTENT]
        
    def get_occurences(self, number):
        return self.get(number)[self.KEY_OCCURENCES]

    def get(self, number):
        return self.get_data().get(str(number))
    
    def get_data(self):
        if self.data is None:
            with GzipFile(self.filepath, 'r') as file:
                self.data = json.loads(file.read())
        return self.data