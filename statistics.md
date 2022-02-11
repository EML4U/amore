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

## Duplicates in original data

- **Duplicates of summaries**
    - There are 994,312 duplicates of summaries.
    - **7,412,716 reviews** (93.69%) are affected.
    - The most used summary occurs 21,560 times. It is: "Great Movie".
- **Duplicates of texts**
    - There are 1,239,822 duplicates of texts.
    - **7,241,411 reviews** (91.53%) are affected.
    - The most used summary occurs 341 times. It is: "BLU-RAY VERSION IS WORTH BUYING. I DON'T NEED TO TELL YOU ABOUT THE MOVIE, OTHERS ALREADY HAVE. BUT, NOT TOO MANY PEOPLE TELL YOU IF IT IS WORTH UPGRADING FROM YOUR REGULAR DVD TO BLU-RAY. THIS ONE IS WORTH IT. COLORS ARE STUNNING AND SOUNDS GREAT."
    - The second most used summary occurs 325 times. It is: "Purchased this for my grown daughter - VHS just doesn't cut it - by the time a new format comes out - she'll have to buy her own".