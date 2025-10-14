import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


def butterfly(dataframe):

    """ Plot modified from ethanlees on Stackoverflow: https://stackoverflow.com/a/69976552"""

    category_names = dataframe.columns.tolist()
    questions = dataframe.index.tolist()

    labels = list(questions)
    data = dataframe.to_numpy()
    data_cum = data.cumsum(axis=1)
    middle_index = data.shape[1]//2
    offsets = data[:, range(middle_index)].sum(axis=1) # Always on
    # offsets = offsets + data[:, middle_index]/2 # uncomment if odd number of categories
    # offsets = offsets * 0  # Commenting enables offsets

    # Color Mapping
    category_colors = plt.get_cmap('coolwarm_r')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot Bars
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths - offsets
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

    # Add Zero Reference Line
    ax.axvline(0, linestyle='--', color='black', alpha=.25)

    # X Axis
    ax.set_xlim(-90, 90)
    ax.set_xticks(np.arange(-90, 91, 10))
    ax.xaxis.set_major_formatter(lambda x, pos: str(abs(int(x))))

    # Y Axis
    ax.invert_yaxis()

    # Remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Ledgend
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='small')

    # Set Background Color
    fig.set_facecolor("#FFFFFF")

    return fig, ax


# ----------------------------------------------------------
# Stacked Area Chart
# ----------------------------------------------------------

def stacked_area(dataframe):

    category_names = dataframe.columns.tolist()
    questions = dataframe.index.tolist()
    x = list(questions)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=dataframe.iloc[:,1].to_numpy(),
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one' # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=x, y=dataframe.iloc[:,2].to_numpy(),
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=dataframe.iloc[:,3].to_numpy(),
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'
    ))

    fig.update_layout(yaxis_range=(0, 100))
    fig.show()

    return fig
