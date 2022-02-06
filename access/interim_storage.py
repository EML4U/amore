# This class provides basic methods to fastly store data in different formats.
# By default, Pickle+BZ2 and the system temporary directory are used.
# Author: https://github.com/adibaba
import os
import tempfile
import json
import bz2
import pickle

class InterimStorage:
    
    JSON      = 'json'
    JSON_BZ2  = 'json.bz2'
    PICKLE    = 'pickle'
    PICKLE_BZ = 'pickle.bz2'
    
    def __init__(self, id_, type_=PICKLE_BZ, directory=None):
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
        elif(self.type_ is self.JSON_BZ2):
            data = json.dumps(data).encode()
        elif(self.type_ is self.PICKLE or self.PICKLE_BZ):
            data = pickle.dumps(data)
        # Compress/write
        if(self.type_ is self.JSON):
            with open(self.get_filepath(), 'w') as file:
                file.write(data)
        elif(self.type_ is self.PICKLE):
            with open(self.get_filepath(), 'wb') as file:
                file.write(data)
        elif(self.type_ is self.JSON_BZ2 or self.PICKLE_BZ):
            with bz2.BZ2File(self.get_filepath(), 'wb') as file:
                file.write(data)
                
        return self

    def read(self):
        # Read/decompress
        if(self.type_ is self.JSON):
            with open(self.get_filepath(), 'r') as file:
                data = file.read()
        elif(self.type_ is self.PICKLE):
            with open(self.get_filepath(), 'rb') as file:
                data = file.read()
        elif(self.type_ is self.JSON_BZ2 or self.PICKLE_BZ):
            with bz2.BZ2File(self.get_filepath(), 'r') as file:
                data = file.read()
        # Decode
        if(self.type_ is self.JSON):
            data = json.loads(data)
        elif(self.type_ is self.JSON_BZ2):
            data = json.loads(data)
        elif(self.type_ is self.PICKLE or self.PICKLE_BZ):
            data = pickle.loads(data)

        return data