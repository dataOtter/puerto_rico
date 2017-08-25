import wrangling_cleaning as w


def create_sub_pid_csv(file_path, node_file="node_index_5_3_17",
                       sub_pid_file="subjects_pids", pid_col_labels=["project_id"]):
    """Input: General file path; node csv file name, subjects pids csv file name and its column labels.
    Output: Creates subjects_pids.csv file and populates it with project_ids."""
    path_pid = file_path + sub_pid_file + ".csv"
    path_nodes = file_path + node_file + ".csv"

    nodes_list = w.get_csv_as_list(path_nodes)[1:]  # data of nodes csv as list
    nodes_pid_index = w.get_value_index_from_nodes_col(path_nodes, "project_id")

    w.create_csv_add_column_labels(path_pid, pid_col_labels)  # make subjects_pids csv with given column labels

    for row in nodes_list:
        w.append_row_to_csv(path_pid, [row[nodes_pid_index]])  # add pids to the subjects_pids file
