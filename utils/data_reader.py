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