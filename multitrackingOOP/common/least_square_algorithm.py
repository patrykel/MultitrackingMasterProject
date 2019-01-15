'''
Compute track_line based on silicon_hit_lines.
Silicon_hit_lines are translated to [+/-] 50m
'''

from scipy.optimize import least_squares

from common.hit_lines_translation import *
from geometry_classes.Line import *

HIT_LINES = []

'''
TODO: check if this code is correct
'''


def get_seed_x0(silicon_hit_lines):
    z_sign = np.sign(silicon_hit_lines[0].z)

    x = 0.0
    y = 0.0
    dx = 0.009999749997
    dy = 0.009999749997
    dz = 0.9999 * z_sign

    return [x, y, dx, dy, dz]


'''
TODO: check if this code is correct
'''


def get_bounds():
    x_lower, x_upper = -100.0, 100.0
    y_lower, y_upper = -100.0, 100.0
    dir_lower, dir_upper = -1.0, 1.0

    lower_bounds = [x_lower, y_lower, dir_lower, dir_lower, dir_lower]
    upper_bounds = [x_upper, y_upper, dir_upper, dir_upper, dir_upper]

    return (lower_bounds, upper_bounds)


'''
CORE OF OUR MINIMIZATION
'''


def objective(params):
    x, y, dx, dy, dz = params
    line = Line(x=x, y=y, dx=dx, dy=dy, dz=dz)  # Assume z = 0
    return np.sum([line.distance(other) for other in HIT_LINES])  # Sum of distances


'''
MOVE TRACK BEGINNING TO FIRST DETECTOR "z" --> [+/- 50m] (if TRANSLATED = 50m)
'''


def normalize_point(track_line):
    z_to_move = np.sign(Config.FIRST_Z_FROM_IP) * Config.TRANSLATION
    move_coefficient = z_to_move / track_line.dz

    track_line.x = track_line.x + move_coefficient * track_line.dx
    track_line.y = track_line.y + move_coefficient * track_line.dy
    track_line.z = Config.FIRST_Z_FROM_IP


'''
ENTRY
'''


def compute_track_line(silicon_hit_lines):
    # Translate so we operate in a different coordinate system. Track begins at z = 0mm, Closest line at 50 000mm = 50m
    translate_hit_lines(silicon_hit_lines)  # Translated z. So the closest z to IP5 =  [-/+] 50m = [+/-] 50 000 mm

    # Constraints
    seed_x0 = get_seed_x0(silicon_hit_lines)
    bounds = get_bounds()

    # Computing solution
    global HIT_LINES
    HIT_LINES = silicon_hit_lines
    solution = least_squares(objective, seed_x0, bounds=bounds, jac='2-point', method='trf')
    track_line = Line(params=solution.x)  # solution.x = [x, y, dx, dy, dz]

    # Normalization
    track_line.normalize_line_vector()  # |[dx, dy, dz]| = 1.0
    normalize_point(track_line)  # We assumed silicon_hit_lines starts from [+/-] 50m. Move point to real "z" of first line.
    # We want track_line.z = FIRST_Z_FROM_IP
    untranslate_hit_lines(silicon_hit_lines)

    return track_line
