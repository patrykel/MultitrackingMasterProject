import copy

import pandas as pd

# DICTIONARY TO COUNT EVENT TYPES
MULTI_EVENTS_TYPES = {}

# MULTI_EVENT_TYPES KEYS
_00_LACK_DATA = "_0_LACK_DATA"
_10_1X1_3RP_LACK = "_10_1X1_3RP_LACK"
_11_1X1_3RP_1X1 = "_11_1X1_3RP_1X1"
_12_1X1_3RP_MORE = "_12_1X1_3RP_MORE"
_20_2X2_3RP_LACK = "_20_2X2_3RP_LACK"
_21_2X2_3RP_ENOUGH = "_21_2X2_3RP_ENOUGH"
_30_OTHER = "_30_OTHER"

# KEYS TO TEMPORARY DICTIONARY "rpIDs_by_type_dict"
_1x1_RP = "_1x1_RP"
_2x2_RP = "_2x2_RP"
_other_RP = "_other_RP"

# hit_lines_dict second level keys [rpID, direction, line_no]
U_KEY = 117
V_KEY = 118

'''
00 EVENT - MISSING DATA
'''


def is_00_event(hit_lines_dict):
    if len(hit_lines_dict) < 3:
        return True  # Lack of RP from group

    for rpID in hit_lines_dict:
        if len(hit_lines_dict[rpID]) < 2:
            return True  # Lack of U/V line

    return False


'''
1X EVENT - POTENTIALLY SINGLE TRACKING
'''


def is_1X_event(rpIDs_by_type_dict):
    rpIDs_1x1 = rpIDs_by_type_dict[_1x1_RP]
    return len(rpIDs_1x1) >= 2


def is_10_event(rp_types_dict, hit_lines_dict):
    other_rpIDs = rp_types_dict[_other_RP]
    '''
    We want one other RP where u or v line_no == 0
    '''
    if len(other_rpIDs) == 0:
        return False
    other_rpID = other_rpIDs[0]
    return len(hit_lines_dict[other_rpID][U_KEY]) == 0 or len(hit_lines_dict[other_rpID][V_KEY]) == 0


def is_11_event(rp_types_dict):
    return len(rp_types_dict[_1x1_RP]) == 3


def get_1X_event_type(rpIDs_by_type_dict, hit_lines_dict):
    if is_10_event(rpIDs_by_type_dict, hit_lines_dict):
        return _10_1X1_3RP_LACK
    elif is_11_event(rpIDs_by_type_dict):
        return _11_1X1_3RP_1X1
    else:
        return _12_1X1_3RP_MORE


'''
2X EVENT - POTENTIALLY MUTLITRACKING (2 TRACKS)
'''


def is_2X_event(rpIDs_by_type_dict):
    rpIDs_2x2 = rpIDs_by_type_dict[_2x2_RP]
    return len(rpIDs_2x2) >= 2


def is_20_event(rp_types_dict, hit_lines_dict):
    other_rpIDs = rp_types_dict[_other_RP]
    '''
    We want one other RP where u or v line_no < 2
    '''
    if len(other_rpIDs) == 0:
        return False
    other_rpID = other_rpIDs[0]
    return len(hit_lines_dict[other_rpID][U_KEY]) < 2 or len(hit_lines_dict[other_rpID][V_KEY]) < 2


def get_2X_event_type(rpIDs_by_type_dict, hit_lines_dict):
    if is_20_event(rpIDs_by_type_dict, hit_lines_dict):
        return _20_2X2_3RP_LACK
    else:
        return _21_2X2_3RP_ENOUGH


'''
ENTRY - #1 RP BY TYPE DICT
'''


def get_rpIDs_by_type_dict(hit_lines_dict):
    rpIDs_by_type_dict = {}

    # Initialize
    rpIDs_by_type_dict[_1x1_RP] = []
    rpIDs_by_type_dict[_2x2_RP] = []
    rpIDs_by_type_dict[_other_RP] = []

    # Fill rpIDs
    for rpID in hit_lines_dict:
        u_line_no = len(hit_lines_dict[rpID][U_KEY])
        v_line_no = len(hit_lines_dict[rpID][V_KEY])

        if u_line_no == 1 and v_line_no == 1:
            rpIDs_by_type_dict[_1x1_RP].append(rpID)  # RP with 1 u, 1 v
        elif u_line_no == 2 and v_line_no == 2:
            rpIDs_by_type_dict[_2x2_RP].append(rpID)  # RP with 2 u, 2 v
        else:
            rpIDs_by_type_dict[_other_RP].append(rpID)  # RP other

    return rpIDs_by_type_dict


'''
ENTRY - #2
'''


def init_multi_event_analysis_dictionary():
    MULTI_EVENTS_TYPES[_00_LACK_DATA] = 0
    MULTI_EVENTS_TYPES[_10_1X1_3RP_LACK] = 0
    MULTI_EVENTS_TYPES[_11_1X1_3RP_1X1] = 0
    MULTI_EVENTS_TYPES[_12_1X1_3RP_MORE] = 0
    MULTI_EVENTS_TYPES[_20_2X2_3RP_LACK] = 0
    MULTI_EVENTS_TYPES[_21_2X2_3RP_ENOUGH] = 0
    MULTI_EVENTS_TYPES[_30_OTHER] = 0


'''
ENTRY - #3
'''


def get_event_type(hit_lines_dict):
    if is_00_event(hit_lines_dict):
        return _00_LACK_DATA
    else:
        rpIDs_by_type_dict = get_rpIDs_by_type_dict(hit_lines_dict)
        if is_1X_event(rpIDs_by_type_dict):
            return get_1X_event_type(rpIDs_by_type_dict, hit_lines_dict)
        elif is_2X_event(rpIDs_by_type_dict):
            return get_2X_event_type(rpIDs_by_type_dict, hit_lines_dict)
        else:
            return _30_OTHER


'''
ENTRY - #4
'''


def update_event_types_dictionary(event_type):
    if event_type in MULTI_EVENTS_TYPES:
        MULTI_EVENTS_TYPES[event_type] = MULTI_EVENTS_TYPES[event_type] + 1


'''
ENTRY - #5
'''


def get_multi_events_types_df():
    type_dict = copy.deepcopy(MULTI_EVENTS_TYPES)
    for key in type_dict:
        type_dict[key] = [type_dict[key]]
    return pd.DataFrame.from_dict(type_dict)
