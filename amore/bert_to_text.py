import pickle


class BertToText:
    def __init__(self, raw_path):
        self.raw_path = raw_path
        self.multi_fast = False
        self.texts = None
        self.keys = None

    def toggle_multi_fast(self, enable=True):
        self.multi_fast = enable
        if enable:
            with open(self.raw_path, 'rb') as handle:
                texts, keys = pickle.load(handle)
                self.texts, self.keys = list(texts), list(keys)
        else:
            del self.texts
            del self.keys
            self.texts = None
            self.keys = None

    def get_raw_text(self, doc_id=0):
        if self.multi_fast:
            return self.texts[doc_id], self.keys[doc_id]
        else:
            with open(self.raw_path, 'rb') as handle:
                texts, keys = pickle.load(handle)
            imp = texts[doc_id], keys[doc_id]
            del texts
            del keys
        return imp
    
    
# test
#b = BertToText('/home/eml4u/EML4U/data/symlink-target/clustering/amazon_all.pickle')
b = BertToText('/home/eml4u/EML4U/data/symlink-target/clustering/amazon_raw.pickle')
b.toggle_multi_fast
print(b.get_raw_text(10000))
    
