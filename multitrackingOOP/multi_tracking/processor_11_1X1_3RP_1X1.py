import time

from common.least_square_algorithm import compute_track_line
from common.track_results_dataframe import cache_result
from common.track_statistics import get_track_statistics
from configuration import MULTI_TRACKING_CACHE
from multi_tracking.event_types_analyzer import _11_1X1_3RP_1X1


def gather_hit_lines(hit_lines_dict):
    hit_lines = []
    for rpID in hit_lines_dict:
        for direction in hit_lines_dict[rpID]:
            for line_no in hit_lines_dict[rpID][direction]:
                for hit_line in hit_lines_dict[rpID][direction][line_no]:
                    hit_lines.append(hit_line)
    return hit_lines


def process_11_1X1_3RP_1X1(eventID, groupID, hit_lines_dict):
    hit_lines = gather_hit_lines(hit_lines_dict)

    start_time = time.time()
    track_line = compute_track_line(hit_lines)
    exec_time = time.time() - start_time

    track_statistics = get_track_statistics(track_line, hit_lines)
    cache_result(eventID, groupID, track_line, exec_time, track_statistics,
                 cache_name=MULTI_TRACKING_CACHE, event_type=_11_1X1_3RP_1X1, trackID=0)
