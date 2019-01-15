import time

from common.least_square_algorithm import compute_track_line
from common.track_results_dataframe import cache_result
from common.track_statistics import get_track_statistics
from configuration import MULTI_TRACKING_CACHE
from multi_tracking.event_types_analyzer import _12_1X1_3RP_MORE
from multi_tracking.event_types_analyzer import _1x1_RP
from multi_tracking.event_types_analyzer import get_rpIDs_by_type_dict


'''
Ok, here we get 2RP 1x1, and 1 PR with more lines. <-- would be nice to have rp_dict
Track for two RPs.
For each u and v line from 3RP calculate avg dist
Take best u and best v.
Do single tracking once again.
Save results
'''

'''
HIT LINE FOR 2 RP u == 1 and v == 1
'''


def gather_hit_lines_2rp_1x1(hit_lines_dict, rpIDs_by_type_dict):
    hit_lines = []
    for rpID in rpIDs_by_type_dict[_1x1_RP]:
        for direction in hit_lines_dict[rpID]:
            for line_no in hit_lines_dict[rpID][direction]:
                for hit_line in hit_lines_dict[rpID][direction][line_no]:
                    hit_lines.append(hit_line)
    return hit_lines


'''
HIT LINE OTHER 3rd RP u >= 1 and v >= 1
'''


def get_other_rpID(hit_lines_dict, rpIDs_by_type_dict):
    for rpID in hit_lines_dict:
        if rpID not in rpIDs_by_type_dict[_1x1_RP]:
            return rpID


def get_avg_distance(track_line_2rp_1x1, hit_lines):
    distances = [track_line_2rp_1x1.distance(line) for line in hit_lines]
    return sum(distances) / len(hit_lines)


LINE_NO = "line_no"
AVG_DIST = "avg_dist"


def get_init_best_uv_line_no_dict():
    return {LINE_NO: -1, AVG_DIST: -1.0}


def found_better_avg_dist(best_uv_line_no, direction, line_no, uv_lines_avg_dist):
    return best_uv_line_no[direction][AVG_DIST] > uv_lines_avg_dist[direction][line_no]


def update_best_uv_line_no(best_uv_line_no, direction, line_no, uv_lines_avg_dist):
    best_uv_line_no[direction][LINE_NO] = line_no
    best_uv_line_no[direction][AVG_DIST] = uv_lines_avg_dist[direction][line_no]


def get_hit_lines_final(hit_lines_dict, rpIDs_by_type_dict, track_line_2rp_1x1):
    other_rpID = get_other_rpID(hit_lines_dict, rpIDs_by_type_dict)

    # FOR EACH UV LINE IN OTHER RP CALCULATE AVG DISTANCE TO TRACK
    uv_lines_avg_dist = {}
    for direction in hit_lines_dict[other_rpID]:
        uv_lines_avg_dist[direction] = {}
        for line_no in hit_lines_dict[other_rpID][direction]:
            hit_lines = hit_lines_dict[other_rpID][direction][line_no]
            uv_lines_avg_dist[direction][line_no] = get_avg_distance(track_line_2rp_1x1, hit_lines)

    # FOR EACH DIRECTION CHOSE BEST AVG DISTANCE AND STORE LINE_NO
    best_uv_line_no = {}
    for direction in hit_lines_dict[other_rpID]:
        best_uv_line_no[direction] = get_init_best_uv_line_no_dict()

        for line_no in uv_lines_avg_dist[direction]:
            if best_uv_line_no[direction][LINE_NO] == -1:
                update_best_uv_line_no(best_uv_line_no, direction, line_no, uv_lines_avg_dist)
            elif found_better_avg_dist(best_uv_line_no, direction, line_no, uv_lines_avg_dist):
                update_best_uv_line_no(best_uv_line_no, direction, line_no, uv_lines_avg_dist)
            else:
                continue

    # TAKE hit lines FROM 2RP_1X1 and from best U and V lines from other RP.
    hit_lines_final = gather_hit_lines_2rp_1x1(hit_lines_dict, rpIDs_by_type_dict)

    # print("2RP lines: {}".format(len(hit_lines_final)), end='')
    # for direction in best_uv_line_no:
    #     other_line_no = best_uv_line_no[direction][LINE_NO]
    #     other_hit_lines = hit_lines_dict[other_rpID][direction][other_line_no]
    #     hit_lines_final = hit_lines_final + other_hit_lines
    #     print(" 3RP {}: {}".format(direction, len(other_hit_lines)), end='')
    # print("")

    # RETURN those lines as the final set of lines
    return hit_lines_final


'''
ENTRY - #1
'''

# TODO TEST IT AS MUCH AS I ONLY CAN --> EACH METHOD --> RESULTS SEEMS OK :) (AT LEAST ACCEPTABLE)!!!
def process_12_1X1_3RP_MORE(eventID, groupID, hit_lines_dict):
    # Dict to distiguish 2rp u == 1 and v == 1 FROM other 3rd RP
    rpIDs_by_type_dict = get_rpIDs_by_type_dict(hit_lines_dict)

    '''
    MEASURE TIME
    '''
    start_time = time.time()
    # Track for 2 rp u == 1 and v == 1
    hit_lines_2rp_1x1 = gather_hit_lines_2rp_1x1(hit_lines_dict, rpIDs_by_type_dict)
    track_line_2rp_1x1 = compute_track_line(hit_lines_2rp_1x1)
    # Final track with best u and v lines from other 3rd RP
    hit_lines_final = get_hit_lines_final(hit_lines_dict, rpIDs_by_type_dict, track_line_2rp_1x1)
    track_line_final = compute_track_line(hit_lines_final)
    exec_time = time.time() - start_time

    '''
    SAVE STATISTICS
    '''
    track_statistics = get_track_statistics(track_line_final, hit_lines_final)
    cache_result(eventID, groupID, track_line_final, exec_time, track_statistics,
                 cache_name=MULTI_TRACKING_CACHE, event_type=_12_1X1_3RP_MORE, trackID=0)
