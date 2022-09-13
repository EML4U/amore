
- filtering_comparison.ipynb
- filtering-comparison-plot.ipynb
- filtering-CountVectorizer.ipynb
- _filtering-deduplication-first.ipynb
- filtering-original.ipynb
- filtering-tfidf.ipynb
- opinion_lexicon.ipynb


## Data preparation and overview

- opinion_collection.ipynb  
  Counts negarive and positive words of fields 'summary' and 'text'.  
  Writes AMORE-OpinionCounts.pickle.bz2 and AMORE-OpinionCollection.pickle.bz2
- filtering-opinion.ipynb  
  Reads original.pickle.bz2 and writes opinion-filtered.pickle.bz2  
  Uses OpinionCounts and AMORE-OpinionCounts.json.gz
- extract_duplicates.ipynb  
  Writes AMORE-TextDuplicates.json.gz  
  Collects duplicates
- filtering-deduplication.ipynb  
  Reads opinion-filtered.pickle.bz2 and writes deduplicated.pickle.bz2 and non-deduplicated.pickle.bz2  
  Uses TextDuplicates and AMORE-TextDuplicates.json.gz  
  Writes deduplicated.pickle.bz2
- count_original_amazon.ipynb  
  Creates table with year/star overview
- extract_year_star.ipynb  
  Writes AMORE-NumbersYearsStars
- extract_opinion_words.ipynb
  Collects and counts positive and negative words of summaries and texts



## Misc

- readers.ipynb  
  Runs different readers, which are scripts to read prepared data files.
- readme_data.ipynb  
  Prints file information for readme.


## Outdated

- amore.ipynb  
  Outdated. Splits reviews. Uses:  
  from amore.amore import Amore  
  from amore.split import Split
- print_results.ipynb
- tests.ipynb
- testdata_amore.ipynb  
  Previously used test data.