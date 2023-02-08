# AMORE: Drift benchmark datasets

AMORE (Amazon Movie Reviews) is a collection of benchmark datasets to compare drift explanation approaches.
Each dataset consists of two sets of unlabeled texts, which are either positive (good rated) or negative (bad rated) movie reviews.
The goal of drift explanation approaches is to detect drift between the two sets and explain why drift was detected.

## AMORE datasets

- **AMORE.1**
  - Set A: 10,000 negative reviews (from 2000 to 2004).
  - Set B: 10,000 reviews (from 2005), 90% negative and 10% positive.
  - Task: Detect the texts in B which contain drift and explain the drift.
  - Note: Drift is mainly based on 3 to 4 words, which only occur in the positive reviews.
- **AMORE.2**
  - Set A: 10,000 negative reviews (from 2006 to 2007).
  - Set B: 10,000 reviews (from 2008), 90% negative and 10% positive.
  - Task: Detect the texts in B which contain drift and explain the drift.
  - Note: Drift is mainly based on 10 words. Negative reviews contain 1 of those, positive contain 5 to 9.

## Misc

- [Data statistics](statistics.md)
- [Data download](data.md)

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