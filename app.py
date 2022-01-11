# TODO continue studying this API https://docs.streamlit.io/en/stable/api.html#display-charts
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json_lines
sns.set()
from projects_vis import *
from notion_api import *
from datetime import datetime
import re

# Caches automatically
@st.cache
def load_data():
    nsync = NotionSync()
    data = nsync.query_databases()
    info = nsync.get_important_information(data)
    return info
# Gets data from database
info = load_data()

st.title("Project data")
# Set up: load and set up the data and write loading message
data_load_state = st.text('Loading data...')
data_load_state.text('Loading data...done!')
# creating list of options for x axis and y axis
xoptions = []
yoptions = []
# currently the x axis only consists of dates and the y axis consists of all other options
for i in info.keys():
    if re.search('date', i, re.IGNORECASE):
        xoptions.append(i)
    else:
        yoptions.append(i)
# drop downs for selecting the x and y axis, currently defaults to completed dates vs status
xaxis = st.selectbox( 'Select x axis', (xoptions))
yaxis = st.selectbox( 'Select y axis', (yoptions))

# Finding valid date ranges(some dates are not filled out so i need to check for actual dates)
minindex = 0
maxindex = 0
for i in range(len(info[xaxis])):
    if info[xaxis][i]:
        minindex = i
        break
for i in range(len(info[xaxis])):
    if info[xaxis][len(info[xaxis]) - (1 + i)]:
        maxindex = len(info[xaxis]) - (1 + i)
        break
mindate = info[xaxis][minindex]
maxdate = info[xaxis][maxindex]
# 2 way slider for dates
slider_range = st.slider("Select Date Range",
  value = [datetime.strptime(mindate[0:10], '%Y-%m-%d'), datetime.strptime(maxdate[0:10], '%Y-%m-%d')]
)

# multi option bar for selecting multile filters for the y axis
# if nothing selected, it defaults to all
options = []
for i in info[yaxis]:
    if i not in options and i != None:
        options.append(i)
option = st.multiselect( 'select specific options?', (options))
option = option if len(option) else ["All"]

st.write('You selected:', option) # can be removed if you want

project_events = projects_scatter_plot(info, xaxis, yaxis, slider_range[0], slider_range[1], option)
st.write(project_events)
