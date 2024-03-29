# AMORE dataset creation
# The steps (1) and (2) can be skipped. To do so, use the load-methods of the respective following step.
# Use to stop: import sys # sys.exit(1)
from access.file_storage import FileStorage
from access.interim_storage import InterimStorage
from amore.amore import Amore
import os.path

# Configure reader
# Possible values: [1997-2012], [1,2,4,5]
reader_min_year = 1997
reader_max_year = 2012
reader_stars    = [1, 5]                                 # TODO: also 2 4
max_lines       = -1
amore = Amore(min_year=reader_min_year, max_year=reader_max_year, stars=reader_stars, max_lines=max_lines)

# Download required files
amore.download_missing_files()                                              # TODO: Check which files are required

# Check, if input files are available
amore.get_missing_files(raise_error=True)

# Reading data and extracting opinion word counts
#amore.extract_opinion_counts(write_file_id='AMORE-OpinionCollection')

# Counting positive and negative words
amore.count_posneg(load_file_id='AMORE-OpinionCollection', write_file_id='AMORE-OpinionCounts')


# (1) Reading data and extracting opinion words
#select_write_file_id = None
#select_write_file_id = 'AMORE-OpinionCounts'
#amore.select_data(write_file_id=select_write_file_id)

# (2) Sorting year-star sets
#sort_load_file_id = None
#sort_load_file_id = 'AMORE-OpinionCounts'
#sort_write_file_id = None
#sort_write_file_id = 'AMORE-Sorted'
#amore.sort(load_file_id=sort_load_file_id, write_file_id=sort_write_file_id)

# (3) Splitting into benchmark datasets
#split_load_file_id = None
#split_load_directory = None
#split_load_file_id = 'AMORE-Sorted'
#  split_load_file_id = '1997-2012_1_5_Sorted'
#  split_load_directory = os.path.dirname(FileStorage().get_filepath(split_load_file_id))
#  splits = amore.split(load_file_id=split_load_file_id, load_file_directory=split_load_directory)

# Checking and writing results
#  final_write_directory = None
#  final_write_file_id = 'AMORE-IDs'
#  amore.check_splits(splits)
#  print(InterimStorage(id_=final_write_file_id, directory=final_write_directory).write(splits).get_filepath())