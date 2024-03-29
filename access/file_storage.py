# System-independet file management
# By default, a symlink 'data' is used for storing data. (https://en.wikipedia.org/wiki/Symbolic_link)
# If you want to use another storage directory, create a file 'data-directory.txt' in the project root directory and specify the path there.
# To add a file, use the constructor below.
# Author: Adrian Wilke https://github.com/adibaba
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
        self.add_file('amazon_gz_file',
                      'movies/movies.txt.gz',
                      note='3.1 GB',
                      web='https://snap.stanford.edu/data/movies.txt.gz')
        self.add_file('opinion-words',
                      'opinion-words/opinion-lexicon-English.rar',
                      note='positive and negative opinion words, 24 KB',
                      web='http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar')
        
        self.add_file('AMORE-NumbersYearsStars',
                      'benchmark/AMORE-NumbersYearsStars.json.gz',
                      note='25 MB')
        self.add_file('AMORE-TextDuplicates',
                      'benchmark/AMORE-TextDuplicates.json.gz',
                      note='18 MB',)
        self.add_file('AMORE-OpinionCollection',
                      'benchmark/AMORE-OpinionCollection.json.gz',
                      note='306 MB',)
        self.add_file('AMORE-OpinionCounts',
                      'benchmark/AMORE-OpinionCounts.json.gz',
                      note='30 MB',)
        self.add_file('deduplicated',
                      'benchmark/deduplicated.pickle.bz2',
                      note='5 MB',)

        self.add_file('AMORE-CountVec-DocTermMatrix',
                      'benchmark/CountVectorizer-DocTermMatrix.pickle.bz2',
                      note='103 MB, (1203682, 918065), scipy.sparse.csr.csr_matrix',
                      web='https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-09-16-AMORE-CountVectorizer/CountVectorizer-DocTermMatrix.pickle.bz2')
        self.add_file('AMORE-CountVec-Object',
                      'benchmark/CountVectorizer-object.pickle.bz2',
                      note='7.3 MB, sklearn.feature_extraction.text.CountVectorizer',
                      web='https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-09-16-AMORE-CountVectorizer/CountVectorizer-object.pickle.bz2')
        self.add_file('AMORE-CountVec-VecidRevno',
                      'benchmark/CountVectorizer-VecidRevno.pickle.bz2',
                      note='4.2 MB, vectorizer ID to review no: 1203682 items',
                      web='https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-09-16-AMORE-CountVectorizer/CountVectorizer-VecidRevno.pickle.bz2')
        self.add_file('AMORE-CountVec-Vocabulary',
                      'benchmark/CountVectorizer-Vocabulary.pickle.bz2',
                      note='7.3 MB, Number of features: 918065',
                      web='https://hobbitdata.informatik.uni-leipzig.de/EML4U/2022-09-16-AMORE-CountVectorizer/CountVectorizer-Vocabulary.pickle.bz2')
        
        # add additional files here
    
    def add_file(self, id_, path, note=None, web=None):
        self.files[id_] = {}
        self.files[id_][self.PATH] = path
        self.files[id_][self.NOTE] = note
        self.files[id_][self.WEB] = web
        
    def get_files(self):
        return self.files
        
    def get_file_info(self, id_, key):
        return self.files[id_][key]
        
    def get_filepath(self, id_):
        return os.path.join(self.get_storage_directory(), *(self.files[id_][self.PATH]).split('/'))
        
    def get_filedir(self, id_):
        return os.path.dirname(self.get_filepath(id_))
    
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