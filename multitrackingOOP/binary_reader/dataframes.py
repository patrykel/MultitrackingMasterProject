import pandas as pd

from binary_reader.bin_reader import *
from configuration import PROJECT_PATH

# DATA
DATAFRAMES = {}

AVG_DET_GEOM_DF = "AVG_DET_GEOM_DF"
GEOM_RP_DF = "GEOM_RP_DF"
GEOM_SILICON_DF = "GEOM_SILICON_DF"
HIT_LINES_DF = "HIT_LINES_DF"
ANALYSIS_DF = "ANALYSIS_DF"
SINGLE_HIT_EVENT_GROUP_DF = "SINGLE_HIT_EVENT_GROUP_DF"  # 3 rp hit in group
MULTI_HIT_EVENT_GROUP_DF = "MULTI_HIT_EVENT_GROUP_DF"  # 3 rp hit in group

GEOM_FILENAMES_PREFIXES = {
    4499: "2015_10_15_fill4499",
    4505: "2015_10_16_fill4505",
    4509: "2015_10_17_fill4509",
    4510: "2015_10_17_fill4510",
    4511: "2015_10_18_fill4511"
}


# FILENAMES
def get_avg_geom_filename():
    return PROJECT_PATH + "data/geom/{}/{}_avg_by_rp_direction.csv".format(FILL, GEOM_FILENAMES_PREFIXES[FILL])


def get_geom_rp_filename():
    return PROJECT_PATH + "data/geom/{}/{}_rps.csv".format(FILL, GEOM_FILENAMES_PREFIXES[FILL])


def get_geom_silicon_filename():
    return PROJECT_PATH + "data/geom/{}/{}_sensors.csv".format(FILL, GEOM_FILENAMES_PREFIXES[FILL])


# DATAFRAMES
def get_avg_geom_df():
    return pd.read_csv(get_avg_geom_filename())


def get_geom_rp_df():
    return pd.read_csv(get_geom_rp_filename())


def get_geom_silicon_df():
    return pd.read_csv(get_geom_silicon_filename())


def get_analysis_df():
    hit_lines_df = DATAFRAMES[HIT_LINES_DF]

    # RP HIT IN GROUP
    analysis_df = hit_lines_df[['eventID', 'groupID', 'rpID']] \
        .drop_duplicates() \
        .groupby(['eventID', 'groupID']) \
        .size() \
        .reset_index(name='RP_hit_in_group') \
        .set_index(['eventID', 'groupID'])

    # MAX LINE NO
    analysis_df['Max_line_no'] = hit_lines_df \
        .groupby(['eventID', 'groupID'])['line_no'] \
        .max()

    # RESETING INDEX TO INCLUDE EVENT_ID AND GROUP_ID
    analysis_df.reset_index(inplace=True)
    return analysis_df


def get_single_hit_event_group_df():
    # need to have HIT_LINES_DF in DATAFRAME dictionary
    analysis_df = DATAFRAMES[ANALYSIS_DF]

    return analysis_df.loc[(analysis_df['Max_line_no'] == 0) &
                           (analysis_df['RP_hit_in_group'] == 3)]


def get_multi_hit_event_group_df():
    analysis_df = DATAFRAMES[ANALYSIS_DF]

    return analysis_df.loc[(analysis_df['Max_line_no'] > 0) &
                           (analysis_df['RP_hit_in_group'] == 3)]


# POPULATE DATAFRAMES DICT
DATAFRAMES[AVG_DET_GEOM_DF] = get_avg_geom_df()  # from configuration
DATAFRAMES[GEOM_RP_DF] = get_geom_rp_df()
DATAFRAMES[GEOM_SILICON_DF] = get_geom_silicon_df()
DATAFRAMES[HIT_LINES_DF] = get_hit_lines_df()
DATAFRAMES[ANALYSIS_DF] = get_analysis_df()
DATAFRAMES[SINGLE_HIT_EVENT_GROUP_DF] = get_single_hit_event_group_df()
DATAFRAMES[MULTI_HIT_EVENT_GROUP_DF] = get_multi_hit_event_group_df()
