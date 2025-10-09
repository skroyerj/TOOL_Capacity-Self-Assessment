import plotly.graph_objects as go
import plotting_data

def time_series_df(dataframe, question):
    """ Create a dataframe for each question to see progression over time. """

    time_series = dataframe.groupby("Anon_ID")[question].value_counts(normalize=True).unstack().fillna(0) * 100
    return time_series
