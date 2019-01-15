'''
The goal of this script is to translate the hit lines.z so that:
- the nearest line to IP5 would have z = [+/-] 50000 [mm]

For such translation least square optimize works bes
'''

import numpy as np

from configuration import *


def translate_hit_lines(silicon_hit_lines):
    Config.FIRST_Z_FROM_IP = min([line.z for line in silicon_hit_lines], key=abs)
    z_sign = np.sign(Config.FIRST_Z_FROM_IP)

    for line in silicon_hit_lines:
        line.z = line.z - Config.FIRST_Z_FROM_IP + \
                 z_sign * Config.TRANSLATION


def untranslate_hit_lines(silicon_hit_lines):
    z_sign = np.sign(Config.FIRST_Z_FROM_IP)

    for line in silicon_hit_lines:
        # Take the closest one to 0, then to the original place. Other izometrically.
        line.z = line.z - z_sign * Config.TRANSLATION + Config.FIRST_Z_FROM_IP
