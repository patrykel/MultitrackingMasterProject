from multi_tracking.results_generator.config import RP_HIT_CACHES
from multi_tracking.results_generator.config import MULTI_STATISTICS_CACHE
from multi_tracking.results_generator.config import RP_IDS
from multi_tracking.results_generator.config import RP_ID_2_CACHE_NAME
from configuration import FILL
from configuration import RUN
from configuration import RECO
from configuration import PROJECT_PATH
from binary_reader.dataframes import DATAFRAMES
from binary_reader.dataframes import GEOM_RP_DF

import numpy as np
import pandas as pd

MULTI_RESULTS_CACHE = {}

MULTI_RP_HIT_COLUMNS = ["x", "y", "track_type", "dist_avg", "tracks_out_det_no"]
MULTI_STATISTICS_COLUMNS = ["track_type", "eventID", "groupID", "exec_time[s]", "chi2_N", "dist_avg",
                            "dx_dz_angle [mrad]",
                            "dy_dz_angle [mrad]"]
'''
INIT CACHE
'''


def init_caches():
    for rp_hit_cache_name in RP_HIT_CACHES:
        MULTI_RESULTS_CACHE[rp_hit_cache_name] = []
    MULTI_RESULTS_CACHE[MULTI_STATISTICS_CACHE] = []


'''
SAVE CACHE
'''


def get_rp_z_mm(rpID):
    geom_rp_df = DATAFRAMES[GEOM_RP_DF]
    rp_info = geom_rp_df.loc[(geom_rp_df['rpID'] == rpID)].iloc[0]
    return rp_info['z'] * 1000


def get_filename_csv(cache_name=None, rpID=None):
    if cache_name in RP_HIT_CACHES:
        rp_z = get_rp_z_mm(rpID)
        return PROJECT_PATH + "multi_tracking/results/{0}/{1}/{2}/{0}_{1}_{2}_hits_rp{3}_z_{4}.csv".format(FILL, RUN, RECO, rpID, rp_z)
    elif cache_name == MULTI_STATISTICS_CACHE:
        return PROJECT_PATH + "multi_tracking/results/{0}/{1}/{2}/{0}_{1}_{2}_statistics.csv".format(FILL, RUN, RECO, rpID)
    return None


def get_multi_result_df(cache_name=None):
    # GET DATA
    results_np = np.array(MULTI_RESULTS_CACHE[cache_name])

    # GET COLUMN NAMES
    if cache_name in RP_HIT_CACHES:
        columns = MULTI_RP_HIT_COLUMNS
    elif cache_name == MULTI_STATISTICS_CACHE:
        columns = MULTI_STATISTICS_COLUMNS

    # CREATE DATAFRAME
    if results_np.size == 0:
        return pd.DataFrame(columns=columns)
    else:
        return pd.DataFrame(data=results_np, columns=columns)


'''
SAVING RP HIT CACHE
'''


def save_cached_rp_results(rpID):
    # GET DATAFRAME
    rp_hit_cache_name = RP_ID_2_CACHE_NAME[rpID]
    rp_hits_df = get_multi_result_df(cache_name=rp_hit_cache_name)

    # STORE IT
    filename_csv = get_filename_csv(cache_name=rp_hit_cache_name, rpID=rpID)
    rp_hits_df.to_csv(filename_csv)

    # CLEAN IT
    MULTI_RESULTS_CACHE[rp_hit_cache_name] = []


'''
SAVING STATISTICS CACHE
'''


def save_statistics_results():
    # GET DATAFRAME
    statistics_df = get_multi_result_df(cache_name=MULTI_STATISTICS_CACHE)

    # STORE IT
    filename_csv = get_filename_csv(cache_name=MULTI_STATISTICS_CACHE)
    statistics_df.to_csv(filename_csv)

    # CLEAN IT
    MULTI_RESULTS_CACHE[MULTI_STATISTICS_CACHE] = []


def save_cached_results():
    for rpID in RP_IDS:
        save_cached_rp_results(rpID)
    save_statistics_results()


'''
CACHING VALUES
'''


def cache_record(record, cache_name=None):
    MULTI_RESULTS_CACHE[cache_name].append(record)


def cache_rp_record(record, rpID):
    cache_name = RP_ID_2_CACHE_NAME[rpID]
    cache_record(record, cache_name)
