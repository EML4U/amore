from amore.amore import Amore
from access.interim_storage import InterimStorage

amore = Amore()
amore.get_missing_files(raise_error=True)
amore.select_data()
amore.sort()
splits = amore.split()
print(InterimStorage(id_='AMORE-IDs').write(splits).get_filepath())