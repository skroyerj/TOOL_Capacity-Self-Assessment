import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


def butterfly(counted_df):

    """ Plot modified from ethanlees on Stackoverflow: https://stackoverflow.com/a/69976552"""

    category_names = counted_df.columns.tolist()
    questions = counted_df.index.tolist()

    labels = list(questions)
    data = counted_df.to_numpy()
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

def stacked_area(counted_df,question):
    """ Create a stacked area chart with plotly. Use a counted dataframe as input. """

    # Colors from https://coolors.co/8d2a2a-c74444-ee6d6d-7a9acd-436db1-325285
    # #8d2a2a, #c74444, #ee6d6d, #7a9acd, #436db1, #325285

    weeks = counted_df.columns.tolist()
    index = counted_df.index.tolist()
    x = list(weeks)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=counted_df.iloc[0,:].to_numpy(),
        name=index[0],
        text=index[0],
        hoverinfo='y+text',
        mode='lines',
        line=dict(width=0.5, color='#8d2a2a'),
        stackgroup='one', # define stack group
        groupnorm='percent' # sets the normalization for the sum of the stackgroup
    ))
    fig.add_trace(go.Scatter(
        x=x, y=counted_df.iloc[1,:].to_numpy(),
        name=index[1],
        text=index[1],
        hoverinfo='y+text',
        mode='lines',
        line=dict(width=0.5, color='#c74444'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=counted_df.iloc[2,:].to_numpy(),
        name=index[2],
        text=index[2],
        hoverinfo='y+text',
        mode='lines',
        line=dict(width=0.5, color='#ee6d6d'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=counted_df.iloc[3,:].to_numpy(),
        name=index[3],
        text=index[3],
        hoverinfo='y+text',
        mode='lines',
        line=dict(width=0.5, color='#7a9acd'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=counted_df.iloc[4,:].to_numpy(),
        name=index[4],
        text=index[4],
        hoverinfo='y+text',
        mode='lines',
        line=dict(width=0.5, color='#436db1'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=counted_df.iloc[5,:].to_numpy(),
        name=index[5],
        text=index[5],
        hoverinfo='y+text',
        mode='lines',
        line=dict(width=0.5, color='#325285'),
        stackgroup='one'
    ))

    fig.update_layout(
    title = question,
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[0, 100],
        ticksuffix='%'))
    # fig.update_layout(yaxis_range=(0, 100))
    
    fig.show()

    return fig
