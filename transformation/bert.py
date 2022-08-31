# Config
amazon_file               = '/home/eml4u/EML4U/data/amazon/movies.txt.gz'
amazon_reviews_reader_dir = '../amore'

import sys
sys.path.insert(1, amazon_reviews_reader_dir)
from amazon_reviews_reader import AmazonReviewsReader

data_dict = {}
id = 0
for item in AmazonReviewsReader(amazon_file, AmazonReviewsReader.MODE_TEXT, max_docs=-1):

    # id is the line number, starting at 1
    id += 1
        
    # item contains a concatenation of the form ["summary"] + " " + ["text"]
    item = item.replace('<br />', ' ')
    
    # Fake embeddings of dimension 2
    # TODO: replace by BERT embeddings
    embeddings = []
    embeddings.append(id)
    embeddings.append(len(item))
    
    # Simply put ID and embeddings to a dict
    data_dict[id] = embeddings

print(data_dict)

# TODO: Store data_dict as pickle