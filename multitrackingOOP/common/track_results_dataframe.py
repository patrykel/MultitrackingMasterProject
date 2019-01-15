import numpy as np
import pandas as pd

from configuration import *

CACHED_RESULTS = {}
SINGLE_TRACKING_COLUMNS = ["recoID", "eventID", "groupID", "x", "y", "z", "dx", "dy", "dz", "exec_time[s]",
           "dist_max", "dist_sum", "dist_avg", "chi2", "chi2_N", "dx_dz_angle [mrad]", "dy_dz_angle [mrad]",
           "tracks_in_det_no", "tracks_out_det_no"]

MULTI_TRACKING_COLUMNS = ["recoID", "eventID", "groupID", "x", "y", "z", "dx", "dy", "dz", "exec_time[s]",
           "dist_max", "dist_sum", "dist_avg", "chi2", "chi2_N", "dx_dz_angle [mrad]", "dy_dz_angle [mrad]",
           "tracks_in_det_no", "tracks_out_det_no", "track_type", "trackID"]


def get_result_csv_filename(cache_name=None):
    if cache_name == SINGLE_TRACKING_CACHE:
        return PROJECT_PATH + "single_tracking/results/{0}/{1}/{0}_{1}_{2}_single_results.csv".format(FILL, RUN, RECO)
    elif cache_name == MULTI_TRACKING_CACHE:
        return PROJECT_PATH + "multi_tracking/results/{0}/{1}/{2}/{0}_{1}_{2}_multi_results.csv".format(FILL, RUN, RECO)
    else:
        return None

'''
ENTRY POINT - #1
'''


def init_track_results_cache(cache_name=None):
    CACHED_RESULTS[cache_name] = []


'''
ENTRY POINT - #2
'''


def cache_result(eventID, groupID, track_line, exec_time, track_statistics, cache_name=None, event_type=None, trackID=None):
    result_record = [RECO, eventID, groupID] + \
                    [track_line.x, track_line.y, track_line.z] + \
                    [track_line.dx, track_line.dy, track_line.dz] + \
                    [exec_time] + \
                    track_statistics

    if event_type is not None:
        result_record = result_record + [event_type]            # FOR MULTITRACKING PURPOSES

    if trackID is not None:
        result_record = result_record + [trackID]

    global CACHED_RESULTS
    if cache_name in CACHED_RESULTS:
        CACHED_RESULTS[cache_name].append(result_record)


'''
ENTRY POINT - #3
'''


def save_cached_tracks(cache_name=None):
    global CACHED_RESULTS
    if cache_name not in CACHED_RESULTS:
        return

    # GET DATA
    results_np = np.array(CACHED_RESULTS[cache_name])

    # GET COLUMN NAMES
    if cache_name == SINGLE_TRACKING_CACHE:
        columns = SINGLE_TRACKING_COLUMNS
    else:
        columns = MULTI_TRACKING_COLUMNS

    # CREATE DATAFRAME
    results_df = pd.DataFrame(data=results_np, columns=columns)

    # STORE IT
    result_csv_filename = get_result_csv_filename(cache_name=cache_name)
    results_df.to_csv(result_csv_filename)

    # CLEAN CACHE
    CACHED_RESULTS[cache_name] = []
