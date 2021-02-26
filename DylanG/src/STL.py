import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.seasonal import STL
from multiprocessing import Pool
import time


"""
Handles generating the STL models and extracting residuals
"""
class Outliers:
	def __init__(self, path, norm_start=124, start_date='1-4-2003', freq="D", seasonal=21, robust=False, taxon_depth='taxa_string'):
		self.seasonal = seasonal
		self.robust = robust
		self.taxon_depth = taxon_depth
		self.df = pd.read_csv(path)
		self.freq = freq
		self.norm = pd.concat([self.df[taxon_depth], self.df[self.df.columns[norm_start:]]], axis=1)
		self.index = pd.date_range(start_date, periods=self.norm.shape[1]-1, freq=freq)


	"""
	Summary:
		For a given row, generate an STL and grab days from day_start to day_end.
	Parameters:
		iloc=row num (0 indexed)
		day_start = day to begin grabbing from (0 indexed, follows Python indexing)
		day_end = day to end grabbing at. If None, just grab the day at day_start (0 indexed, follows Python indexing)
		seasonal = STL seasonal window size
		robust = STL robust
		taxon_depth = taxon to use for reporting
		with_date = use date for returned Series index
	Returns:
		A series showing the remainder for bacterial signatures in row=iloc at dates start_date:end_date.
		Series has name=bacteria (to the defined taxon_depth) and, if with_date=True, indexed according to date
	"""
	def gen_STL(self, series):
		taxon = series[0]
		bacteria = pd.Series(series[1:].values, index=self.index)
		stl = STL(bacteria, seasonal=self.seasonal, robust=self.robust)
		model = stl.fit()
		residuals = model.resid
		residuals.name = taxon
		return residuals


	def outliers(self, day, until_end=False, by=None, as_date=False, nlarge=5, nsmall=5):
		day_resids = []
		for i in range(len(self.norm)):
			row = self.norm.iloc[i]
			bacteria_sample = self.gen_STL(row)
			day_sample = self.__process_day_range(bacteria_sample, day, until_end)
			day_resids.append(day_sample)
		day_frame = pd.DataFrame(day_resids).reset_index()
		dates = self.__process_day_range(self.index, day, until_end)
		day_frame.columns = self.__process_col_names(day, until_end, as_date)
		return self.__get_outliers(day_frame, by, nlarge, nsmall)
		# with Pool(8) as pool:
		# 	result = pool.map(self.gen_STL, self.norm.itertuples(name=False))


	def __process_day_range(self, container, day, until_end):
		if until_end or day == -1:
			return container[day:]
		else:
			return container[day:day+1]


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


	def __get_outliers(self, day_frame, by, nlarge, nsmall):
		if not by:
			by = -1
		sort_col = day_frame.columns[by]
		largest = day_frame.nlargest(nlarge, sort_col)
		smallest = day_frame.nsmallest(nsmall, sort_col)
		return pd.concat([smallest, largest])


	"""
	Convenience STL plotting. Optionally overide the object frequency
	"""
	def plot(self, iloc, freq=None):
		index = self.index
		taxon = self.df[self.taxon_depth].iloc[iloc]
		if freq:
			index = pd.date_range(self.index.values[0], periods=self.norm.shape[1], freq=freq)
		bacteria = pd.Series(self.norm.iloc[iloc].values, index=index, name=taxon)
		stl = STL(bacteria, seasonal=self.seasonal, robust=self.robust)
		model = stl.fit()
		fig = model.plot()
		plt.show()


	def plot_processed(self, processed_row, save_mode=False):
		taxon = processed_row["taxon"]
		row_i = self.df[self.df[self.taxon_depth] == taxon].index.values[0]
		bacteria = pd.Series(self.norm.loc[row_i].values[1:], index=self.index.values, name=taxon)
		stl = STL(bacteria, seasonal=self.seasonal)
		model = stl.fit()
		fig = model.plot()
		if not save_mode:
			plt.show()
		

	def save_processed_figs(self, processed):
		for i in range(len(processed)):
			row = processed.iloc[i]
			fname = f"{i+1}.png"
			print(f"Saving {row['taxon']} as {fname} [{row['residual']}]")
			self.plot_processed(row, True)
			plt.savefig(fname)


#Plot setup for pretty output
register_matplotlib_converters()
sns.set_style('darkgrid')
plt.rc('figure', figsize=(16, 12))
plt.rc('font', size=13)


pd.set_option('display.max_columns', None)


start = time.perf_counter()

out = Outliers("../../Austin_data.csv")
result = out.outliers(-2, until_end=True)

delta = time.perf_counter() - start
print(f"Execution time: {delta:.5f}s")