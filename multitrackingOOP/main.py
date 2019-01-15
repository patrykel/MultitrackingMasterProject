import time

from single_tracking.algorithm import run_single_tracking
from algorithm_multi import run_multi_tracking
from totem_single_comparator import run_comparison

from configuration import COMPUTE_SINGLE_TRACKS_FLAG
from configuration import COMPUTE_MULTI_TRACKS_FLAG
from configuration import COMPARE_UV_PROJECTIONS_WITH_SINGLE_TRACKS_FLAG


if COMPUTE_SINGLE_TRACKS_FLAG:

    single_tracking_start_time = time.time()
    run_single_tracking()
    single_tracking_total_time = time.time() - single_tracking_start_time
    print("Single tracking computing time: {}".format(single_tracking_total_time))

    if COMPARE_UV_PROJECTIONS_WITH_SINGLE_TRACKS_FLAG:
        comparing_start_time = time.time()
        run_comparison()
        comparing_total_time = time.time() - comparing_start_time
        print("Comparing time: {}".format(comparing_total_time))

if COMPUTE_MULTI_TRACKS_FLAG:
    multi_start_time = time.time()
    run_multi_tracking()
    multi_total_time = time.time() - multi_start_time
    print("Multi tracking computing time: {}".format(multi_total_time))

