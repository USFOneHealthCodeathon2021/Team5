Overview
This script takes as input a csv file containing abundance counts for airborne microbes and yields outliers via Seasonal-Trend decomposition using LOESS (STL).
This is accomplished by running STL on a row (which should indicate an abundance time-series for a given identified microbe), iterating this process over
the entire dataset, and extracting the residuals at a given time point (or over a range of time points). At a specified time point, the n highest and n lowest
residuals (representing potential outliers) are extracted.

Dependencies
 -Python 3 (run on 3.9.1)
 -pandas (run on 1.2.2)
 -numpy (run on 1.20.1)
 -matplotlib (run on 3.3.4)
 -statsmodels (run on 0.12.2)

Usage
>>#Obtain the 5 largest and 5 smallest microbial remainders for the final day of the dataset, showing the last 3 days of residuals
>>import SLT
>>out = SLT.Outliers(path_to_csv, -3, until_end=True)
>>outliers = out.outliers()
>>if __name__ == "__main__":
>>  print(outliers)
                                                                              taxon                 day_111      day_112     day_113
222   Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Nocardiaceae;sf_1;1805              188.350309   219.656049 -604.764231
989   Bacteria;Firmicutes;Clostridia;Unclassified;Unclassified;sf_7;4216                         -41.203199  -155.150039 -277.882589 
477   Bacteria;Cyanobacteria;Cyanobacteria;Chloroplasts;Chloroplasts;sf_5;5006                   -35.570980  -149.450269 -270.019115
484   Bacteria;Cyanobacteria;Cyanobacteria;Chloroplasts;Chloroplasts;sf_5;5182                   -34.620290  -144.882724 -262.431377 
1289  Bacteria;Proteobacteria;Alphaproteobacteria;Sphingomonadales;Sphingomonadaceae;sf_1;6663   -36.183176  -141.948040 -256.757691 
1755  Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacteriales;Enterobacteriaceae;sf_1;9337  12.254567    38.118430   65.442693 
539   Bacteria;Firmicutes;Bacilli;Bacillales;Bacillaceae;sf_1;3277                                10.429037    34.226302   59.658730 
238   Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Propionibacteriaceae;sf_1;2002        7.673082    32.333474   57.237908 
160   Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Micrococcaceae;sf_1;1529             -2.261048    23.687304   55.386548 
599   Bacteria;Firmicutes;Bacilli;Bacillales;Bacillaceae;sf_1;3715                                 7.121895    24.181345   42.686451 

--Execution time--
Input
input file: Austin_data.csv
Input file size: 4.48 MB
Input file rows x cols: 1994 x 237
Input file processed rows x cols: 1993 x 113
Outliers instantiation: Outliers("../../Austin_data.csv", -10, until_end=True)
all_outliers call: outliers_obj.outliers()
Execution time function: time.perf_counter()

Hardware
Computer: Asus G14
CPU: Ryzen 9 4900HS (16 logical cores, 3.00 GHz boost up to 4.20 GHz)
RAM: 16 GB
Drive: 1 TB m.2 NVMe SSD

Output
DataFrame size (rows x cols) = 10 x 11
Execution time mean: 3.29s
Std dev: +/-0.0317s
Number of runs: 10

Scaling
~Preliminary analysis indicates that this is linearly extensible 
Justifiction: I increased the dataset by a factor of 3x for rows by copy/pasting the entire spreadsheet, appending it 3 times.
	      For increasing columns, I copy/pasted just the normalized counts (right-side pasting).
	      Both row and col pasting yielded almost identical results by inspecting the per-core and main core times.
	      For both, STL times were ~0.4s-0.5s per core, total time was ~8s for both
	      *NOTE: big cols had more variablity in per-core STL compute time (may be due to background processes)
