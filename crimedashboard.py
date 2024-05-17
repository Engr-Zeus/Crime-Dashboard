import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go
import plotly.express as px
import warnings
import dash
from dash import dcc, html

# Suppress FutureWarning for chained assignment
warnings.simplefilter(action='ignore', category=FutureWarning)


def create_dash_app():
    # Directory where the CSV files are located
    directory = "Dataset"

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

    # Checking for missing values
    missing_values = combined_df.isnull().sum()

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

    return app


# Run the app
if __name__ == '__main__':
    app = create_dash_app()
    app.run_server(host='0.0.0.0', port=8050, debug=True)
