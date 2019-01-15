from totem_comparator.submission.slurm_comparator_config import *


def get_python_job_invocation(fill, run, reco_idx):
    return "python3 /net/archive/groups/plggdiamonds/TOTEM-2015-data/CODE/RECONSTRUCTION" \
           "/totem_comparator/totem_single_comparator.py {} {} {}\n".format(fill, run, reco_idx)


def get_job_script(fill, run, first_reco_idx, last_reco_idx):
    script_content = "#!/bin/bash\n" + \
                     "echo \"loading python3...\"\n" + \
                     "module add plgrid/tools/python/3.6.0\n" + \
                     "echo \"Running main.py...\"\n" + \
                     "date\n" + \
                     "\n"

    for reco_idx in range(first_reco_idx, last_reco_idx + 1):
        script_content = script_content + get_python_job_invocation(fill, run, reco_idx)
        script_content = script_content + "date\n"

    return script_content


def get_submission_line(fill, run, first_reco_idx, last_reco_idx):
    submission_line = "sbatch " + \
                      "-J {2}-{3}_{1}_{0}_TOTEM-COMPARE-SINGLE ".format(fill, run, first_reco_idx, last_reco_idx) + \
                      "-N 1 " + \
                      "--ntasks-per-node=1 " + \
                      "--mem-per-cpu=4GB " + \
                      "--time={}:00:00 ".format(JOB_TIME_HOURS) + \
                      "-A intdata " + \
                      "--partition plgrid " + \
                      "--output=\"output/{}_{}_{}-{}_output.out\" ".format(fill, run, first_reco_idx, last_reco_idx) + \
                      "--error=\"error/{}_{}_{}-{}_error.err\" ".format(fill, run, first_reco_idx, last_reco_idx) + \
                      "jobs/compare_single_{}_{}_{}-{}.sh".format(fill, run, first_reco_idx, last_reco_idx)

    return submission_line


def get_job_filename(fill, run, first_reco_idx, last_reco_idx):
    return "generated/jobs/compare_single_{}_{}_{}-{}.sh".format(fill, run, first_reco_idx, last_reco_idx)


def get_submission_filename():
    return "generated/submit_jobs_{}_{}.sh".format(FILL, RUN)


reco_numbers = [1554, 2, 1001, 1025, 1028, 1031, 1034, 1037, 1040, 1043, 1046, 1049, 1052, 1055, 1058, 1061, 1064, 1067,
                1070, 1073, 1076, 1079, 1082, 1085, 1088, 1091, 1094, 1097, 1100, 1103, 1106, 1115, 1118, 1121, 1124,
                1127, 1130, 1133, 1136, 1139, 1142, 1145, 1148, 1151, 1154, 1157, 1160, 1163, 1166, 1169, 1172, 1175,
                1178, 1181, 1184, 1187, 1190, 1193, 1196, 1199, 11, 1202, 1205, 1208, 1211, 1214, 1217, 1220, 1223,
                1226, 1229, 122, 1232, 1235, 1244, 1247, 1250, 1253, 1256, 125, 1268, 1271, 1289, 128, 1292, 1295, 1298,
                1301, 1304, 1307, 1310, 1313, 1316, 1319, 131, 1322, 1325, 1328, 1331, 1334, 1337, 1340, 1343, 1346,
                1349, 1352, 1355, 1367, 1370, 1373, 1376, 1379, 1382, 1385, 1388, 1391, 1394, 1397, 1400, 1403, 1406,
                1409, 1412, 1430, 1433, 1436, 1439, 1442, 1445, 1448, 1451, 1454, 1457, 1460, 1463, 1466, 1469, 1472,
                1475, 1478, 1481, 1484, 1487, 1490, 1493, 1499, 14, 1502, 1505, 1508, 1511, 1514, 1517, 1520, 1523,
                1526, 1529, 152, 1532, 1535, 1538, 1541, 1544, 1547, 155, 158, 161, 170, 173, 176, 179, 17, 182, 185,
                205, 215, 218, 245, 248, 251, 254, 257, 260, 263, 266, 269, 272, 275, 278, 281, 284, 287, 290, 293, 32,
                338, 341, 344, 347, 350, 353, 356, 359, 35, 362, 365, 368, 371, 374, 377, 380, 383, 386, 38, 395, 398,
                401, 404, 41, 431, 434, 437, 440, 443, 446, 449, 44, 452, 455, 458, 461, 464, 467, 470, 473, 476, 479,
                47, 482, 485, 488, 491, 494, 497, 500, 503, 506, 509, 50, 512, 515, 518, 521, 524, 527, 530, 533, 536,
                539, 53, 542, 545, 548, 551, 554, 557, 560, 563, 566, 569, 56, 572, 575, 578, 581, 584, 587, 590, 593,
                596, 59, 5, 617, 620, 623, 626, 629, 62, 644, 647, 650, 653, 656, 659, 65, 662, 665, 668, 671, 674, 677,
                680, 683, 686, 689, 68, 692, 695, 698, 701, 704, 707, 710, 713, 716, 719, 71, 722, 725, 728, 731, 734,
                737, 740, 743, 746, 749, 752, 755, 758, 761, 764, 767, 770, 773, 776, 779, 77, 782, 785, 788, 791, 794,
                797, 800, 803, 806, 809, 80, 811, 812, 815, 818, 821, 824, 827, 830, 833, 836, 838, 839, 83, 841, 842,
                844, 845, 847, 848, 850, 851, 853, 854, 856, 857, 859, 860, 862, 863, 865, 866, 868, 869, 86, 871, 872,
                874, 875, 877, 878, 880, 881, 883, 884, 886, 887, 889, 890, 893, 896, 899, 89, 8, 902, 904, 905, 907,
                908, 910, 911, 914, 917, 920, 923, 926, 929, 92, 932, 935, 938, 941, 944, 947, 959, 95, 962, 965, 968,
                971, 974, 977, 980, 983, 986, 989, 992, 995, 998]

submission_filename = get_submission_filename()
with open(submission_filename, "w") as submission_file:
    print("#!/bin/bash", file=submission_file)

    for first_reco_idx in reco_numbers:
        # Add invocation
        last_reco_idx = first_reco_idx + RECO_PER_JOB - 1
        if last_reco_idx > MAX_RECO:
            last_reco_idx = MAX_RECO

        submission_line = get_submission_line(FILL, RUN, first_reco_idx, last_reco_idx)
        print(submission_line, file=submission_file)

        # Add job with several python invocations
        job_script = get_job_script(FILL, RUN, first_reco_idx, last_reco_idx)
        job_filename = get_job_filename(FILL, RUN, first_reco_idx, last_reco_idx)
        with open(job_filename, "w") as job_file:
            print(job_script, file=job_file)
