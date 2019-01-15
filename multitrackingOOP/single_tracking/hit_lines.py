from binary_reader.dataframes import *
from geometry_classes.Line import *

'''
HIT POSITION DF
'''


def get_hit_positions_df(eventID, groupID):
    hit_positions_df = DATAFRAMES[HIT_LINES_DF]  # all hit positions actually

    # TODO: please time it with and without index on it :)
    return hit_positions_df[(hit_positions_df['eventID'] == eventID) &
                            (hit_positions_df['groupID'] == groupID)]


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


def get_hit_lines(eventID, groupID):
    hit_lines = []

    hit_positions_df = get_hit_positions_df(eventID, groupID)
    silicon_hit_lines = get_silicon_hit_lines(hit_positions_df)
    return silicon_hit_lines
