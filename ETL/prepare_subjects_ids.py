"""Function to create and populate the subject IDs csv file."""
import constants as c
from ETL import wrangling_functions as w


def create_sub_ids_csv():
    """Input: None.
    Output: Creates subjects_ids.csv file and populates it with project_ids, rds_ids, and unique_ids."""
    path_sub_ids, path_nodes = c.SUBJECTS_IDS_PATH, c.OLD_NODES_PATH

    nodes_data = w.get_csv_as_list(path_nodes)[1:]  # data of nodes csv as list
    nodes_pid_index = w.get_index_of_file_col(path_nodes, c.LABEL_PID)
    nodes_rds_index = w.get_index_of_file_col(path_nodes, c.LABEL_RDS_ID)
    nodes_unique_index = w.get_index_of_file_col(path_nodes, c.LABEL_UNIQUE_ID)

    w.create_csv_add_column_labels(path_sub_ids, [c.LABEL_PID, c.LABEL_RDS_ID, c.LABEL_UNIQUE_ID])

    # make sure that the data is put into the correct column in subjects_ids
    # put project_id, rds_id, and unique_id from the old nodes table into the new subjects_ids table
    for row in nodes_data:
        for i in range(len(row)):
            if row[i] in c.NO_ENTRIES:
                row[i] = ''
        add_row = [row[nodes_pid_index], row[nodes_rds_index], row[nodes_unique_index]]
        w.append_row_to_csv(path_sub_ids, add_row)
