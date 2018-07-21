"""Function to clean all phase 2 csv files."""
import constants as c
from ETL import wrangling_functions as w


def prep_all_p2():
    """Output: Merges all phase 2 files' unique id fragment columns, adding a unique_id column;
    adds a project_id column to p2_first_interviews.csv; adds a rds_id column to p2_second_interviews.csv;
    creates the network supplement extract file."""
    path_old_net = c.P2_DEPRECATED_NET_SUPS_PATH
    path_net_sup_extract = c.P2_NET_SUPS_EXTRACT_PATH
    path_hiv = c.P2_HIVS_PATH
    path_hcv = c.P2_HCVS_PATH
    path_interviews1 = c.P2_FIRST_INTERVIEWS_PATH
    path_interviews2 = c.P2_SECOND_INTERVIEWS_PATH
    path_nodes = c.OLD_NODES_PATH

    # use unique_id segments to make unique_id and add it to each p2 csv file
    unique_id = c.LABEL_UNIQUE_ID
    w.add_merged_col_to_csv(path_hiv, unique_id, c.NETWORK_HCV_HIV_COLS_TO_MERGE)
    w.add_merged_col_to_csv(path_hcv, unique_id, c.NETWORK_HCV_HIV_COLS_TO_MERGE)
    w.add_merged_col_to_csv(path_interviews1, unique_id, c.INTERVIEWS1_COLS_TO_MERGE)
    w.add_merged_col_to_csv(path_interviews2, unique_id, c.INTERVIEWS2_COLS_TO_MERGE)

    # extract P2SF and P2NS1 columns from the deprecated network supplement and get rds ids
    make_net_sup_extract_file(path_old_net, path_net_sup_extract)

    # add project_id to p2_first_interviews.csv using its newly made unique_id to associate the correct project_id
    w.add_column_and_data_from_old_nodes_to_csv(path_interviews1, path_nodes,
                                                add_col_name=c.LABEL_PID, reference_col_name=unique_id)

    # add rds_id to p2_second_interviews.csv using its newly made unique_id to associate the correct rds_id
    w.add_column_and_data_from_old_nodes_to_csv(path_interviews2, path_nodes,
                                                add_col_name=c.LABEL_RDS_ID, reference_col_name=unique_id)


def add_unique_id_to_net_sup_edges(path_net_sup_edges):
    """Input: File path of network supplement edges.
    Output: Adds a unique ID column to the network supplement edges file."""
    pids_from_subs_ids = w.get_data_from_one_col_as_list(c.SUBJECTS_IDS_PATH, c.LABEL_PID)
    unique_ids_from_subs_ids = w.get_data_from_one_col_as_list(c.SUBJECTS_IDS_PATH, c.LABEL_UNIQUE_ID)

    net_sup_edges = w.get_csv_as_list(path_net_sup_edges)
    net_sup_edges_data = net_sup_edges[1:]
    net_sup_edges_cols = net_sup_edges[:1][0]
    net_sup_edges_cols.append(c.LABEL_UNIQUE_ID)
    # make temp file to add unique ID column
    w.create_csv_add_column_labels(c.TEMP_FILE_PATH, net_sup_edges_cols)

    pid_index_net_sup_edges = w.get_index_of_file_col(path_net_sup_edges, c.LABEL_SENDER_PID)

    for row in net_sup_edges_data:
        # get index of this row's project ID in the subjects_ids.csv
        subs_ids_index = pids_from_subs_ids.index(row[pid_index_net_sup_edges])
        unique_id = unique_ids_from_subs_ids[subs_ids_index]
        row.append(unique_id)
        # append the matching unique ID to the row and to the temp file
        w.append_row_to_csv(c.TEMP_FILE_PATH, row)

    w.rename_csv(c.TEMP_FILE_PATH, path_net_sup_edges)  # replace the previous file with the temp file


def make_net_sup_extract_file(path_old_net, path_net_sup_extract):
    """Input: File path of deprecated network supplement and new net sup extract.
    Output: Extracts P2SF and P2NS1 columns from deprecated net sup, gets rds ids, and makes net sup extract file."""
    # make unique id column in deprecated net sup file
    w.add_merged_col_to_csv(path_old_net, c.LABEL_UNIQUE_ID, c.NETWORK_HCV_HIV_COLS_TO_MERGE)

    unique_ids_from_subs_ids = w.get_data_from_one_col_as_list(c.SUBJECTS_IDS_PATH, c.LABEL_UNIQUE_ID)
    unique_ids_from_depr_net_sup = w.get_data_from_one_col_as_list(path_old_net, c.LABEL_UNIQUE_ID)

    subs_ids_data = w.get_csv_as_list(c.SUBJECTS_IDS_PATH)[1:]
    depr_net_sup_data = w.get_csv_as_list(path_old_net)[1:]

    w.create_csv_add_column_labels(path_net_sup_extract, [c.LABEL_PID, c.LABEL_P2SF, c.LABEL_P2NS1, c.LABEL_UNIQUE_ID])

    pid_index_subs_ids = w.get_index_of_file_col(c.SUBJECTS_IDS_PATH, c.LABEL_PID)
    P2SF_index_depr_net_sup = w.get_index_of_file_col(path_old_net, c.LABEL_P2SF)
    P2NS1_index_depr_net_sup = w.get_index_of_file_col(path_old_net, c.LABEL_P2NS1)

    for i in range(len(unique_ids_from_depr_net_sup)):
        unique_id = unique_ids_from_depr_net_sup[i]
        try:
            # try to get the row index of this unique id in the subjects ids file
            subs_ids_row_index = unique_ids_from_subs_ids.index(unique_id)
            # get that row from subjects ids and get its rds id column entry
            pid = subs_ids_data[subs_ids_row_index][pid_index_subs_ids]
            # get current row from depr_net_sup to fetch its P2SF and P2NS1 columns entries
            P2SF = depr_net_sup_data[i][P2SF_index_depr_net_sup]
            P2NS1 = depr_net_sup_data[i][P2NS1_index_depr_net_sup]
            # append the new row to the net_sup_extract file
            w.append_row_to_csv(path_net_sup_extract, [pid, P2SF, P2NS1, unique_id])

        except ValueError:
            print(unique_id + " not found in subjects_ids.csv")
            pass
