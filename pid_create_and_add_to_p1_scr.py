import wrangling_cleaning as w


def pid_create_add(file_path, pid_col_labels, node_file, scr_file, sub_pid_file):
    """Input: file_path and name of each csv file to be used and modified,
    list of column labels to be used in the new sub_pid file.
    Output: Creates a subjects_pids.csv file and populates it from nodes csv file;
    adds and populates a subject_pid column to the p1_screenings.csv file."""
    path_nodes = file_path + node_file + ".csv"
    path_p1_screenings = file_path + scr_file + ".csv"
    pid_path = file_path + sub_pid_file + ".csv"

    a = w.get_csv_as_list(path_nodes)
    nodes_cols = a[0]  # column labels of nodes csv as list
    nodes_list = a[1:]  # data of nodes csv as list

    x = w.get_csv_as_list(path_p1_screenings)
    scr_cols = x[0]  # column labels of p1_screenings csv as list
    scr_list = x[1:]  # data of p1_screenings csv as list

    w.create_csv_add_column_labels(pid_path, pid_col_labels)  # make subjects_pids csv with given column labels

    nodes_pid_index = nodes_cols.index("project_id")  # or look up col_labels[0]
    nodes_rds_index = nodes_cols.index("rds_id")

    rds_pid = {}
    for row in nodes_list:
        w.add_row_to_csv(pid_path, [row[nodes_pid_index]])  # add pids to the subjects_pids file
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
        w.add_row_to_csv(path_p1_screenings, row)


file_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"
pid_col_labels = ["project_id"]
node_file = "node_index_5_3_17"
scr_file = "p1_screenings"
sub_pid_file = "subjects_pids"
pid_create_add(file_path, pid_col_labels, node_file, scr_file, sub_pid_file)
