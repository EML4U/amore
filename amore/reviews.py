from access.interim_storage import InterimStorage
from amore.review import Review
from operator import methodcaller

class Reviews:
    
    FILE_ID_COUNTER = 'amore-counter'
    
    def __init__(self):
        self.review_objects = {} # {year, {star, [review_obj]}}
    
    def get_years(self):
        return self.review_objects.keys()
    
    def get_stars(self, year):
        return self.review_objects[year].keys()
        
    def add_review(self, year, star, review_obj):
        if not year in self.review_objects.keys():
            self.review_objects[year] = {}
        if not star in self.review_objects[year].keys():
            self.review_objects[year][star] = []
        self.review_objects[year][star].append(review_obj)
        return self
        
    def get_positive_sorted(self, year, star):
        return sorted(self.review_objects[year][star], key=methodcaller('get_positive_sort_value'))

    def get_positive_sorted_tuple(self, year, star):
        tup = []
        for review in self.get_positive_sorted(year, star):
            tup.append(review.get_id_counts())
        return tup
    
    def get_negative_sorted(self, year, star):
        return sorted(self.review_objects[year][star], key=methodcaller('get_negative_sort_value'))

    def get_negative_sorted_tuple(self, year, star):
        tup = []
        for review in self.get_negative_sorted(year, star):
            tup.append(review.get_id_counts())
        return tup
    
    def write_review_objects(self, file_id=None, directory=None, type_=InterimStorage.PICKLE_BZ2, verbose=True):
        if file_id is None:
            file_id=self.FILE_ID_COUNTER
        interim_storage = InterimStorage(file_id, type_=type_, directory=directory)
        interim_storage.write(self.review_objects)
        if verbose:
            print('Wrote:', interim_storage.get_filepath())
        return self
    
    def read_review_objects(self, file_id=None, directory=None, type_=InterimStorage.PICKLE_BZ2, verbose=True):
        if file_id is None:
            file_id=self.FILE_ID_COUNTER
        interim_storage = InterimStorage(file_id, type_=type_, directory=directory)
        self.review_objects = interim_storage.read()
        if verbose:
            print('Loaded:', interim_storage.get_filepath())
        return self
    
    def get_size(self):
        size = 0
        for year in self.review_objects.keys():
            for star in self.review_objects[year].keys():
                size += len(self.review_objects[year][star])
        return size