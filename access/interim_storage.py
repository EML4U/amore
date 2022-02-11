# This class provides basic methods to fastly store data in different formats.
# By default, Pickle+BZ2 and the system temporary directory are used.
# GZ is faster as BZ2.
# In JSON, integer keys are stored as strings.
# JSON is also limited to Python data structures, see https://docs.python.org/3/library/json.html#encoders-and-decoders
# Author: Adrian Wilke https://github.com/adibaba
import os
import tempfile
import json
import bz2
import gzip
import pickle

class InterimStorage:
    
    JSON       = 'json'
    JSON_BZ2   = 'json.bz2'
    JSON_GZ    = 'json.gz'
    PICKLE     = 'pickle'
    PICKLE_BZ2 = 'pickle.bz2'
    PICKLE_GZ  = 'pickle.gz'
    
    def __init__(self, id_, type_=PICKLE_BZ2, directory=None):
        self.id_ = id_
        self.type_ = type_
        
        if directory is None:
            self.directory = os.path.join(tempfile.gettempdir(), 'InterimStorage')
        else:
            self.directory = directory
    
    def get_directory(self):
        return self.directory
    
    def get_id(self):
        return self.id_

    def get_filepath(self):
        return os.path.join(self.directory, self.id_ + '.' + self.type_)
    
    def isfile(self):
        return os.path.isfile(self.get_filepath())
    
    def delete_file(self):
        return os.remove(self.get_filepath())
    
    def write(self, data):
        os.makedirs(self.get_directory(), exist_ok=True)
        # Encode
        if(self.type_ is self.JSON):
            data = json.dumps(data)
        elif(self.type_ is self.JSON_BZ2 or self.type_ is self.JSON_GZ):
            data = json.dumps(data).encode()
        elif(self.type_ is self.PICKLE or self.type_ is self.PICKLE_BZ2 or self.type_ is self.PICKLE_GZ):
            data = pickle.dumps(data)
        else:
            raise ValueError
            
        # Compress/write
        if(self.type_ is self.JSON):
            with open(self.get_filepath(), 'w') as file:
                file.write(data)
        elif(self.type_ is self.PICKLE):
            with open(self.get_filepath(), 'wb') as file:
                file.write(data)
        elif(self.type_ is self.JSON_BZ2 or self.type_ is self.PICKLE_BZ2):
            with bz2.BZ2File(self.get_filepath(), 'wb') as file:
                file.write(data)
        elif(self.type_ is self.JSON_GZ or self.type_ is self.PICKLE_GZ):
            with gzip.GzipFile(self.get_filepath(), 'wb') as file:
                file.write(data)
        else:
            raise ValueError
                
        return self

    def read(self):
        # Read/decompress
        if(self.type_ is self.JSON):
            with open(self.get_filepath(), 'r') as file:
                data = file.read()
        elif(self.type_ is self.PICKLE):
            with open(self.get_filepath(), 'rb') as file:
                data = file.read()
        elif(self.type_ is self.JSON_BZ2 or self.type_ is self.PICKLE_BZ2):
            with bz2.BZ2File(self.get_filepath(), 'r') as file:
                data = file.read()
        elif(self.type_ is self.JSON_GZ or self.type_ is self.PICKLE_GZ):
            with gzip.GzipFile(self.get_filepath(), 'r') as file:
                data = file.read()
        else:
            raise ValueError
                
        # Decode
        if(self.type_ is self.JSON):
            data = json.loads(data)
        elif(self.type_ is self.JSON_BZ2 or self.type_ is self.JSON_GZ):
            data = json.loads(data)
        elif(self.type_ is self.PICKLE or self.type_ is self.PICKLE_BZ2 or self.type_ is self.PICKLE_GZ):
            data = pickle.loads(data)
        else:
            raise ValueError

        return data