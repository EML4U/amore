# EML4U deduplicated review IDs
# File source: https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-02-15-Benchmark-deduplicated/
# Statistics: https://github.com/EML4U/bench/blob/master/statistics.md

import bz2
import pickle

# see https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-02-15-Benchmark-deduplicated/
file_duplicates = '../../Data/EML4U/2022-02-15-Benchmark-deduplicated/deduplicated.pickle.bz2'
path_data = '../../Data/EML4U/2022-02-05-DriftExplanationPaper'

# Read deduplicated review Ids
with bz2.BZ2File(file_duplicates, 'r') as file:
    dup_ids = pickle.loads(file.read())

# Extract IDs (or exact: tuples)
base = []
neg = []
pos = []
len_base = 40
len_neg  = 36
len_pos  = 4
for year in dup_ids:
    for star in dup_ids[year]:
        #size = len(dup_ids[year][star])
        #print(year, star, size)
        for tup in dup_ids[year][star]:
            if year == 2000 and (star == 1 or star == 2) and len(base) < len_base:
                base.append(tup)
            elif year == 2001 and (star == 1 or star == 2) and len(neg) < len_neg:
                neg.append(tup)
            elif year == 2001 and (star == 4 or star == 5) and len(pos) < len_pos:
                pos.append(tup)
print('base:', len(base))
print('neg: ', len(neg))
print('pos: ', len(pos))



# TODO: notebook killed process. probably not enough memory



# Extra: Read an example (with mapping item ID to raw ID)
emb_base = {}
emb_neg  = {}
emb_pos  = {}
if True:
    # see https://github.com/EML4U/ExplainingDriftTextEmbeddings/blob/2820a1f6825b763ca72b1ca2272e2787af717b90/access/amazon_pickle_reader.py#L68
    from external.amazon_pickle_reader import AmazonPickleReader
    # see https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-02-05-DriftExplanationPaper/
    reader = AmazonPickleReader(path_data)

    # Bag of Words / Doc2Vec
    for tup in base:
        item_no = tup[0]
        raw_id = reader.get_raw_id(item_no)
        emb_base[item_no] = reader.get_bow50(raw_id)
    for tup in neg:
        item_no = tup[0]
        raw_id = reader.get_raw_id(item_no)
        emb_neg[item_no] = reader.get_bow50(raw_id)
    for tup in pos:
        item_no = tup[0]
        raw_id = reader.get_raw_id(item_no)
        emb_pos[item_no] = reader.get_bow50(raw_id)

    print('base:', len(emb_base))
    print('neg: ', len(emb_neg))
    print('pos: ', len(emb_pos))
    print('first base:', emb_base[0])
