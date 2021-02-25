Overview
This script takes as input a csv file containing abundance counts for airborne microbes and yields outliers using Seasonal-Trend decomposition using LOESS (STL).
This is accomplished by running STL on a row (which should indicate an abundance time-series for a given identified microbe) and iterating this process over
the entire dataset. For each STL run, the residual(s) are obtained over a given date span.

Dependencies
 -Python 3 (run on 3.9.1)
 -pandas (run on 1.2.2)
 -numpy (run on 1.20.1)
 -matplotlib (run on 3.3.4)
 -statsmodels (run on 0.12.2)

Usage
>>#Obtain the 5 largest and 5 smallest microbial remainders for the final 3 days of the dataset
>>import SLT
>>outliers = SLT.Outliers(path_to_csv)
>>outliers.all_outliers(-3, ":", avg_flag=True)

                      2003-04-24  2003-04-25  2003-04-26
Unclassified         -122.406159 -301.247425 -504.036064
Sphingomonadaceae    -110.400698 -274.799009 -461.647264
Unclassified         -108.605897 -270.171168 -453.735678
Bacillaceae          -104.292540 -257.607428 -431.623277
Unclassified         -103.894660 -256.967664 -430.755091
Bacillaceae            23.120253   46.415174   71.125009
Propionibacteriaceae   26.772970   58.400236   92.691835
Bacillaceae            30.622072   66.012767  104.609053
Enterobacteriaceae     35.928383   75.466742  118.428281
Nocardiaceae           57.654975   34.186216 -437.536284
mean                  -36.670005  -90.278105 -151.231112

Execution time

Input
input file: Austin_data.csv
Input file size: 4.48 MB
Input file rows x cols: 1994 x 237
Input file processed rows x cols: 1993 x 113
Outliers instantiation: Outliers("../../Austin_data.csv")
all_outliers call: outliers_obj.all_outliers(":", seasonal=21, avg_flag=True)

Hardware
Computer: Asus G14
CPU: Ryzen 9 4900HS (3.00 GHz, no turbo boost disabled)
RAM: 16 GB
Drive: 1 TB m.2 NVMe SSD

Output
DataFrame size (rows x cols) = 11 x 113
Execution time mean: 7.23s
Number of runs: 3
Std dev: +/-0.018s