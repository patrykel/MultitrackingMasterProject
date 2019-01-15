import math
import time

from binary_reader.dataframes import DATAFRAMES
from binary_reader.dataframes import HIT_LINES_DF
from geometry_classes.Line import Line
from totem_comparator.cache.cache import cache_record
from totem_comparator.cache.cache import cache_rp_record
from totem_comparator.cache.cache import init_caches
from totem_comparator.cache.cache import save_cached_results
from totem_comparator.cache.config import COMPARE_STATISTICS_CACHE
from totem_comparator.single_tracks import get_single_tracking_df
from totem_comparator.totem_hit_point import get_totem_hit_point
from totem_comparator.cache.config import GROUP_ID_TO_RP_IDS
from totem_comparator.cache.config import SIGMA
from totem_comparator.cache.config import RP_MISSING_UV_CACHE


'''
===========
= TARGET: =
===========
- Per RP
    - columns:	[s_x, 	s_y, 	t_x, 	t_y,
                x_diff, 	sufit(x_diff 	/ SIGMA),	y_diff,	sufit(y_diff/SIGMA)
                total_diff, sufit(total_diff/ SIGMA)
                tracks_out_det_no]
    - filename:	/4499/9920/7/single_hits_compare_rp21_z-214628.csv
- Statistics:
    - columns: [eventID,groupID,exec_time[s],dist_avg,chi2_N,dx_dz_angle [mrad],dy_dz_angle [mrad], tracks_out_det_no]
    - filename: /4499/9920/7/single_statistics.csv

==========
= STEPS: =
==========
Load:
- single_result file:
    -   recoID,eventID,groupID,
        x,y,z,dx,dy,dz,exec_time[s],
        dist_max,dist_sum,dist_avg,chi2,chi2_N,
        dx_dz_angle [mrad],dy_dz_angle [mrad],
        tracks_in_det_no,tracks_out_det_no

- binary_file:
    -   'eventID', 'recoId', 'armID', 'groupID', 'rpID', 'uLineSize', 'vLineSize',
        'siliconID', 'direction', 'line_no', 'position', 'line_a', 'line_b', 'line_w'

For each (eventID, groupID)
    - create single Line
    - For each RP in group:
        - compute s_x, s_y, t_x, t_y
        - compute rest of the required fields
        - store record in cache
    - store statistics record
'''

'''
GET TOTEM HITS DF
'''


def get_totem_uv_lines_df():
    totem_hits_df = DATAFRAMES[HIT_LINES_DF]  # TODO MAYBE WE CAN GET RID OF SOME DATA FROM TOTEM_HITS_DF ???
    totem_hits_df = totem_hits_df[['eventID', 'groupID',
                                   'rpID', 'direction',
                                   'line_a', 'line_b']]
    totem_hits_df = totem_hits_df.drop_duplicates()
    return totem_hits_df


'''
GET LINE FROM single_tracking_row WHICH COMES FROM single_result file
'''


def get_single_track_line(single_tracking_row):
    x = single_tracking_row['x']
    y = single_tracking_row['y']
    z = single_tracking_row['z']
    dx = single_tracking_row['dx']
    dy = single_tracking_row['dy']
    dz = single_tracking_row['dz']

    return Line(x=x, y=y, z=z, dx=dx, dy=dy, dz=dz)


'''
TOTEM RP HITS UV LINES
'''


def get_totem_rp_uv_lines_df(totem_uv_lines_df, eventID, groupID, rpID):
    return totem_uv_lines_df.loc[(totem_uv_lines_df['eventID'] == eventID) &
                                 (totem_uv_lines_df['groupID'] == groupID) &
                                 (totem_uv_lines_df['rpID'] == rpID)]


'''
COMPARE RP HIT SINGLE vs TOTEM
'''


def compare_in_rp(single_line, totem_rp_uv_lines_df, eventID, groupID, rpID):
    if len(totem_rp_uv_lines_df) < 2:
        rp_missing_uv_record = [eventID, groupID, rpID]
        cache_record(rp_missing_uv_record, cache_name=RP_MISSING_UV_CACHE)
        print("\t[NO U/V LINE]")
        return

    totem_hit_point = get_totem_hit_point(totem_rp_uv_lines_df)
    # rpID = get_rp_id(totem_rp_uv_lines_df)

    hit_z = totem_hit_point.z
    single_x, single_y = single_line.xy_on_z(hit_z)

    # DATA TO CREATE RECORD
    totem_x = totem_hit_point.x
    totem_y = totem_hit_point.y

    diff_x = abs(totem_x - single_x)
    diff_y = abs(totem_y - single_y)
    diff_total = math.sqrt(diff_x ** 2 + diff_y ** 2)

    diff_x_strip = math.ceil(diff_x / SIGMA)
    diff_y_strip = math.ceil(diff_y / SIGMA)
    diff_total_strip = math.ceil(diff_total / SIGMA)

    record = [single_x, single_y, totem_x, totem_y,
              diff_x, diff_x_strip, diff_y, diff_y_strip,
              diff_total, diff_total_strip]

    cache_rp_record(record, rpID)


'''
CACHE STATISTICS
'''


def cache_statistic_record(single_tracking_row):
    eventID = single_tracking_row['eventID']
    groupID = single_tracking_row['groupID']
    exec_time = single_tracking_row['exec_time[s]']
    dist_avg = single_tracking_row['dist_avg']
    chi2_N = single_tracking_row['chi2_N']
    dx_dz_angle = single_tracking_row['dx_dz_angle [mrad]']
    dy_dz_angle = single_tracking_row['dy_dz_angle [mrad]']
    tracks_out_det_no = single_tracking_row['tracks_out_det_no']

    statistic_record = [eventID, groupID, exec_time, dist_avg, chi2_N,
                        dx_dz_angle, dy_dz_angle, tracks_out_det_no]

    cache_record(statistic_record, COMPARE_STATISTICS_CACHE)


'''
ENTRY #1 RUN COMPARISON
'''


def run_comparison():
    start_time = time.time()

    init_caches()  # init caches for rp comparison and statistics records
    single_tracking_df = get_single_tracking_df()
    totem_uv_lines_df = get_totem_uv_lines_df()

    for idx, single_tracking_row in single_tracking_df.iterrows():
        recoID = single_tracking_row['recoID']
        eventID = single_tracking_row['eventID']
        groupID = single_tracking_row['groupID']

        print("\tComparing tracks.\tEventID: {}\tGroupID: {}".format(eventID, groupID))

        single_line = get_single_track_line(single_tracking_row)

        for rpID in GROUP_ID_TO_RP_IDS[groupID]:
            totem_rp_uv_lines_df = get_totem_rp_uv_lines_df(totem_uv_lines_df, eventID, groupID, rpID)
            compare_in_rp(single_line, totem_rp_uv_lines_df, eventID, groupID, rpID)

        cache_statistic_record(single_tracking_row)

    save_cached_results()  # save cached records

    exec_time = time.time() - start_time
    print("Exec time: {}".format(exec_time))


# run_comparison()
