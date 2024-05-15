#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html


# Directory where the CSV files are located
directory = "C:/Personal/Esther/Project/Dataset"

# List to store all dataframes
dfs = []

# Looping through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Load the CSV file into a dataframe
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        # Append the dataframe to the list
        dfs.append(df)


# Combining all dataframes into a single dataframe
combined_df = pd.concat(dfs, ignore_index=True)


# Displaying the first few rows of the combined dataframe
print(combined_df.head())


# Displaying general information about the dataset
print(combined_df.info())


# Checking for missing values
missing_values = combined_df.isnull().sum()
print("Missing Values:")
print(missing_values)


# Drop columns with a large number of missing values
combined_df.drop(columns=['Crime ID', 'Last outcome category', 'Context'], inplace=True)

# Fill missing values in longitude and latitude with means
combined_df['Longitude'].fillna(combined_df['Longitude'].mean(), inplace=True)
combined_df['Latitude'].fillna(combined_df['Latitude'].mean(), inplace=True)

# Fill missing values in LSOA code and name with mode
combined_df['LSOA code'].fillna(combined_df['LSOA code'].mode()[0], inplace=True)
combined_df['LSOA name'].fillna(combined_df['LSOA name'].mode()[0], inplace=True)

# Verify if missing values are handled
missing_values_after = combined_df.isnull().sum()
print("Missing Values After Handling:")
print(missing_values_after)


# Checking the summary statistics of numerical columns
print(combined_df.describe())

# Checking the summary statistics of categorical columns
print(combined_df.describe(include=['object']))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    # Title
    html.H1("Crime Data Dashboard"),
    
    # Scatter plot
    dcc.Graph(
        id='crime-scatter-plot',
        figure=px.scatter(combined_df, x="Longitude", y="Latitude", hover_name="Crime type", color="Crime type").update_layout(title="Crime Incidents Scatter Plot")
    ),
    
    # Histogram
    dcc.Graph(
        id='crime-histogram',
        figure=px.histogram(combined_df, x="Crime type").update_layout(title="Crime Types Histogram")
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




