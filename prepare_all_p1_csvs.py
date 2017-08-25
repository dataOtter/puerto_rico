import wrangling_cleaning as w


def prep_all_p1(path, screenings_file='p1_screenings', hiv_file='p1_hivs', hcv_file='p1_hcvs',
                interviews_file='p1_interviews', followups_file='p1_followups', nodes_file="node_index_5_3_17"):
    """Input: General file path; names of all p1 csv files; name of nodes csv file.
    Output: Fixes all files' column labels; adds a project_id column to p1_screenings."""
    replace_with = {'COUPONID': 'rds_id'}

    path_screenings = path + screenings_file + ".csv"
    path_hiv = path + hiv_file + '.csv'
    path_hcv = path + hcv_file + '.csv'
    path_interviews = path + interviews_file + '.csv'
    path_followups = path + followups_file + '.csv'
    path_nodes = path + nodes_file + '.csv'

    w.fix_column_labels_csv(path_screenings, replace_with)
    w.fix_column_labels_csv(path_hiv, replace_with)
    w.fix_column_labels_csv(path_hcv, replace_with)
    w.fix_column_labels_csv(path_interviews, replace_with)
    w.fix_column_labels_csv(path_followups, replace_with)

    add_pid_col_to_p1_scr(path_nodes, path_screenings)


def add_pid_col_to_p1_scr(path_nodes, path_p1_screenings):
    """Input: file_path and name of each csv file to be used and modified,
    list of column labels to be used in the new sub_pid file.
    Output: Creates a subjects_pids.csv file and populates it from nodes csv file;
    adds and populates a subject_pid column to the p1_screenings.csv file."""
    x = w.get_csv_as_list(path_p1_screenings)
    scr_cols = x[0]  # column labels of p1_screenings csv as list
    scr_list = x[1:]  # data of p1_screenings csv as list

    nodes_list = w.get_csv_as_list(path_nodes)[1:]  # data of nodes csv as list
    nodes_pid_index = w.get_value_index_from_nodes_col(path_nodes, "project_id")
    nodes_rds_index = w.get_value_index_from_nodes_col(path_nodes, "rds_id")

    rds_pid = {}
    for row in nodes_list:
        if row[nodes_rds_index] != '#NULL!' and row[nodes_rds_index] != '':
            rds_pid[row[nodes_rds_index]] = row[nodes_pid_index]  # make rds number (where it exists) to pid dictionary
    #print(rds_pid)

    scr_pid_index = scr_cols.index("project_id")  # or look up col_labels[0]
    scr_rds_index = scr_cols.index("rds_id")

    w.create_csv_add_column_labels(path_p1_screenings, scr_cols)  # remove screenings file, make new one with pid column

    for row in scr_list:
        pid = rds_pid[row[scr_rds_index]]  # use rds_id from each row in screenings to get pid from rds_pid dictionary
        row[scr_pid_index] = pid  # replace empty pid entry with the retrieved pid
        #print(row)
        w.append_row_to_csv(path_p1_screenings, row)