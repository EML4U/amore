from amore.amore import Amore
from access.interim_storage import InterimStorage

# Configure reader
amore = Amore(min_year=2001, max_year=2010)

# Check, if input files are available
amore.get_missing_files(raise_error=True)

# Reading data and extracting opinion words
amore.select_data(write_file_id='AMORE-OpinionCounts')

# Sorting year-star sets
amore.sort(load_file_id='AMORE-OpinionCounts', write_file_id='AMORE-Sorted')

# Splitting into benchmark datasets
splits = amore.split(load_file_id='AMORE-Sorted')

# Checking IDs
amore.check_splits(splits)

# Write result and print file path
print(InterimStorage(id_='AMORE-IDs').write(splits).get_filepath())