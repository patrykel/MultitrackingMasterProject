from multi_tracking.event_types_analyzer import _00_LACK_DATA
from multi_tracking.event_types_analyzer import _10_1X1_3RP_LACK
from multi_tracking.event_types_analyzer import _11_1X1_3RP_1X1
from multi_tracking.event_types_analyzer import _12_1X1_3RP_MORE
from multi_tracking.event_types_analyzer import _20_2X2_3RP_LACK
from multi_tracking.event_types_analyzer import _21_2X2_3RP_ENOUGH
from multi_tracking.event_types_analyzer import _30_OTHER
from multi_tracking.processor_11_1X1_3RP_1X1 import process_11_1X1_3RP_1X1
from multi_tracking.processor_12_1X1_3RP_MORE import process_12_1X1_3RP_MORE
from multi_tracking.processor_21_2X2_3RP_ENOUGH import process_21_2X2_3RP_ENOUGH

def process_event(eventID, groupID, event_type, hit_lines_dict):
    if event_type == _00_LACK_DATA:
        return                                                      # [11.00%] [DO NOT SERVE] case: less than 3RP or no u or v line in RP (after filtering)
    elif event_type == _10_1X1_3RP_LACK:
        return                                                      # [00.00%] [DO NOT SERVE] case: 2RP 1x1, 3RP u == 0 or v == 0
    elif event_type == _11_1X1_3RP_1X1:
        process_11_1X1_3RP_1X1(eventID, groupID, hit_lines_dict)    # [57,50%] --> [SERVE] case where 3RP 1x1
    elif event_type == _12_1X1_3RP_MORE:
        process_12_1X1_3RP_MORE(eventID, groupID, hit_lines_dict)   # [18,55%] --> [SERVE] case where 2RP 1x1, 3RP u >=1 and v >= 1 (fishing)
    elif event_type == _20_2X2_3RP_LACK:
        return                                                      # [0.88%]  [DO NOT SERVE] case: 2RP 1x1, 3RP u == 0 or v == 0
    elif event_type == _21_2X2_3RP_ENOUGH:
        process_21_2X2_3RP_ENOUGH(eventID, groupID, hit_lines_dict) # [6.28%]  --> [SERVE] case: 2RP 2x2, 3RP enough to run fishing (u >= 2 and v >=2)
    elif event_type == _30_OTHER:
        return                                                      # [5.77%]  [DO NOT SERVE]  other cases
    else:
        return
