import pandas as pd
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
	Generate an STL at the given row number and grab the n largest/smallest values from the remainder
	"""
	def get_outliers(self, iloc, seasonal=7, robust=False, taxon_depth='family_tax', smallest=5, largest=5, avg_flag=False):
		taxon = self.df[taxon_depth].iloc[iloc]
		bacteria = pd.Series(self.norm.iloc[iloc].values, index=self.index, name=taxon)
		stl = STL(bacteria, seasonal=seasonal, robust=robust)
		model = stl.fit()
		residuals = model.resid
		outliers = pd.Series(pd.concat([residuals.nlargest(largest), residuals.nsmallest(smallest)]), name=taxon).reset_index(drop=True)
		if avg_flag:
			outliers.loc[smallest + largest] = residuals.mean()
		return outliers


	"""
	Get all n largerst/smallest remainders from each bacerial signataure and return them as a combined dataframe with the defined "taxon_depth"
	as the column headers
	"""
	def all_outliers(self, seasonal=7, robust=False, taxon_depth='family_tax', smallest=5, largest=5, avg_flag=False):
		series = []
		for i in range(len(self.norm)):
			series.append(self.get_outliers(i, seasonal, robust, taxon_depth, smallest, largest, avg_flag))
		print(pd.concat(series, axis=1))


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



register_matplotlib_converters()
sns.set_style('darkgrid')
plt.rc('figure', figsize=(16, 12))
plt.rc('font', size=13)

start = time.perf_counter()
out = Outliers("../../Austin_data.csv")
out.all_outliers()
delta = time.perf_counter() - start
print(f"Execution time: {delta:.5f}s")