# Original data: Amazon movie reviews (raw web data)

- Source: https://snap.stanford.edu/data/web-Movies.html
- Article: McAuley and Leskovec (2013): From Amateurs to Connoisseurs: Modeling the Evolution of User Expertise through Online Reviews ([DOI 10.1145/2488388.2488466](https://doi.org/10.1145/2488388.2488466))

## Numbers of reviews

|       | 1997 |  1998 |  1999  |   2000  |   2001  |   2002  |   2003  |   2004  |   2005  |   2006  |   2007  |   2008  |   2009  |   2010  |   2011  |   2012  |      Sum  |
|  ---: | ---: |  ---: |   ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |    ---: |      ---: |  
| **1** |    6 |   191 |  4.844 |  19.944 |  24.221 |  25.311 |  25.734 |  41.016 |  54.744 |  49.049 |  49.521 |  56.076 |  59.099 |  65.343 |  72.957 |  81.276 |   629.332 |
| **2** |    1 |   262 |  3.631 |  17.808 |  20.320 |  22.641 |  24.183 |  33.117 |  40.868 |  37.992 |  40.205 |  40.138 |  39.680 |  41.430 |  45.767 |  47.356 |   455.399 |
| **3** |    8 |   442 |  6.458 |  30.907 |  35.395 |  37.798 |  43.323 |  60.489 |  71.012 |  66.128 |  75.239 |  74.057 |  73.178 |  70.279 |  72.055 |  74.826 |   791.594 |
| **4** |   29 |   797 | 14.178 |  73.314 |  79.152 |  84.276 |  90.527 | 119.160 | 138.000 | 135.581 | 167.632 | 161.693 | 149.771 | 142.000 | 148.457 | 150.248 | 1.654.815 |
| **5** |   64 | 3.313 | 49.866 | 192.002 | 189.638 | 198.712 | 205.916 | 257.603 | 308.080 | 311.252 | 452.009 | 412.870 | 422.403 | 426.248 | 465.918 | 484.650 | 4.380.544 |
| **∑** |  108 | 5.005 | 78.977 | 333.975 | 348.726 | 368.738 | 389.683 | 511.385 | 612.704 | 600.002 | 784.606 | 744.834 | 744.131 | 745.300 | 805.154 | 838.356 | 7.911.684 |

## Numbers of positive/negative reviews

- Positive reviews with |pos-words| > |neg-words|.
- Negative reviews with |pos-words| < |neg-words|.
- Neutral reviews with -1 <= |pos-words| - |neg-words| <= 1.
- Two fields concatenated: summary and text.
- Both checked: single word occurences (count all words in texts) and general word occurences (each word counted once or never).

|     |   1997 |   1998 |   1999 |   2000 |   2001 |   2002 |   2003 |   2004 |   2005 |   2006 |   2007 |   2008 |   2009 |   2010 |   2011 |   2012 |     Sum |
|:----|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|--------:|
| 1   |      6 |    104 |   3110 |  12698 |  14751 |  15934 |  16611 |  26835 |  35093 |  29878 |  30496 |  33972 |  35420 |  39177 |  43552 |  48432 |  386069 |
| 2   |    nan |    122 |   1589 |   7820 |   8866 |  10127 |  10742 |  15439 |  19141 |  17152 |  17724 |  17271 |  16641 |  18523 |  20105 |  21036 |  202298 |
| 3   |    nan |    107 |   1535 |   6152 |   6376 |   6280 |   6917 |  10403 |  12668 |  11947 |  16364 |  16218 |  17691 |  17052 |  18243 |  19266 |  167219 |
| 4   |     13 |    599 |  10429 |  52130 |  56607 |  58688 |  62256 |  80602 |  93419 |  93912 | 121336 | 117024 | 110548 | 102739 | 109983 | 112609 | 1182894 |
| 5   |     52 |   2694 |  39621 | 150126 | 148077 | 153886 | 157562 | 194587 | 234448 | 242242 | 370047 | 341264 | 352366 | 353522 | 393641 | 410560 | 3544695 |
| Sum |     71 |   3626 |  56284 | 228926 | 234677 | 244915 | 254088 | 327866 | 394769 | 395131 | 555967 | 525749 | 532666 | 531013 | 585524 | 611903 | 5483175 |

## Duplicates in original data

- **Duplicates of summaries**
    - There are 994,312 duplicates of summaries.
    - **7,412,716 reviews** (93.69%) are affected.
    - The most used summary occurs 21,560 times. It is: "Great Movie".
    - Summaries are short, multiple occurrence is reasonable, therefore they're not included in deduplication.
- **Duplicates of texts**
    - There are 1,239,822 duplicates of texts.
    - **7,241,411 reviews** (91.53%) are affected.
    - The most used summary occurs 341 times. It is: "BLU-RAY VERSION IS WORTH BUYING. I DON'T NEED TO TELL YOU ABOUT THE MOVIE, OTHERS ALREADY HAVE. BUT, NOT TOO MANY PEOPLE TELL YOU IF IT IS WORTH UPGRADING FROM YOUR REGULAR DVD TO BLU-RAY. THIS ONE IS WORTH IT. COLORS ARE STUNNING AND SOUNDS GREAT."
    - The second most used summary occurs 325 times. It is: "Purchased this for my grown daughter - VHS just doesn't cut it - by the time a new format comes out - she'll have to buy her own".

## Duplicates in data cleaned by opinion words

- **Deduplication**
    - **489,009 non-duplicate reviews** and
    - **1,238,812 deduplicated reviews** with same year and stars.
    - Not included: 11,296 reviews (1010 text duplicates) with different year or stars.

|     |   1997 |   1998 |   1999 |   2000 |   2001 |   2002 |   2003 |   2004 |   2005 |   2006 |   2007 |   2008 |   2009 |   2010 |   2011 |   2012 |     Sum |
|:----|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|--------:|
| 1   |      2 |     26 |    597 |   2512 |   3015 |   3597 |   3689 |   6643 |  10413 |   9943 |  11125 |  12661 |  14150 |  15822 |  19132 |  21570 |  134897 |
| 2   |    nan |     30 |    437 |   2162 |   2541 |   3048 |   3364 |   4880 |   7053 |   7050 |   8067 |   8417 |   8846 |   9536 |  11363 |  12041 |   88835 |
| 3   |      1 |     65 |    880 |   3932 |   4562 |   5064 |   5860 |   8592 |  11420 |  11322 |  13932 |  13944 |  14835 |  14925 |  16796 |  17593 |  143723 |
| 4   |      4 |    146 |   2166 |   9832 |  11216 |  12257 |  13466 |  19364 |  25958 |  27917 |  37664 |  36838 |  37089 |  36408 |  40392 |  40528 |  351245 |
| 5   |     14 |    561 |   7266 |  25204 |  26294 |  29576 |  32416 |  46222 |  64445 |  71619 | 108952 | 104455 | 112998 | 113957 | 130571 | 134571 | 1009121 |
| Sum |     21 |    828 |  11346 |  43642 |  47628 |  53542 |  58795 |  85701 | 119289 | 127851 | 179740 | 176315 | 187918 | 190648 | 218254 | 226303 | 1727821 |