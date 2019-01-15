from binary_reader.dataframes import *
from configuration import PROJECT_PATH

def get_csv_filename(df_name):
    return PROJECT_PATH + "multi_tracking/results/{0}/{1}/{2}/{0}_{1}_{2}_{3}.csv".format(FILL, RUN, RECO, df_name)


def save_dataframe(df_name, dataframe=None):
    if dataframe is None:
        dataframe = DATAFRAMES[df_name]
    csv_filename = get_csv_filename(df_name)
    dataframe.to_csv(csv_filename)