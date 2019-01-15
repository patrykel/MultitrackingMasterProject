from common.detector_contain_track_test import *

SIGMA = 0.0659 / np.sqrt(2)

DETECTOR_GROUP_MAP = {
    1: "L-TOP",
    2: "L-BOT",
    3: "L-HOR",
    4: "R-TOP",
    5: "R-BOT",
    6: "R-HOR"
}


def get_group_name(group_id):
    return DETECTOR_GROUP_MAP[group_id]


'''
DISTANCES
'''


def get_distances(track_line, silicon_hit_lines):
    return [track_line.distance(line) for line in silicon_hit_lines]


def get_dist_sum(track_line, silicon_hit_lines):
    distances = get_distances(track_line, silicon_hit_lines)
    return sum(distances)


def get_dist_max(track_line, silicon_hit_lines):
    distances = get_distances(track_line, silicon_hit_lines)
    return max(distances)


'''
CHI_2
'''


def get_chi2(track_line, silicon_hit_lines):
    return sum([(track_line.distance(hit_line) / SIGMA) ** 2 for hit_line in silicon_hit_lines])


def get_chi2_N(track_line, silicon_hit_lines):
    return get_chi2(track_line, silicon_hit_lines) / (len(silicon_hit_lines) - Config.LEAST_SQUARE_PARAMS_NO)


'''
ATAN
'''


def get_mili_rad_angle(da, dz):
    return 1000 * np.arctan(da / dz)


'''
INSIDE SILICON TEST
'''


def get_silicon_id_list(silicon_hit_lines):
    return [line.silicon_id for line in silicon_hit_lines]


def get_det_with_track_list(silicon_id_list, track_line):
    return [silicon_id for silicon_id in silicon_id_list
            if detector_contains_track(silicon_id, track_line)]


def get_tracks_in_det_no(track_line, silicon_hit_lines):
    silicon_id_list = get_silicon_id_list(silicon_hit_lines)
    det_with_track = get_det_with_track_list(silicon_id_list, track_line)

    return len(det_with_track)


'''
MAIN STATISTICS
'''


def get_track_statistics(track_line, silicon_hit_lines):
    dist_max = get_dist_max(track_line, silicon_hit_lines)
    dist_sum = get_dist_sum(track_line, silicon_hit_lines)
    dist_avg = dist_sum / len(silicon_hit_lines)
    chi2 = get_chi2(track_line, silicon_hit_lines)
    chi2_N = get_chi2_N(track_line, silicon_hit_lines)
    dx_dz_angle = get_mili_rad_angle(track_line.dx, track_line.dz)
    dy_dz_angle = get_mili_rad_angle(track_line.dy, track_line.dz)
    tracks_in_det_no = get_tracks_in_det_no(track_line, silicon_hit_lines)
    tracks_out_det_no = len(silicon_hit_lines) - tracks_in_det_no

    return [dist_max, dist_sum, dist_avg, chi2, chi2_N, dx_dz_angle, dy_dz_angle,
            tracks_in_det_no, tracks_out_det_no]
