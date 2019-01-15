import numpy as np
import pandas as pd

from binary_reader.dataframes import DATAFRAMES
from binary_reader.dataframes import GEOM_RP_DF
from configuration import FILL
from configuration import RECO
from configuration import RUN
from configuration import PROJECT_PATH
from totem_comparator.cache.config import COMPARE_STATISTICS_CACHE
from totem_comparator.cache.config import RP_COMPARE_CACHES
from totem_comparator.cache.config import RP_IDS
from totem_comparator.cache.config import RP_ID_2_CACHE_NAME
from totem_comparator.cache.config import RP_MISSING_UV_CACHE

COMPARE_SINGLE_TRACKS_CACHE = {}

COMPARE_RP_HIT_COLUMNS = ["single_x", "single_y", "totem_x", "totem_y",
                          "diff_x", "diff_x [strip]", "diff_y", "diff_y [strip]",
                          "diff_total", "diff_total [strip]"]

COMPARE_STATISTICS_COLUMNS = ["eventID", "groupID", "exec_time[s]",
                              "dist_avg", "chi2_N",
                              "dx_dz_angle [mrad]", "dy_dz_angle [mrad]",
                              "tracks_out_det_no"]

RP_MISSING_UV_COLUMNS = ["eventID", "groupID", "rpID"]

'''
INIT CACHE
'''


def init_caches():
    for rp_hit_cache_name in RP_COMPARE_CACHES:
        COMPARE_SINGLE_TRACKS_CACHE[rp_hit_cache_name] = []
    COMPARE_SINGLE_TRACKS_CACHE[COMPARE_STATISTICS_CACHE] = []
    COMPARE_SINGLE_TRACKS_CACHE[RP_MISSING_UV_CACHE] = []

'''
SAVE CACHE
'''

'''
RP Z - PART OF RESULT FILENAME
'''


def get_rp_z_mm(rpID):
    geom_rp_df = DATAFRAMES[GEOM_RP_DF]
    rp_info = geom_rp_df.loc[(geom_rp_df['rpID'] == rpID)].iloc[0]
    return rp_info['z'] * 1000


def get_filename_csv(cache_name=None, rpID=None):
    if cache_name in RP_COMPARE_CACHES:
        rp_z = get_rp_z_mm(rpID)
        return PROJECT_PATH + "totem_comparator/results/{0}/{1}/{2}/{0}_{1}_{2}_hits_rp{3}_z_{4}.csv".format(FILL, RUN, RECO, rpID, rp_z)
    elif cache_name == COMPARE_STATISTICS_CACHE:
        return PROJECT_PATH + "totem_comparator/results/{0}/{1}/{2}/{0}_{1}_{2}_statistics.csv".format(FILL, RUN, RECO, rpID)
    elif cache_name == RP_MISSING_UV_CACHE:
        return PROJECT_PATH + "totem_comparator/results/{0}/{1}/{2}/{0}_{1}_{2}_rp_missing_uv.csv".format(FILL, RUN, RECO, rpID)
    return None


def get_comparator_result_df(cache_name=None):
    # GET DATA
    results_np = np.array(COMPARE_SINGLE_TRACKS_CACHE[cache_name])

    # GET COLUMN NAMES
    if cache_name in RP_COMPARE_CACHES:
        columns = COMPARE_RP_HIT_COLUMNS
    elif cache_name == COMPARE_STATISTICS_CACHE:
        columns = COMPARE_STATISTICS_COLUMNS
    elif cache_name == RP_MISSING_UV_CACHE:
        columns = RP_MISSING_UV_COLUMNS

    # CREATE DATAFRAME
    if results_np.size == 0:
        return pd.DataFrame(columns=columns)
    else:
        return pd.DataFrame(data=results_np, columns=columns)


'''
SAVING RP COMPARE CACHE
'''


def save_cached_rp_results(rpID):
    # GET DATAFRAME
    rp_compare_cache_name = RP_ID_2_CACHE_NAME[rpID]
    rp_compare_df = get_comparator_result_df(cache_name=rp_compare_cache_name)

    # STORE IT
    filename_csv = get_filename_csv(cache_name=rp_compare_cache_name, rpID=rpID)
    rp_compare_df.to_csv(filename_csv)

    # CLEAN IT
    COMPARE_SINGLE_TRACKS_CACHE[rp_compare_cache_name] = []


'''
SAVING STATISTICS CACHE
'''


def save_statistics_results():
    # GET DATAFRAME
    statistics_df = get_comparator_result_df(cache_name=COMPARE_STATISTICS_CACHE)

    # STORE IT
    filename_csv = get_filename_csv(cache_name=COMPARE_STATISTICS_CACHE)
    statistics_df.to_csv(filename_csv)

    # CLEAN IT
    COMPARE_SINGLE_TRACKS_CACHE[COMPARE_STATISTICS_CACHE] = []


'''
SAVING RP_MISSING_UV_CACHE
'''

def save_rp_missing_uv_cache():
    # GET DATAFRAME
    rp_missing_uv_df = get_comparator_result_df(cache_name=RP_MISSING_UV_CACHE)

    # STORE IT
    filename_csv = get_filename_csv(cache_name=RP_MISSING_UV_CACHE)
    rp_missing_uv_df.to_csv(filename_csv)

    # CLEAN IT
    COMPARE_SINGLE_TRACKS_CACHE[RP_MISSING_UV_CACHE] = []


'''
SAVING - MAIN
'''
def save_cached_results():
    for rpID in RP_IDS:
        save_cached_rp_results(rpID)
    save_statistics_results()
    save_rp_missing_uv_cache()


'''
CACHING VALUES
'''


def cache_record(record, cache_name=None):
    COMPARE_SINGLE_TRACKS_CACHE[cache_name].append(record)


def cache_rp_record(record, rpID):
    cache_name = RP_ID_2_CACHE_NAME[rpID]
    cache_record(record, cache_name)
