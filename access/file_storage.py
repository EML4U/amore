# System-independet file management
# By default, a symlink 'data' is used for storing data. (https://en.wikipedia.org/wiki/Symbolic_link)
# If you want to use another storage directory, create a file 'data-directory.txt' in the project root directory and specify the path there.
# To add a file, use the constructor below.
# Author: https://github.com/adibaba
import os
import urllib.request

class FileStorage():
    CONFIG_DATA_FILENAME = 'data-directory.txt'
    DEFAULT_DATA_PATH = 'data'
    PATH = 'path'
    NOTE = 'note'
    WEB = 'web'
    files = {}
    
    def __init__(self):
        self.add_file('amazon_gz_file', 'movies/movies.txt.gz', note='3.1 GB', web='https://snap.stanford.edu/data/movies.txt.gz')
        self.add_file('opinion-words', 'opinion-words/opinion-lexicon-English.rar', note='positive and negative opinion words, 24 KB', web='http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar')
        # test
#        self.add_file('readme', 'movies/README.test.md', note='a test file', web='https://raw.githubusercontent.com/EML4U/Drift-detector-comparison/main/README.md')
        # opinion words

        # amazon original

        # for paper
#        self.add_file('amazon_raw.pickle', 'clustering/amazon_raw.pickle', 'sorted amazon movie reviews data, created by amazon_movie_sorter.py, 7.6 GB')
#        self.add_file('amazon_bow_50.pickle', 'clustering/amazon_raw.pickle', 'BoW 50 dimensions, created by generator_amazon_movie_embeddings.py, 1.8 GB')
        # add additional files here
    
    def add_file(self, id_, path, note=None, web=None):
        self.files[id_] = {}
        self.files[id_][self.PATH] = path
        self.files[id_][self.NOTE] = note
        self.files[id_][self.WEB] = web
        
    def get_files(self):
        return self.files
        
    def get_filepath(self, id_):
            return os.path.join(self.get_storage_directory(), *(self.files[id_][self.PATH]).split('/'))
    
    def get_storage_directory(self):
        if(os.path.isfile(self.get_config_file_path())):
            with open(self.get_config_file_path(), 'r') as file:
                return file.read().strip()
        else:
            return os.path.join(self.get_project_rootpath(), self.DEFAULT_DATA_PATH)
    
    def get_config_file_path(self):
        return os.path.join(self.get_project_rootpath(), self.CONFIG_DATA_FILENAME)
    
    def get_project_rootpath(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    def download(self, id_):
        if(os.path.isfile(self.get_filepath(id_))):
            print('File exists, will not be downloaded')
        else:
            os.makedirs(os.path.abspath(os.path.join(self.get_filepath(id_), '..')), exist_ok=True)
            urllib.request.urlretrieve(self.files[id_][self.WEB], filename=self.get_filepath(id_))
            urllib.request.urlcleanup()
    
    def print_file_overview(self):
        for item in self.get_files().items():
            print(item[0])
            for item in item[1].items():
                print('', item[0].ljust(5), item[1])