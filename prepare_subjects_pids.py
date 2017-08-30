import wrangling_functions as w


def create_sub_pid_csv(path, node_file="node_index_5_3_17",
                       sub_pid_file="subjects_pids", pid_col_labels=["project_id"]):
    """Input: General file path; node csv file name, subjects pids csv file name and its column labels.
    Output: Creates subjects_pids.csv file and populates it with project_ids."""
    path_pid = w.get_full_path(path, sub_pid_file)
    path_nodes = w.get_full_path(path, node_file)

    nodes_data = w.get_csv_as_list(path_nodes)[1:]  # data of nodes csv as list
    nodes_pid_index = w.get_index_of_file_col(path_nodes, "project_id")

    w.create_csv_add_column_labels(path_pid, pid_col_labels)  # make subjects_pids csv with given column labels

    for row in nodes_data:
        w.append_row_to_csv(path_pid, [row[nodes_pid_index]])  # add pids to the subjects_pids file
