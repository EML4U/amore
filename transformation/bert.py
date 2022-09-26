import sys
from embedding import BertHuggingface
import numpy as np
import pickle
import os


amazon_raw_file   = 'data/movies/embeddings/amazon_raw.pickle'
embeddings_file   = 'data/movies/embeddings/amazon_all.pickle'
temp_filename = 'data/movies/embeddings/embedding.tmp', 'data/movies/embeddings/keys.tmp'
BERT_BATCH_SIZE = 8


bert = BertHuggingface(5, batch_size=BERT_BATCH_SIZE)
embed = bert.embed_generator

print('loading texts and initializing generator')

with open(amazon_raw_file, 'rb') as handle:
    texts, keys = pickle.load(handle)
    texts, keys = list(texts), list(keys)
for i in range(len(keys)):
    keys[i][1] -= 1   # fix class names from 1..5 to 0..4 for easier 1-hot encoding


def generator_temp():
    for i in range(0, len(texts), BERT_BATCH_SIZE):
        yield texts[i:i + BERT_BATCH_SIZE]

print('texts loaded, now checking whether embeddings file is already there...')

if os.path.isfile(embeddings_file):  # Do not overwrite
    print("Embeddings file already exists, exiting.", embeddings_file)
    exit()
else:
    print('Continuing with some file opening...')

embeddings = []
e_keys = []

# 1.
with open(temp_filename[1], 'wb') as handle:
    pickle.dump(keys, handle)
del keys

# 2. generate the embeddings iteratively
print('starting embedding...')
for chunk in embed(generator_temp()):
    with open(temp_filename[0], 'ab+') as fp:
        pickle.dump(chunk, fp)
    del chunk

# 3. purge script of all unnecessary data
print('embedding successful, now removing all unecessary data...')
del bert
del texts


# 4. try reloading the files
print('removing successful, now reloading and stacking data...')
with open(temp_filename[1], 'rb') as handle:
    emb_keys = pickle.load(handle)

chunks = []
with open(temp_filename[0] , 'rb') as f:
    while True:
        try:
            chunk = pickle.load(f)
            chunks.append(chunk)
        except EOFError:
            break
embeddings = np.vstack(chunks)

# 5. re-delete the chunks
print('reloading successful, now deleting chunks...')
del chunks

print('removing successful, now dumping results...')
dump_data = {'data': (embeddings, emb_keys)}

with open(embeddings_file, 'wb') as handle:
    pickle.dump(dump_data, handle)
