from common.track_results_dataframe import init_track_results_cache
from common.track_results_dataframe import save_cached_tracks
from multi_tracking.dataframes_save import save_dataframe
from multi_tracking.event_processor import process_event
from multi_tracking.event_types_analyzer import get_event_type
from multi_tracking.event_types_analyzer import get_multi_events_types_df
from multi_tracking.event_types_analyzer import init_multi_event_analysis_dictionary
from multi_tracking.event_types_analyzer import update_event_types_dictionary
from multi_tracking.multi_hit_lines import *
from multi_tracking.results_generator.multi_statistics_and_rp_hits_generator import save_multi_statistics_and_rp_hits


# Here I want to receive dataframe with records:
#   (reco, event, group, track_id, Line=(x,y,z,dx,dy,dz), exec_time[s], track_statistics)
# Store to file: multi/4499/9920/4499_9920_100_multi_results

def get_event_group_pairs():
    multi_tracking_event_groups_df = DATAFRAMES[MULTI_HIT_EVENT_GROUP_DF]
    return multi_tracking_event_groups_df[['eventID', 'groupID']].values


def before_multi_algorithm():
    save_dataframe(MULTI_HIT_EVENT_GROUP_DF)
    init_track_results_cache(cache_name=MULTI_TRACKING_CACHE)
    init_multi_event_analysis_dictionary()


# MAIN ALGORITHM
def run_multi_tracking():
    before_multi_algorithm()

    for eventID, groupID in get_event_group_pairs():
        print("\tMultitracking.\tEventID: {}\tGroupID: {}".format(eventID, groupID))

        # if eventID > 20010123:
        #     break

        # CREATE HIT LINES DICT
        hit_lines_dict = get_hit_lines_dict(eventID, groupID)
        event_type = get_event_type(hit_lines_dict)
        update_event_types_dictionary(event_type)

        # PROCESS = GET TRACK LINES AND STORE STATISTICS TO CACHE
        # start_time = time.time()
        process_event(eventID, groupID, event_type, hit_lines_dict)
        # exec_time = time.time() - start_time


        # Would be nice to store: [eventID, groupID, kind, exec time]
        # In different dataframe, as many lines may be in single group

    save_dataframe("event_types", get_multi_events_types_df())
    save_cached_tracks(cache_name=MULTI_TRACKING_CACHE)

    save_multi_statistics_and_rp_hits()         # REQUIRES THAT 4499_9920_100_multi_results.csv EXISTS

# run_multi_tracking()
