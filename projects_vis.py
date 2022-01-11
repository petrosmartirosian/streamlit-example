import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime

# Bubble sort needed for sorting 
# all lists in a dictionary based on one list
def special_sort(data, key):
    n = len(data[key])
    for i in range(n-1):
    # range(n) also work but outer loop will
    # repeat one time more than needed.
         # Last i elements are already in place
        for j in range(0, n-i-1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if data[key][j] > data[key][j + 1]:
                for x in data.keys():
                    data[x][j], data[x][j + 1] = data[x][j + 1], data[x][j]
    return data

# Function for creating the graphs
def projects_scatter_plot(data, xaxis, yaxis, start, stop, option):
    actual = {i: [] for i in data.keys()} # duplicates data dictionary for sorting
    
    # iterates through each element
    for i in range(len(data[xaxis])):
        # if element has an actual input for the date
        if data[xaxis][i] and data[yaxis][i]:
            # if the date is within the start and stop dates
            if (datetime.strptime(data[xaxis][i][0:10], '%Y-%m-%d') >= start and
            datetime.strptime(data[xaxis][i][0:10], '%Y-%m-%d') <= stop):
                # And if it is one of the filters selected( or all)
                if "All" in option or data[yaxis][i] in option:
                    # Append all aspects to dictionary
                    for j in actual.keys():
                        actual[j].append(data[j][i])
    # Bubble sort everything
    actual = special_sort(actual, xaxis)
    # turn data into dataframe so I can show all names on hover
    df = pd.DataFrame(actual)
    # plotting calls
    fig = px.strip(df, x=xaxis, y=yaxis, hover_data=df.keys())
    graphname = xaxis + ' vs ' + yaxis
    fig.update_layout(template='simple_white',  width=800, height=800, title=graphname,
                  legend=dict(title=graphname, itemclick='toggle', itemsizing='constant', traceorder='normal',
                  bgcolor='rgba(0,0,0,0)', x=1),
                  xaxis=dict(showticklabels=True, ticks='outside', type='category')
                 )
    fig.update_yaxes(rangemode="nonnegative")
   
    return fig
