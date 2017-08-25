import csv
import wrangling_cleaning as w

def create_pid_table_add_pid_to_p1_screenings(file_path):
    path_nodes = file_path + "node_index_5_3_17.csv"
    path_p1_screenings = file_path + "p1_screenings.csv"

    nodes_list = w.get_csv_as_list(path_nodes)[1:]

    x = w.get_csv_as_list(path_p1_screenings)
    scr_cols = x[0]
    scr_list = x[1:]

    pid_path = file_path + "subjects_pids.csv"
    col_labels = ["project_id"]
    w.create_csv_add_column_labels(pid_path, col_labels)

    rds_pid = {}
    for row in nodes_list:
        #write to pid file/table
        if row[2] != '#NULL!':
            rds_pid[row[2]] = row[0]

    print(rds_pid)

    scr_rds = []
    for row in scr_list:
        scr_rds.append(row[0])

    print(scr_rds)

    '''for pid, rds in rds_pid.items():
        if rds in scr_rds:'''


file_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"
create_pid_table_add_pid_to_p1_screenings(file_path)