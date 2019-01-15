from multi_tracking.submission.slurm_config import *


def get_python_job_invocation(fill, run, reco_idx):
    return "python3 /net/archive/groups/plggdiamonds/TOTEM-2015-data" + \
           "/CODE/RECONSTRUCTION/multi_tracking/algorithm_multi.py {} {} {}\n".format(fill, run, reco_idx)


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
                      "-J {2}-{3}_{1}_{0}_TOTEM-MULTI ".format(fill, run, first_reco_idx, last_reco_idx) + \
                      "-N 1 " + \
                      "--ntasks-per-node=1 " + \
                      "--mem-per-cpu=4GB " + \
                      "--time={}:00:00 ".format(JOB_TIME_HOURS) + \
                      "-A intdata " + \
                      "--partition plgrid " + \
                      "--output=\"output/{}_{}_{}-{}_output.out\" ".format(fill, run, first_reco_idx, last_reco_idx) + \
                      "--error=\"error/{}_{}_{}-{}_error.err\" ".format(fill, run, first_reco_idx, last_reco_idx) + \
                      "jobs/multi_tracking_{}_{}_{}-{}.sh".format(fill, run, first_reco_idx, last_reco_idx)

    return submission_line


def get_job_filename(fill, run, first_reco_idx, last_reco_idx):
    return "generated/jobs/multi_tracking_{}_{}_{}-{}.sh".format(fill, run, first_reco_idx, last_reco_idx)


def get_submission_filename():
    return "generated/submit_jobs_{}_{}.sh".format(FILL, RUN)


submission_filename = get_submission_filename()
with open(submission_filename, "w") as submission_file:
    print("#!/bin/bash", file=submission_file)

    for first_reco_idx in range(MIN_RECO, MAX_RECO + 1, RECO_PER_JOB):
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
