class Split:
    
    def __init__(self, split_name, distribution_name, year, star, number):
        self.split_name        = split_name
        self.distribution_name = distribution_name
        self.year   = year
        self.star   = star
        self.number = number
        self.review_ids = []

    def is_full(self):
        return len(self.review_ids) == self.number

    def takes(self, year, star):
        return self.year == year and self.star == star
    
    def add(self, review_id):
        self.review_ids.append(review_id)
    
    def get_review_ids(self):
        return self.review_ids
    
    def __repr__(self):
        return f'Split({self.split_name},{self.distribution_name},{len(self.review_ids)})'