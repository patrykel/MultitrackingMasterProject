import pandas as pd

from common.track_results_dataframe import get_result_csv_filename
from configuration import SINGLE_TRACKING_CACHE

'''
NAME OF CSV FILE WHICH STORES SINGLE TRACKING RESULTS
'''
def get_single_tracking_csv_filename():
    return get_result_csv_filename(cache_name=SINGLE_TRACKING_CACHE)


'''
RETURN SINGLE TRACKING RESULTS DATAFRAME
'''
def get_single_tracking_df():
    single_tracking_csv_filename = get_single_tracking_csv_filename()
    return pd.read_csv(single_tracking_csv_filename)