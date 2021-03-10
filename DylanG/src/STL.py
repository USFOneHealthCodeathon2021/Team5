# Author: Dylan Gallinson
# Date: 2/24/2021
# Data File: ../../Austin_data.csv

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.seasonal import STL
import multiprocessing as mp
from multiprocessing import Pool
import time


"""
Handles generating the STL models and extracting residuals, finding high/low outliers by day (or whatever unit is specified by freq)
"""
class Outliers:
	"""
	*Parameters:
		path [str] = Path to CSV data containing time-series microbe abundance data
		start_day [int] = Day (or whatever was specified in freq) to begin extraction from
		until_end [bool, default False] = If True, extract all time points from start_day until the end
		norm_start [int, default 124] = Column where the count data being (assumed the count data are contiguous)
		start_date [str, default '1-4-2003'] = Beginning date of the time-series
		freq [str, default 'D'] = Frequency of the time-series (e.g. "D", "W", "M" for day, week, and month respectively)
		seasonal [int, default 21] = Seasonal window size to be used in STL
		robust [bool, default False] = Whether or not the STL is robust to outliers
		taxon_depth [str, default 'taxa_string'] = The column name representing the depth of bacterial identification to be used in reporting (phylum, class, order, etc)
	*Most defaults were set for the inerpolated Austin.csv dataset
	"""
	def __init__(self, path, start_day, until_end=False, norm_start=124, start_date='1-4-2003', freq="D", seasonal=21, robust=False, taxon_depth='taxa_string'):
		self.start_day = start_day
		self.until_end = until_end
		self.seasonal = seasonal
		self.robust = robust
		self.taxon_depth = taxon_depth
		self.df = pd.read_csv(path)
		self.freq = freq
		self.norm = pd.concat([self.df[taxon_depth], self.df[self.df.columns[norm_start:]]], axis=1)
		self.index = pd.date_range(start_date, periods=self.norm.shape[1]-1, freq=freq)


	"""
	Summary:
		For a given row, generate an STL and grab data at self.start_day
		(and through the end of the remaining days if self.until_flag is True)
	Parameters:
		norm_counts [list] = A 2D list where each inner list represents a row of counts for
					  a bacteria over a period of time, and norm_counts[n][0] is an identifier
	Returns:
		A 2D list containing residuals for the specified days that can be converted to a DataFrame
		where the index is the taxon and the columns represent the date of the residuals
	"""
	def gen_STL(self, norm_counts):
		taxon = norm_counts[0]
		bacteria = pd.Series(norm_counts[1:], index=self.index)
		stl = STL(bacteria, seasonal=self.seasonal, robust=self.robust)
		model = stl.fit()
		residuals = model.resid
		residuals.name = taxon
		day_resids = self.__process_day_range(residuals, self.start_day, self.until_end)
		return day_resids


	"""
	Summary:
		Generate STLs using gen_STL() (parallel processing used to speed up STL generation), and extract
		the nlarge largest residuals and the nsmall smallest residuals
	Parameters:
		by [int, default None] = Indicates which date to use for outlier extraction when multiple days are extracter
		as_date [bool, default False] = Controls the column name format, where False uses freq_n (e.g. day_1) annd Trye uses actual dates (e.g. 2003-04-25)
		nlarge [int, default 5] = The number of largest residual values to be extracted
		nsmall [int, default 5] = The number of smallest residual values to be extracted
		cores [int, default max] = The number of cores to use for parallel processing
	Returns:
		A DataFrame containing the highest and lowest residuals for a specified date, where the first column represents the
		taxon (depth specified by self.taxon_depth), and the remaining columns show the residuals organized by date ascending
	"""
	def outliers(self, by=None, as_date=False, nlarge=5, nsmall=5, cores="max"):
		if __name__ == "__main__":
			if cores == "max":
				cores = mp.cpu_count()
			with Pool(cores) as pool:
				day_resids = pool.map(self.gen_STL, self.norm.values.tolist())
			day_frame = pd.DataFrame(day_resids).reset_index()
			dates = self.__process_day_range(self.index, self.start_day, self.until_end)
			day_frame.columns = self.__process_col_names(self.start_day, self.until_end, as_date)
			return self.__get_outliers(day_frame, by, nlarge, nsmall)


	"""
	Convenience method to process the start_day/until day notation
	"""
	def __process_day_range(self, container, day, until_end):
		if until_end or day == -1:
			return container[day:]
		else:
			return container[day:day+1]


	"""
	Convenience method to handle generating column names for DataFrame containing residuals for n days.
	Using as_date=True generates actual dates as columns names whereas as_date=False uses freq_n, where
	n is iterated from start_date until the final freq (day, week, etc)
	"""
	def __process_col_names(self, day, until_end, as_date):
		freq_key = {
			"D": "day",
			"W": "week",
			"M": "month",
			"Y": "year"
		}
		if as_date:
			dates = self.__process_day_range(self.index, day, until_end)
			col_names = [str(date) for date in dates.date]
		else:
			total_len = len(self.norm.columns)
			sub_len = len(self.__process_day_range(self.norm.columns, day, until_end))
			start = total_len - sub_len
			col_names = [f"{freq_key[self.freq]}_{i}" for i in range(start, total_len)]
		return ["taxon"] + col_names


	"""
	Convenience method to obtain the nlarge and nsmall residuals. Only obtains these largest/smallest
	values in the column specified using "by"
	"""
	def __get_outliers(self, day_frame, by, nlarge, nsmall):
		if not by:
			by = -1
		self.by = by
		self.nlarge = nlarge
		self.nsmall = nsmall
		sort_col = day_frame.columns[by]
		largest = day_frame.nlargest(nlarge, sort_col)
		smallest = day_frame.nsmallest(nsmall, sort_col)
		return pd.concat([smallest, largest])


	def split_processed(self, processed, small_ascend=True, large_ascend=True):
		small = processed[:self.nsmall]
		small = small.sort_values(by=small.columns[self.by], ascending=small_ascend)
		large = processed[self.nsmall:]
		large = large.sort_values(by=large.columns[self.by], ascending=large_ascend)
		return small, large



	"""
	Summary:
		Convenience STL plotting. Optionally overide the object frequency
	Parameters:
		iloc [int] = The row to plot the STL decomposition of (0 indexed)
		freq [str, default None] = Override self.freq
		seasonal [int, default None] = Override self.seasonal (must be odd and >=7)
		robust [bool, default None] = Override self.robust
	Returns:
		None, shows the STL plot of the specified iloc
	"""
	def plot(self, iloc, freq=None, seasonal=None, robust=None):
		if not seasonal:
			seasonal = self.seasonal
		if not robust:
			robust = self.robust
		if not freq:
			index = self.freq
		else:
			index = pd.date_range(self.index.values[0], periods=self.norm.shape[1], freq=freq)
		index = self.index
		taxon = self.df[self.taxon_depth].iloc[iloc]
		bacteria = pd.Series(self.norm.iloc[iloc].values[1:], index=index, name=taxon)
		stl = STL(bacteria, seasonal=self.seasonal, robust=self.robust)
		model = stl.fit()
		fig = model.plot()
		plt.show()


	"""
	Summary:
		Convenience plotting of a row (specified by process_row)
	Parameters:
		processed_row [pd.Series] = Expects a row from the results of self.outliers()
		save_mode [bool, default False] = False shows the plot to screen, True adds the figure to plot without displaying it (used for self.save_processed_figs)
	Return:
		None, adds the figure to matplotlib's plot and shows it (if save_mode=False)
	"""
	def plot_processed(self, processed_row, save_mode=False):
		taxon = processed_row["taxon"]
		row_i = self.df[self.df[self.taxon_depth] == taxon].index.values[0]
		bacteria = pd.Series(self.norm.loc[row_i].values[1:], index=self.index.values, name=taxon)
		stl = STL(bacteria, seasonal=self.seasonal)
		model = stl.fit()
		fig = model.plot()
		if not save_mode:
			plt.show()
		

	"""
	Summary:
		Saves all rows in the output of self.outliers() as PNGs
	Parameters:
		processed [pd.DataFrame] = Dataframe output from self.outliers()
		output_dir [str, default None] = Output directory to save images in (do not add a trailing slash)
		small_ascend [bool, default True] = If the nsmall smallest outliers should be saved in ascending or descending order
		large_ascend [bool, default True] = If the nlarge largest outliers should be saved in ascending or descending order
		ftype [str, default svg] = Filetype to save the images as (e.g. svg, png, jpg)
		dpi [int, default 1200] = Image pixel density in dots per inch (higher means sharper image)
	Return:
		None, saves all outliers in ascending/descending order. Smallest outliers are saved as "low_n.ftype", where "low_1.ftype"
		represents the highest (descending) or lowest (ascending) small outlier. Similarly, saves the highest outliers as
		"high_n.ftype" where "high_1.ftype" is the highest (descending) or lowest (ascending) large outlier. The STL from
		ALL time points, not just from start_day, is generated through plot_processed.
	"""
	def save_processed_figs(self, processed, output_dir=None, small_ascend=True, large_ascend=True, ftype="svg", dpi=1200):
		resid_col = processed.columns.values[self.by]
		small, large = self.split_processed(processed, small_ascend=small_ascend, large_ascend=large_ascend)
		print(f"Saving {self.nsmall} lowest outliers in {'ascending' if small_ascend else 'descending'} order...")
		for i in range(small.shape[0]):
			row = small.iloc[i]
			fname = f"low_{i+1}.{ftype}"
			if output_dir:
				fname = f"{output_dir}/{fname}"
			print(f"Saving {row['taxon']} as {fname} [{row[resid_col]}]")
			self.plot_processed(row, True)
			plt.savefig(fname, format=ftype, dpi=dpi)
		
		print("Done!\n")
		print(f"Saving {self.nlarge} highest outliers in {'ascending' if small_ascend else 'descending'} order...")
		
		for i in range(large.shape[0]):
			row = large.iloc[i]
			fname = f"high_{i+1}.{ftype}"
			if output_dir:
				fname = f"{output_dir}/{fname}"
			print(f"Saving {row['taxon']} as {fname} [{row[resid_col]}]")
			self.plot_processed(row, True)
			plt.savefig(fname, format=ftype, dpi=dpi)

		print("Done!")


#Plot setup for pretty output
register_matplotlib_converters()
sns.set_style('darkgrid')
plt.rc('figure', figsize=(16, 12))
plt.rc('font', size=13)



# It is recommended that using this class is wrapped in an if statement to ensure
# that the executing namespace is __main__. An example use placed in this block is as follows:
# out = Outliers("../../Austin_data.csv", start_day=-5, until_end=True)

# out = Outliers("../../Austin_data.csv", start_day=-5, until_end=True)
# outliers = out.outliers()
# outliers.to_csv("../Figures/outliers.csv", index=False)
# out.save_processed_figs(outliers, small_ascend=False, output_dir="../Figures/STLs")

# This grabs the 5 highest/lowest outliers by the last day, stores the last 5 days of
# data in a DataFrame, saves this to a CSV, and then saves the entire STLs corresponding
# to these outliers as SVG files (all files saved to a Figures directory).
if __name__ == "__main__":
	pass