from binary_reader.dataframes import *
from common.silicon_detector import *
from configuration import *

'''
CREATE SILICON DETECTOR OBJECT
'''

SILICON_DETECTOR_CACHE = {}


def get_silicon_info(silicon_id):
    geom_silicon_df = DATAFRAMES[GEOM_SILICON_DF]
    return geom_silicon_df.loc[(geom_silicon_df['detId'] == silicon_id)].iloc[0]


def get_rp_silicon(silicon_id):
    if silicon_id in SILICON_DETECTOR_CACHE:
        return SILICON_DETECTOR_CACHE[silicon_id]

    silicon_info = get_silicon_info(silicon_id)
    silicon_center = Point2D(x=silicon_info['x'], y=silicon_info['y'])
    silicon_readout_direction = Direction2D(dx=silicon_info['dx'], dy=silicon_info['dy'])
    silicon_detector = SiliconDetector(silicon_center, silicon_readout_direction, silicon_id)

    SILICON_DETECTOR_CACHE[silicon_id] = silicon_detector
    return silicon_detector


'''
GET POINT (X,Y) WHERE TRACK PASSES THROUGH DETECTOR
    Track starts at z = Config.FIRST_Z_FROM_IP
    Detector info stores real "z" of detector in [m]
'''


def get_track_hit_point(silicon_id, track_line):
    silicon_info = get_silicon_info(silicon_id)

    z_to_move = silicon_info['z'] * 1000 - Config.FIRST_Z_FROM_IP
    move_coefficient = z_to_move / track_line.dz

    track_hit_point = Point2D(x=track_line.x + move_coefficient * track_line.dx,
                              y=track_line.y + move_coefficient * track_line.dy)

    return track_hit_point


'''
[ENTRY] CHECK WHETHER TRACK GOES THROUGH SILICON DETECTOR
'''


def detector_contains_track(silicon_id, track_line):
    silicon_detector = get_rp_silicon(silicon_id)
    track_hit_point = get_track_hit_point(silicon_id, track_line)
    return silicon_detector.contains(track_hit_point)
