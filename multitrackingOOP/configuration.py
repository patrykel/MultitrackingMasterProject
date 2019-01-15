import sys


# GENERAL CONFIGURATION
FILL = int(sys.argv[1])  # 4510
RUN = int(sys.argv[2])  # 9985
RECO = int(sys.argv[3])  # 7

# PATH TO PROJECT
PROJECT_PATH = "/Users/patryklawski/Desktop/Master-Python/single/multitrackingOOP/"

# SELECT WHAT TO RUN
COMPUTE_SINGLE_TRACKS_FLAG = True
COMPUTE_MULTI_TRACKS_FLAG = True
COMPARE_UV_PROJECTIONS_WITH_SINGLE_TRACKS_FLAG = True # Only applicable when COMPUTE_SINGLE_TRACKS set to True

# CACHE CONFIGURATION
MULTI_TRACKING_CACHE = "MULTI_TRACKING_CACHE"
SINGLE_TRACKING_CACHE = "SINGLE_TRACKING_CACHE"

# FITTING ALGORITHM CONFIGURATION
class Config:
    TRANSLATION = 50000
    FIRST_Z_FROM_IP = 0  # after translation it is closest "z" to IP5, can be + or -
    LEAST_SQUARE_PARAMS_NO = 5  # least_square minimization takes (x,y,dx,dy,dz)