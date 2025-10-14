import plotly.graph_objects as go
# import plotting_data
import pandas as pd
from functools import reduce

def time_series_df(dfs, question, index_by, to_excel=False):
    """ Create a dataframe for each question to see progression of answers over time. """

    week_dfs = []

    # time_series = dataframe.groupby(index_by)[question].value_counts(normalize=True).unstack().fillna(0)
    for week_name, df in dfs.items():
        week_dfs.append(df[[index_by, question]].rename(columns={question: week_name}))

    time_series = reduce(lambda left, right: pd.merge(left, right, on=index_by, how="outer"), week_dfs)#.fillna(0)

    time_series = time_series.sort_values(index_by).reset_index(drop=True)

    if to_excel:
        time_series.to_excel("data/combined_qs/" + str(question)+".xlsx", index=False)

    return time_series
