# AMORE

- [Data statistics](statistics.md)

## Data files and Python code

- For single results, there are related data files and python classes to read them.
- The data format is JSON ([Wikipedia](https://en.wikipedia.org/wiki/JSON)), the files are compressed using gzip ([Wikipedia](https://en.wikipedia.org/wiki/Gzip)).
- The line number of the original raw file are used as identifiers.

### Data Files, formats, examples and Python classes

- File: AMORE-TextDuplicates.json.gz
    - Format: [number1, number2, ...]
    - Example: [1, 5615911]
    - Size: 1,239,822 entries
    - Code: [text_duplicates.py](readers/text_duplicates.py)
- File: AMORE-NumbersYearsStars.json.gz
    - Format: [number, year, stars]
    - Example: [1, 2007, 3]
    - Size: 7,911,684 entries
    - Code: [numbers_years_stars.py](readers/numbers_years_stars.py)