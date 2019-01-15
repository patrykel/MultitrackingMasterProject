import time
import math

from common.least_square_algorithm import compute_track_line
from common.track_results_dataframe import cache_result
from common.track_statistics import get_track_statistics
from multi_tracking.event_types_analyzer import _21_2X2_3RP_ENOUGH
from multi_tracking.event_types_analyzer import _2x2_RP
from multi_tracking.event_types_analyzer import get_rpIDs_by_type_dict
from configuration import MULTI_TRACKING_CACHE

'''
Flow:
    - get 2RP 2x2 (watch out - there may be three of them!!! --> then take not rotated)
    - get all combinations of 1u_line_no, 1v_line_no, 2u_line_no, 2_v_line_no
    - for each combination:
        - get track_line (watch out for long times) --> analyze
        - calculate avg distance
        - get best u and v --> calculate avg distance

    - create pairs of 4 by 4 combination:
        0000 - 1111
        0001 - 1110
        ...
        0111 - 1000

    - pick one with best overall avg (with best u and v)

    - compute tracks once again

IMPORTANT:
    - There will be 2 tracks. Track processing time = total time / 2
    - Threre may be 3 RP 2X2
'''

TRANSLATED_IDX = "TRANSLATED_IDX"
TRACK_LINE = "TRACK_LINE"
AVG_DIST = "AVG_DIST"
BEST_U = "BEST_U"
BEST_V = "BEST_V"
DIR_AVG_DIST = "DIR_AVG_DIST"
LINE_NO = "LINE_NO"
EXEC_TIME = "EXEC_TIME"

U_DIRECTION = 117
V_DIRECTION = 118


def get_fitting_rpIDs(rpIDs_by_type_dict):
    rp_ids_2x2 = rpIDs_by_type_dict[_2x2_RP]
    rp_ids_2x2.sort()
    return rp_ids_2x2[:2]


def get_fishing_rpID(fitting_rpIDs, hit_lines_dict):
    for rpID in hit_lines_dict:
        if rpID not in fitting_rpIDs:
            return rpID


'''
{
    rpID: {U_DIRECTION: [0,1], V_DIRECTION: [2,3]},
    rpID: {U_DIRECTION: [1,2], V_DIRECTION: [0,1]}
}
'''


def get_empty_lines_no_dictionary(fitting_rpIDs):
    lines_no_dictionary = {}
    for rpID in fitting_rpIDs:
        lines_no_dictionary[rpID] = {}
        lines_no_dictionary[rpID][U_DIRECTION] = []
        lines_no_dictionary[rpID][V_DIRECTION] = []
    return lines_no_dictionary


def get_lines_no_dictionary(fitting_rpIDs, hit_lines_dict):
    lines_no_dictionary = get_empty_lines_no_dictionary(fitting_rpIDs)

    for rpID in fitting_rpIDs:
        lines_no_dictionary[rpID][U_DIRECTION] = list(hit_lines_dict[rpID][U_DIRECTION].keys())
        lines_no_dictionary[rpID][V_DIRECTION] = list(hit_lines_dict[rpID][V_DIRECTION].keys())

    return lines_no_dictionary


'''
RETURNS ["0_0_0_0" ... "1_1_1_1"] rp1_u_line_idx, rp1_v_line_idx, rp2_u_line_idx, rp2_v_line_idx
'''


def get_idx_combinations():
    idx_combinations = []
    for idx in range(0, 2 ** 4):
        idx_combination_string = format(idx, '04b')  # '0101'
        idx_combination_chr_array = list(idx_combination_string)  # ['0', '1', '0', '1']
        idx_combination = '_'.join(idx_combination_chr_array)  # '0_1_0_1'
        idx_combinations.append(idx_combination)
    return idx_combinations


'''
GET IDX TO TRACK DICT (WITH AUXILIARY STATISTICS)
{
    "0_0_0_0" :
    {   "TRANSLATED_IDX": "0_2_1_3",
        "TRACK_LINE" : Line(),
        "EXEC_TIME" : 0.0513241243,
        "BEST_U" : {"LINE_NO" : 7, "DIR_AVG_DIST": 0.075}
        "BEST_V" : {"LINE_NO" : 6, "DIR_AVG_DIST": 0.065}
        "AVG_DIST" : 0.06,                                  # for all (fitted and fished)
    }
}
'''


def get_empty_combi_track_dict(combi_strings):
    idx_track_dict = {}
    for combi_string in combi_strings:
        idx_track_dict[combi_string] = {}
        idx_track_dict[combi_string][TRANSLATED_IDX] = None
        idx_track_dict[combi_string][TRACK_LINE] = None
        idx_track_dict[combi_string][AVG_DIST] = None
        idx_track_dict[combi_string]
        idx_track_dict[combi_string][BEST_U] = {}
        idx_track_dict[combi_string][BEST_U][LINE_NO] = None
        idx_track_dict[combi_string][BEST_U][DIR_AVG_DIST] = None
        idx_track_dict[combi_string][BEST_V] = {}
        idx_track_dict[combi_string][BEST_V][LINE_NO] = None
        idx_track_dict[combi_string][BEST_V][DIR_AVG_DIST] = None
    return idx_track_dict


'''
1. TRANSLATE COMBINATION "0000" --> "0213"
'''


def get_combi_idx_at_position(i, combi_string):
    return int(combi_string.split('_')[i])


def get_translated_combi_string(combi_string, fitting_rpIDs, lines_no_dictionary):
    translated_line_no_strings = []  # array of strings
    i = 0
    for rpID in fitting_rpIDs:
        for direction in [U_DIRECTION, V_DIRECTION]:
            line_idx = get_combi_idx_at_position(i, combi_string)
            i = i + 1

            line_no_string = str(lines_no_dictionary[rpID][direction][line_idx])
            translated_line_no_strings.append(line_no_string)

    return '_'.join(translated_line_no_strings)


'''
2. Calculate track line for fitting RP
'''


def get_hit_lines_combi(fitting_rpIDs, hit_lines_dict, translated_combi_string):
    hit_lines = []
    i = 0
    for rpID in fitting_rpIDs:
        for direction in [U_DIRECTION, V_DIRECTION]:
            line_no = get_combi_idx_at_position(i, translated_combi_string)
            i = i + 1
            for hit_line in hit_lines_dict[rpID][direction][line_no]:
                hit_lines.append(hit_line)
    return hit_lines


def get_track_line_combi(translated_idx_combi, fitting_rpIDs, hit_lines_dict):
    hit_lines_combi = get_hit_lines_combi(fitting_rpIDs, hit_lines_dict, translated_idx_combi)
    track_line_combi = compute_track_line(hit_lines_combi)
    return track_line_combi


'''
3. Get best u line from fishing RP
'''


def get_best_dir_avg_dist(track_line_combi, hit_lines_dict, fishing_rpID, direction, line_no):
    hit_lines_best_dir = hit_lines_dict[fishing_rpID][direction][line_no]
    distances = [track_line_combi.distance(line) for line in hit_lines_best_dir]
    return sum(distances) / len(hit_lines_best_dir)


def get_best_direction_dict(track_line_combi, fishing_rpID, hit_lines_dict, direction):
    best_direction_dict = {LINE_NO: None, DIR_AVG_DIST: None}
    for line_no in hit_lines_dict[fishing_rpID][direction]:
        if best_direction_dict[LINE_NO] is None:
            best_direction_dict[LINE_NO] = line_no
            best_direction_dict[DIR_AVG_DIST] = get_best_dir_avg_dist(track_line_combi, hit_lines_dict,
                                                                      fishing_rpID, direction, line_no)
        else:
            next_avg_dist = get_best_dir_avg_dist(track_line_combi, hit_lines_dict, fishing_rpID, direction, line_no)
            if best_direction_dict[DIR_AVG_DIST] > next_avg_dist:
                best_direction_dict[LINE_NO] = line_no
                best_direction_dict[DIR_AVG_DIST] = next_avg_dist
    return best_direction_dict


'''
4. Avg distance of all lines alligned to track
'''


def get_hit_lines_fishing(hit_lines_dict, fishing_rpID, best_dir_dict, direction):
    line_no = best_dir_dict[LINE_NO]
    return hit_lines_dict[fishing_rpID][direction][line_no]


def get_hit_lines_all(best_u_dict, best_v_dict, fishing_rpID, fitting_rpIDs, hit_lines_dict, translated_combi_string):
    hit_lines_all = []
    for hit_line in get_hit_lines_combi(fitting_rpIDs, hit_lines_dict, translated_combi_string):
        hit_lines_all.append(hit_line)
    for hit_line_u in get_hit_lines_fishing(hit_lines_dict, fishing_rpID, best_u_dict, U_DIRECTION):
        hit_lines_all.append(hit_line_u)
    for hit_line_v in get_hit_lines_fishing(hit_lines_dict, fishing_rpID, best_v_dict, V_DIRECTION):
        hit_lines_all.append(hit_line_v)
    return hit_lines_all


def get_avg_dist(track_line_combi, translated_idx_combi, fitting_rpIDs, fishing_rpID, best_u_dict, best_v_dict,
                 hit_lines_dict):
    hit_lines_all = get_hit_lines_all(best_u_dict, best_v_dict, fishing_rpID,
                                      fitting_rpIDs, hit_lines_dict, translated_idx_combi)
    distances = [track_line_combi.distance(line) for line in hit_lines_all]
    return sum(distances) / len(hit_lines_all)


'''
{
    "0_0_0_0" :
    {   "TRANSLATED_IDX": "0_2_1_3",
        "TRACK_LINE" : Line(),
        "EXEC_TIME" : 0.0513241243,
        "BEST_U" : {"LINE_NO" : 7, "DIR_AVG_DIST": 0.075}
        "BEST_V" : {"LINE_NO" : 6, "DIR_AVG_DIST": 0.065}
        "AVG_DIST" : 0.06,                                  # for all (fitted and fished)
    }
}
'''


def get_combi_track_dict(combi_strings, fitting_rpIDs, fishing_rpID, hit_lines_dict):
    lines_no_dictionary = get_lines_no_dictionary(fitting_rpIDs,
                                                  hit_lines_dict)  # [rpID][direction] -> [line_no_1, line_no_2]
    combi_track_dict = get_empty_combi_track_dict(combi_strings)
    for combi_string in combi_strings:
        translated_combi_string = get_translated_combi_string(combi_string, fitting_rpIDs, lines_no_dictionary)
        start_time_combi= time.time()
        track_line_combi = get_track_line_combi(translated_combi_string, fitting_rpIDs, hit_lines_dict)
        exec_time_combi = time.time() - start_time_combi
        best_u_dict = get_best_direction_dict(track_line_combi, fishing_rpID, hit_lines_dict, U_DIRECTION)
        best_v_dict = get_best_direction_dict(track_line_combi, fishing_rpID, hit_lines_dict, V_DIRECTION)
        avg_dist = get_avg_dist(track_line_combi, translated_combi_string, fitting_rpIDs, fishing_rpID, best_u_dict,
                                best_v_dict, hit_lines_dict)

        combi_track_dict[combi_string][EXEC_TIME] = exec_time_combi
        combi_track_dict[combi_string][TRANSLATED_IDX] = translated_combi_string
        combi_track_dict[combi_string][TRACK_LINE] = track_line_combi
        combi_track_dict[combi_string][BEST_U] = best_u_dict
        combi_track_dict[combi_string][BEST_V] = best_v_dict
        combi_track_dict[combi_string][AVG_DIST] = avg_dist

    return combi_track_dict


'''
GET COMBI STRING B (ANOTHER to complete a pair) { "0_0_1_0" ->  "1_1_0_1" : avg of avg, ... }
'''


def get_combi_string_B(combi_string_A):
    combi_string_B = combi_string_A.replace('0', '#').replace('1', '0').replace('#', '1')

    # '0_1_0_1'
    # '#_1_#_1'
    # '#_0_#_0'
    # '1_0_1_0'

    return combi_string_B


'''
COMBI PAIR: 0_1_0_0#1_0_1_1 : AVG OF AVG
'''

def get_combi_pairs_avg_dict(combi_track_dict):
    combi_pairs_avg_dict = {}
    for combi_string_A in combi_track_dict:
        if combi_string_A[0] == '1':  # we want to serve only 0xxx to find counter part
            continue
        combi_string_B = get_combi_string_B(combi_string_A)
        combi_pair = combi_string_A + '#' + combi_string_B
        avg_A = combi_track_dict[combi_string_A][AVG_DIST]
        avg_B = combi_track_dict[combi_string_B][AVG_DIST]
        combi_pairs_avg_dict[combi_pair] = math.sqrt(avg_A**2 + avg_B**2)
    return combi_pairs_avg_dict


'''
RECOMPUTE AND STORE TRACKS
'''


def get_hit_lines_final(combi_string, idx_track_dict, hit_lines_dict, fitting_rpIDs, fishing_rpID):
    lines_no_dictionary = get_lines_no_dictionary(fitting_rpIDs,
                                                  hit_lines_dict)  # [rpID][direction] -> [line_no_1, line_no_2]
    translated_combi_string = get_translated_combi_string(combi_string, fitting_rpIDs, lines_no_dictionary)

    best_u_dict = idx_track_dict[combi_string][BEST_U]
    best_v_dict = idx_track_dict[combi_string][BEST_V]

    return get_hit_lines_all(best_u_dict, best_v_dict,
                             fishing_rpID, fitting_rpIDs,
                             hit_lines_dict, translated_combi_string)


def recompute_and_store_tracks(eventID, groupID, start_time,
                               combi_pairs_avg_dict, idx_track_dict, hit_lines_dict,
                               fitting_rpIDs, fishing_rpID):
    best_pair = min(combi_pairs_avg_dict, key=combi_pairs_avg_dict.get)  # SO WE KNOW INDEXES OF BEST TWO LINES

    '''
    FIRST TRACK
    '''
    combi_string_first = best_pair.split('#')[0]
    hit_lines_first = get_hit_lines_final(combi_string_first, idx_track_dict, hit_lines_dict,
                                          fitting_rpIDs, fishing_rpID)
    track_line_first = compute_track_line(hit_lines_first)

    '''
    SECOND TRACK
    '''
    combi_string_second = best_pair.split('#')[1]
    hit_lines_second = get_hit_lines_final(combi_string_second, idx_track_dict, hit_lines_dict,
                                           fitting_rpIDs, fishing_rpID)
    track_line_second = compute_track_line(hit_lines_second)

    exec_time = time.time() - start_time

    '''
    FIRST STATISTICS
    '''
    track_statistics_first = get_track_statistics(track_line_first, hit_lines_first)
    cache_result(eventID, groupID, track_line_first, exec_time / 2.0, track_statistics_first,
                 cache_name=MULTI_TRACKING_CACHE, event_type=_21_2X2_3RP_ENOUGH, trackID=0)

    '''
    SECOND STATISTICS
    '''
    track_statistics_second = get_track_statistics(track_line_second, hit_lines_second)
    cache_result(eventID, groupID, track_line_second, exec_time / 2.0, track_statistics_second,
                 cache_name=MULTI_TRACKING_CACHE, event_type=_21_2X2_3RP_ENOUGH, trackID=1)


'''
ENTRY #1
'''


def process_21_2X2_3RP_ENOUGH(eventID, groupID, hit_lines_dict):
    start_time = time.time()

    rpIDs_by_type_dict = get_rpIDs_by_type_dict(hit_lines_dict)

    fitting_rpIDs = get_fitting_rpIDs(rpIDs_by_type_dict)  # Return SORTED fitting rp ids
    fishing_rpID = get_fishing_rpID(fitting_rpIDs, hit_lines_dict)

    idx_combinations = get_idx_combinations()  # We cannot use lists... We need to use strings ["0000", ... , "1111"]

    '''
    HERE WE SPEND SOME TIME --> COMPUTE 16 TRACK LINES ;)
    '''
    combi_track_dict = get_combi_track_dict(idx_combinations, fitting_rpIDs, fishing_rpID, hit_lines_dict)
    combi_pairs_avg_dict = get_combi_pairs_avg_dict(combi_track_dict)

    '''
    HERE WE RECOMPUTE TRACKS AND STORE EM TO CACHE
    '''
    recompute_and_store_tracks(eventID, groupID, start_time,
                               combi_pairs_avg_dict, combi_track_dict, hit_lines_dict,
                               fitting_rpIDs, fishing_rpID)
