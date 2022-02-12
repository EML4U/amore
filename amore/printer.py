from pandas import DataFrame
from IPython.display import display

class Printer():
    
    def ipython_display(self, value):
        display(value)
    
    def get_dataframe_markdown(self, df, tablefmt='pipe', float_as_integer=False):
        # Formats: https://pypi.org/project/tabulate/
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html
        if float_as_integer:
            return df.to_markdown(tablefmt=tablefmt, floatfmt=".0f")
        else:
            return df.to_markdown(tablefmt=tablefmt)
    
    def get_dataframe_with_sums(self, dy_ds_lt):
        df = self.get_dataframe(dy_ds_lt)
        df['Sum'] = df.sum(axis=1)
        df.loc['Sum']= df.sum()
        return df

    def get_dataframe(self, dy_ds_lt):
        df = DataFrame(index=sorted(dy_ds_lt[next(iter(dy_ds_lt))].keys()), columns=sorted(dy_ds_lt.keys()))
        for year in dy_ds_lt.keys():
            for star in dy_ds_lt[year].keys():
                df.at[star,year] = len(dy_ds_lt[year][star])
        return df