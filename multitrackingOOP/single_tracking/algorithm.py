# Here I want to receive dataframe with records:
#   (reco, event, group, Line=(x,y,z,dx,dy,dz), exec_time[s])
# And store it to propper file: single/4499/9920/4499_9920_100_single_results


# Algorithm flow:

# Iterate over all (eventID, groupID) pairs --> groupID belongs to [1,2,3,4,5,6]
# Create track line that best fits activated silicon strips
# Calculate statistics for track
# Store statistics

import time

from common.least_square_algorithm import *
from common.track_results_dataframe import cache_result
from common.track_results_dataframe import init_track_results_cache
from common.track_results_dataframe import save_cached_tracks
from common.track_statistics import *
from single_tracking.hit_lines import *


def get_event_group_pairs():
    single_tracking_event_groups_df = DATAFRAMES[SINGLE_HIT_EVENT_GROUP_DF]
    return single_tracking_event_groups_df[['eventID', 'groupID']].values


# MAIN ALGORITHM
def run_single_tracking():
    init_track_results_cache(cache_name=SINGLE_TRACKING_CACHE)

    for eventID, groupID in get_event_group_pairs():

        print("\tSingle tracking.\tEvent: {}\tGroup: {}".format(eventID, groupID))

        hit_lines = get_hit_lines(eventID, groupID)  # Plain silicon hit lines. All in mm, real NOT TRANSLATED numbers

        start_time = time.time()
        track_line = compute_track_line(hit_lines)
        exec_time = time.time() - start_time

        track_statistics = get_track_statistics(track_line, hit_lines)
        cache_result(eventID, groupID, track_line, exec_time, track_statistics, cache_name=SINGLE_TRACKING_CACHE)

    save_cached_tracks(cache_name=SINGLE_TRACKING_CACHE)
