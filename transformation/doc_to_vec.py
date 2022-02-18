# Author: https://github.com/adibaba
#
# Doc2Vec
#
# https://radimrehurek.com/gensim/models/doc2vec.html
#
# Installation note:
# Make sure you have a C compiler before installing Gensim, to use the optimized doc2vec routines.
# https://radimrehurek.com/gensim/models/doc2vec.html#introduction
#
# Le and Mikolov: Distributed Representations of Sentences and Documents
# https://cs.stanford.edu/~quocle/paragraph_vector.pdf

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
import numpy as np

class DocToVec:
    
    def __init__(self, vector_size=50, epochs=50):
        self.vector_size = vector_size
        self.epochs = epochs
  
    # https://radimrehurek.com/gensim/models/doc2vec.html#usage-examples
    def create_model(self, documents):
        tagged_docs = [self.get_tagged_document(doc, i) for i, doc in enumerate(documents)]

        # https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec
        self.model = Doc2Vec(documents=tagged_docs, vector_size=self.vector_size, epochs=self.epochs)
    
    # https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.TaggedDocument
    def get_tagged_document(self, string, counter):
        return TaggedDocument(self.tokenize(string), [counter])
    
    # https://radimrehurek.com/gensim/utils.html#gensim.utils.simple_preprocess
    def tokenize(self, string):
        return simple_preprocess(string, deacc=False, min_len=2, max_len=15)
    
    
    def save_model(self, file):
        self.model.save(file)
    
    def load_model(self, file):
        self.model = Doc2Vec.load(file)
        
    def get_model(self):
        return self.model
    
    
    def get_vector_size(self):
        return self.vector_size
    
    def get_epochs(self):
        return self.epochs
        
    
    # https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec.infer_vector
    def embed(self, text_list):
        embeddings = []
        for text in text_list:
            emb = self.model.infer_vector(self.tokenize(text))
            embeddings.append(emb)
        return np.stack(embeddings)