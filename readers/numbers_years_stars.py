# Reader for AMORE numbers/year/stars
# DICE group at Paderborn University, https://dice-research.org/
# EML4U project, https://eml4u.github.io/
#
# Example:
# from numbers_years_stars import NumbersYearsStars
# nys = NumbersYearsStars(filepath)
# print(nys.get_by_number(1))
#  [1, 2007, 3]
# year1997 = nys.get_by_year_star(years=[1997])
# print(list(year1997.keys()), list(year1997[1997].keys()), list(year1997[1997][1][0]))
#  [1997] [3, 5, 4, 1, 2] [7760958, 1997, 1]
# good = nys.get_by_year_star(stars=[4,5])
# print(list(good.keys()), list(good[1997].keys()), list(good[1997][5][0]))
#  [2006, 2003, 2002, 2007, 2008, 2004, 2000, 2009, 2011, 2010, 2001, 2005, 2012, 1999, 1998, 1997] [5, 4] [7629210, 1997, 5]
from gzip import GzipFile
import json

class NumbersYearsStars:
    
    KEY_NUMBER = 0
    KEY_YEAR = 1
    KEY_STAR = 2

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
        self.number_dict = None
    
    def get_by_year_star(self, years=[], stars=[]):
        results = {}
        for t in self.get_data():
            if t[self.KEY_YEAR] in years or not years:
                if t[self.KEY_YEAR] not in results.keys():
                    results[t[self.KEY_YEAR]] = {}
                if t[self.KEY_STAR] in stars or not stars:
                    if t[self.KEY_STAR] not in results[t[self.KEY_YEAR]].keys():
                        results[t[self.KEY_YEAR]][t[self.KEY_STAR]] = []
                    results[t[self.KEY_YEAR]][t[self.KEY_STAR]].append(t)
        return results

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