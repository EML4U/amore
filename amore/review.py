class Review:
    
    def __init__(self, id_, positive_word_count, negative_word_count):
        self.id_ = id_
        self.positive_word_count = positive_word_count 
        self.negative_word_count = negative_word_count
    
    def get_positive_sort_value(self):
        return self.negative_word_count - self.positive_word_count
    
    def get_negative_sort_value(self):
        return self.positive_word_count - self.negative_word_count

    def __repr__(self):
        return f'Review("{self.id_}","{self.positive_word_count}",{self.negative_word_count})'