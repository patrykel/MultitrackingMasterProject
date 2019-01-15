from binary_reader.dataframes import AVG_DET_GEOM_DF
from binary_reader.dataframes import DATAFRAMES
from binary_reader.dataframes import GEOM_RP_DF
from geometry_classes.Point3D import Point3D

U_DIRECTION_NUMBER = 117
V_DIRECTION_NUMBER = 118

U_DIRECTION_CHAR = 'u'
V_DIRECTION_CHAR = 'v'

'''
GET TOTEM HIT POINT
'''

# UV_COORDINATE_SYSTEM_SKELETON = UVCoordinateSystemSkeleton()
#
#
# def get_totem_hit_point(rpID, totem_group_hits_df):
#     totem_rp_hits_df = get_totem_rp_hits_df(rpID, totem_group_hits_df)
#     avg_det_geom_df = DATAFRAMES[AVG_DET_GEOM_DF]
#     geom_rp_df = DATAFRAMES[GEOM_RP_DF]
#
#     UV_COORDINATE_SYSTEM_SKELETON.reset()
#     UV_COORDINATE_SYSTEM_SKELETON.setup(rpID, totem_rp_hits_df, avg_det_geom_df, geom_rp_df)
#     return UV_COORDINATE_SYSTEM_SKELETON.get_pt0()


'''
We need to get:
- detector u direction
- detector v direction
- z
- Avg x y
'''

'''
ENTRY #2 RP ID based on 2-row totem_rp_uv_lines_df [(RP_ID, 117(u)), (RP_ID, 118(v))]
'''


def get_rp_id(totem_rp_uv_lines_df):
    return totem_rp_uv_lines_df.rpID.iloc[0]


'''
ROMAN POT Z
'''


def get_rp_z_mm(rpID):
    geom_rp_df = DATAFRAMES[GEOM_RP_DF]
    goem_rp_row = geom_rp_df.loc[geom_rp_df['rpID'] == rpID].iloc[0]
    return goem_rp_row['z'] * 1000


'''
DX DY for given direction within one RP
'''


def get_uv_dx_dy(rpID, direction_char=U_DIRECTION_CHAR):
    avg_det_geom_df = DATAFRAMES[AVG_DET_GEOM_DF]
    avg_direction_df = avg_det_geom_df.loc[(avg_det_geom_df['rpId'] == rpID) &
                                           (avg_det_geom_df['direction'] == direction_char)].iloc[0]
    dx = avg_direction_df['dx']
    dy = avg_direction_df['dy']

    return dx, dy


'''
LINE A B for given direction within one RP_ID
'''


def get_line_uv_ab(totem_rp_uv_lines_df, direction_number=V_DIRECTION_NUMBER):
    totem_rp_uv_line_row = totem_rp_uv_lines_df.loc[totem_rp_uv_lines_df['direction'] == direction_number].iloc[0]
    line_a = totem_rp_uv_line_row['line_a']
    line_b = totem_rp_uv_line_row['line_b']
    return line_a, line_b


'''
ENTRY # 1
'''


def get_totem_hit_point(totem_rp_uv_lines_df):
    rpID = get_rp_id(totem_rp_uv_lines_df)
    rp_z = get_rp_z_mm(rpID)
    u_dx, u_dy = get_uv_dx_dy(rpID, direction_char=U_DIRECTION_CHAR)
    v_dx, v_dy = get_uv_dx_dy(rpID, direction_char=V_DIRECTION_CHAR)
    line_u_a, line_u_b = get_line_uv_ab(totem_rp_uv_lines_df, direction_number=U_DIRECTION_NUMBER)
    line_v_a, line_v_b = get_line_uv_ab(totem_rp_uv_lines_df, direction_number=V_DIRECTION_NUMBER)

    p_x = line_u_b * u_dx + line_v_b * v_dx
    p_y = line_u_b * u_dy + line_v_b * v_dy

    return Point3D(p_x, p_y, rp_z)
