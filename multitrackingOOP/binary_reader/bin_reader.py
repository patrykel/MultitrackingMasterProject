import numpy as np
import pandas as pd

from configuration import *

RAW_BIN_TYPE = ({
    'eventID': ('i4', 0),
    'recoId': ('H', 4),
    'armID': ('b', 6),
    'groupID': ('b', 7),
    'rpID': ('b', 8),
    'uLineSize': ('b', 9),
    'vLineSize': ('b', 10),
    'siliconID': ('b', 11),
    'direction': ('b', 12),
    'line_no': ('b', 13),
    'position': ('d', 16),
    'line_a': ('d', 24),
    'line_b': ('d', 32),
    'line_w': ('d', 40)})

NUMPY_TYPE = [('eventID', int),
              ('recoId', int),
              ('armID', int),
              ('groupID', int),
              ('rpID', int),
              ('uLineSize', int),
              ('vLineSize', int),
              ('siliconID', int),
              ('direction', int),
              ('line_no', int),
              ('position', np.double),
              ('line_a', np.double),
              ('line_b', np.double),
              ('line_w', np.double)]


def get_hits_bin_filename(fill, run, reco):
    return PROJECT_PATH + "data/hits/{0}/{1}/{0}_{1}_{2}.bin".format(fill, run, reco)


def get_hit_lines_df():
    bin_filename = get_hits_bin_filename(FILL, RUN, RECO)  # from configuration
    hits_raw = np.fromfile(bin_filename, dtype=RAW_BIN_TYPE)
    hits_numpy = hits_raw.astype(NUMPY_TYPE)
    return pd.DataFrame(hits_numpy)
