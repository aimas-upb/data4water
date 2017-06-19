import pandas as pd
import numpy as np
import os

DATASET_ROOT_FOLDER = "../AMR-data"

def read_dataset():
    """
    Returns the AMR dataset as a set of pandas dataframes containing the data for each consumer
    :return: a list of pandas datasets, one for each consumer
    """
    df_list = []

    for filename in os.listdir(DATASET_ROOT_FOLDER):
        filepath = DATASET_ROOT_FOLDER + os.path.sep + filename
        df = pd.read_csv(filepath, header = None, names = ['date', 'h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9',
                                                           'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19',
                                                           'h20', 'h21', 'h22', 'h23'],
                         parse_dates=[1])
        df_list.append(df)

    return df_list

def get_extended_timeseries(df):
    """
    Get the concatenated 'all-time' timeseries for a consumer.
    :param df: The dataframe containing the data for that consumer
    :return: A pandas Timeseries object containing the concatenated timeseries
    """
    hours = range(24)
    hour_cols = map(lambda x : "h" + str(x), hours)

    names = []
    values = []
    for index, row in df.iterrows():
        names = names + map(lambda x: str(row['date']) + " " + str(x) + ":00:00Z", hours)
        values = values + [row[col] for col in hour_cols]

    # print(names)
    # print(values)
    # print(len(values))

    big_series = pd.Series(values, index = names)
    return big_series