from binary_reader.dataframes import *
from geometry_classes.Line import *

WEIGHT_THRESHOLD = 3.0
STDEV_TRHESHOLD = 1.0  # I would give it smaller

'''
HIT POSITIONS FOR GIVEN EVENT_ID, GROUP_ID
'''


def get_hit_positions_df(eventID, groupID):
    hit_positions_df = DATAFRAMES[HIT_LINES_DF]
    return hit_positions_df[(hit_positions_df['eventID'] == eventID) &
                            (hit_positions_df['groupID'] == groupID)]


'''
[RP_ID, DIRECTION (117|118), LINE_NO] TRIPLETS (VALID LINES ONLY)
'''


def get_rp_dir_line_triplets(hit_positions_df):
    stats_df = hit_positions_df.groupby(['rpID', 'direction', 'line_no', 'line_w'])[
        'position'].std().to_frame().reset_index().rename(columns={"position": "position_std"})
    stats_df = stats_df.loc[(stats_df['position_std'] < STDEV_TRHESHOLD) &
                            (stats_df['line_w'] > WEIGHT_THRESHOLD)]
    return stats_df[['rpID', 'direction', 'line_no']].values


'''
SILICON HIT LINES
'''


def get_silicon_id(hit_position_info):
    return 10 * hit_position_info['rpID'] + hit_position_info['siliconID']


def get_silicon_info(silicon_id):
    geom_silicon_df = DATAFRAMES[GEOM_SILICON_DF]
    return geom_silicon_df[(geom_silicon_df['detId'] == silicon_id)].iloc[0]


def hit_line_x(hit_position_info, silicon_info):
    return silicon_info['x'] + \
           hit_position_info['position'] * silicon_info['dx']


def hit_line_y(hit_position_info, silicon_info):
    return silicon_info['y'] + \
           hit_position_info['position'] * silicon_info['dy']


def hit_line_z_in_mm(silicon_info):
    return silicon_info['z'] * 1000


def hit_line_dx(silicon_info):
    return - silicon_info['dy']


def hit_line_dy(silicon_info):
    return silicon_info['dx']


def hit_line_dz():
    return 0.0


def get_silicon_hit_lines(hit_positions_df):
    silicon_hit_lines = []

    for idx, hit_position_info in hit_positions_df.iterrows():
        silicon_id = get_silicon_id(hit_position_info)
        silicon_info = get_silicon_info(silicon_id)

        x = hit_line_x(hit_position_info, silicon_info)
        y = hit_line_y(hit_position_info, silicon_info)
        z = hit_line_z_in_mm(silicon_info)
        dx = hit_line_dx(silicon_info)
        dy = hit_line_dy(silicon_info)
        dz = hit_line_dz()

        silicon_hit_lines.append(Line(x, y, z, dx, dy, dz, silicon_id=silicon_id))

    return silicon_hit_lines


'''
GET HIT LINES FOR [EVENT_ID GROUP_ID]
'''


def get_hit_lines_dict(eventID, groupID):
    hit_positions_df = get_hit_positions_df(eventID, groupID)

    hit_lines_dict = {}  # For each [rpID, direction, line_no] we store array of Line
    for rpID, direction, line_no in get_rp_dir_line_triplets(hit_positions_df):
        if rpID not in hit_lines_dict:
            hit_lines_dict[rpID] = {}
        if direction not in hit_lines_dict[rpID]:
            hit_lines_dict[rpID][direction] = {}

        lines_position_df = hit_positions_df[(hit_positions_df['rpID'] == rpID) &
                                             (hit_positions_df['direction'] == direction) &
                                             (hit_positions_df['line_no'] == line_no)]
        hit_lines_dict[rpID][direction][line_no] = get_silicon_hit_lines(lines_position_df)

    return hit_lines_dict
