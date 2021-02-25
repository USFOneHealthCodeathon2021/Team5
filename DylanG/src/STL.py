import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.seasonal import STL
import time


"""
Handles generating the STL models and extracting residuals
"""
class Outliers:
	def __init__(self, path, norm_start=124, start_date='1-4-2003', freq="D"):
		self.df = pd.read_csv(path)		
		self.norm = self.df[self.df.columns[norm_start:]]
		self.index = pd.date_range(start_date, periods=self.norm.shape[1], freq=freq)


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
	def get_day(self, iloc, day_start, day_end=None, seasonal=7, robust=False, taxon_depth='family_tax', with_date=True):
		if day_start == ":":
			day_start = 0
		if day_end == ":":
			day_end = self.norm.shape[1]
		taxon = self.df[taxon_depth].iloc[iloc]
		bacteria = pd.Series(self.norm.iloc[iloc].values, index=self.index, name=taxon)
		stl = STL(bacteria, seasonal=seasonal, robust=robust)
		model = stl.fit()
		residuals = model.resid
		residuals.name = taxon
		if day_end:
			day_resid = residuals[day_start:day_end]
		else:
			day_resid = residuals[day_start:day_start+1]
		if not with_date:
			day_resid = day_resid.reset_index(drop=True)
		return day_resid


	"""
	Summary:
		Generate STLs for an entire dataset (using get_day), obtaining the decomposed remainder(s) for a given bacteria based from day_start to day_end
	Parameters:
		day_start = day to begin grabbing from (0 indexed, follows Python indexing)
		day_end = day to end grabbing at. If None, just grab the day at day_start (0 indexed, follows Python indexing)
		seasonal = STL seasonal window size
		robust = STL robust
		taxon_depth = taxon to use for reporting
		smallest = number of smallest bacterial remainders to grab for each day
		largest = number of largest bacterial remainders to grab for each day
		avg_flag = append the average value for each day to the final dataframe
	returns:
		A dataframe where rows are the dates and indices are the bacteria (given based on taxon_depth). Each cell indicates the remainder for a specific bacteria (index)
		based on a specific day (column). Averages can optionally be added and are calculated based on the values within a column.
	"""
	def all_outliers(self, day_start, day_end=None, seasonal=7, robust=False, taxon_depth='family_tax', smallest=5, largest=5, avg_flag=False):
		if day_start == ":":
			day_start = 0
		if day_end == ":":
			day_end = self.norm.shape[1]
		cols = self.index[day_start:day_end]
		cols = [str(date) for date in cols.date]
		resid_mat = np.zeros([len(self.df), len(cols)])
		index = []
		for i in range(len(self.norm)):
			day_i_resids = self.get_day(i, day_start, day_end, seasonal, robust, taxon_depth, False)
			index.append(day_i_resids.name)
			resid_mat[i, :] = day_i_resids
		resid_df = pd.DataFrame(resid_mat, index=index)
		resid_df.sort_values(by=[i for i in range(len(cols))], inplace=True)
		resid_df.columns = cols
		largest = resid_df.iloc[-largest:]
		smallest = resid_df.iloc[:smallest]
		avgs = resid_df.mean()
		outliers = pd.concat([smallest, largest])
		if avg_flag:
			outliers.loc["mean"] = avgs 
		return outliers


	"""
	Convenience STL plotting. Optionally overide the object frequency
	"""
	def plot(self, iloc, seasonal=7, freq=None, robust=False, taxon_depth='family_tax'):
		index = self.index
		taxon = self.df[taxon_depth].iloc[iloc]
		if freq:
			index = pd.date_range(self.index.values[0], periods=self.norm.shape[1], freq=freq)
		bacteria = pd.Series(self.norm.iloc[iloc].values, index=index, name=taxon)
		stl = STL(bacteria, seasonal=seasonal, robust=robust)
		model = stl.fit()
		fig = model.plot()
		plt.show()


#Plot setup for pretty output
register_matplotlib_converters()
sns.set_style('darkgrid')
plt.rc('figure', figsize=(16, 12))
plt.rc('font', size=13)

start = time.perf_counter()
out = Outliers("../../Austin_data.csv")
result = out.all_outliers(":", seasonal=21, avg_flag=True)
print(result)
print(result.shape)
delta = time.perf_counter() - start
print(f"Execution time: {delta:.5f}s")