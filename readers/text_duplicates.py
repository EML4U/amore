# Reader for AMORE text duplicates
# DICE group at Paderborn University, https://dice-research.org/
# EML4U project, https://eml4u.github.io/
#
# Example:
# from text_duplicates import TextDuplicates
# td = TextDuplicates(filepath)
# print(len(td.get_data()))
#  1239822
# print(td.get_data()[0])
#  [1, 5615911]
from gzip import GzipFile
import json

class TextDuplicates:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def get_data(self):
        if self.data is None:
            with GzipFile(self.filepath, 'r') as file:
                self.data = json.loads(file.read())
        return self.data