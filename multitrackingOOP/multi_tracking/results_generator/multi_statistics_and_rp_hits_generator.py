import pandas as pd

from common.track_results_dataframe import get_result_csv_filename
from configuration import MULTI_TRACKING_CACHE
from geometry_classes.Line import Line
from multi_tracking.results_generator.cache import cache_record
from multi_tracking.results_generator.cache import cache_rp_record
from multi_tracking.results_generator.cache import get_rp_z_mm
from multi_tracking.results_generator.cache import init_caches
from multi_tracking.results_generator.cache import save_cached_results
from multi_tracking.results_generator.config import GROUP_TO_RP_LIST
from multi_tracking.results_generator.config import MULTI_STATISTICS_CACHE

'''
The task is to generate:
    - (x, y, type(11, 12, 21), avg_dist, tracks_out_det_no)
	- Per each RP
	- /4499/9920/7/hits_rp21_z_-214628.csv
'''

'''
GET results/4499/9920/100/4499_9920_100_multi_results.csv DATAFRAME
'''


def get_multi_results_df():
    result_csv_filename = get_result_csv_filename(cache_name=MULTI_TRACKING_CACHE)
    return pd.read_csv(result_csv_filename)


def get_track_x_y(rpID, multi_result_row):
    x = multi_result_row['x']  # [mm]
    y = multi_result_row['y']  # [mm]
    z = multi_result_row['z']  # [mm]
    dx = multi_result_row['dx']  # [dx ** 2 + dy ** 2 + dz ** 2 = 1]
    dy = multi_result_row['dy']
    dz = multi_result_row['dz']
    track_line = Line(x=x, y=y, z=z, dx=dx, dy=dy, dz=dz)

    rp_z = get_rp_z_mm(rpID)
    return track_line.xy_on_z(rp_z)  # TODO TEST THAT METHOD WITH 3 DIFFERENT LINES ;)


def store_rp_track_hits(multi_result_row):
    groupID = multi_result_row['groupID']

    for rpID in GROUP_TO_RP_LIST[groupID]:
        x, y = get_track_x_y(rpID, multi_result_row)
        type = multi_result_row['track_type']
        dist_avg = multi_result_row['dist_avg']
        tracks_out_det_no = multi_result_row['tracks_out_det_no']

        record = [x, y, type, dist_avg, tracks_out_det_no]
        cache_rp_record(record, rpID)


def store_track_statistics(multi_result_row):
    track_type = multi_result_row['track_type']
    eventID = multi_result_row['eventID']
    groupID = multi_result_row['groupID']
    exec_time = multi_result_row['exec_time[s]']
    chi2_N = multi_result_row['chi2_N']
    dist_avg = multi_result_row['dist_avg']
    dx_dz_angle = multi_result_row['dx_dz_angle [mrad]']
    dy_dz_angle = multi_result_row['dy_dz_angle [mrad]']

    record = [track_type, eventID, groupID, exec_time, chi2_N, dist_avg, dx_dz_angle, dy_dz_angle]

    cache_record(record, cache_name=MULTI_STATISTICS_CACHE)


def save_multi_statistics_and_rp_hits():
    init_caches()
    multi_results_df = get_multi_results_df()

    for index, multi_result_row in multi_results_df.iterrows():
        store_rp_track_hits(multi_result_row)
        store_track_statistics(multi_result_row)

    save_cached_results()
