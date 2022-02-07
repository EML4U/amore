class Split:
    
    def __init__(self, split_name, distribution_name, year, star, number):
        self.split_name        = split_name
        self.distribution_name = distribution_name
        self.year   = year
        self.star   = star
        self.number = number
        
        self.counter = number
        self.review_ids = []

    def count_down(self, year, star):
        if(year != self.year or star != self.star):
            return

        while(self.counter > 0):
            yield self.counter
            self.counter -= 1
    
    def add(self, review_id):
        self.review_ids.append(review_id)
    
    def get_review_ids(self):
        return self.review_ids
    
    def __repr__(self):
        return f'Review({self.split_name},{self.distribution_name},{len(self.review_ids)})'