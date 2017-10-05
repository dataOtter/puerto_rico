"""Function to clean all phase 2 csv files."""
import constants as c
from ETL import wrangling_functions as w


def prep_all_p2():
    """Output: Merges all phase 2 files' unique id fragment columns, adding a unique_id column;
        adds a project_id column to p2_first_interviews.csv; adds a rds_id column to p2_second_interviews.csv."""
    path_network = c.P2_NETWORK_INTERVIEWS_PATH
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
    w.add_merged_col_to_csv(path_network, unique_id, c.NETWORK_HCV_HIV_COLS_TO_MERGE)

    # add project_id to p2_first_interviews.csv using its newly made unique_id to associate the correct project_id
    w.add_column_and_data_from_old_nodes_to_csv(path_interviews1, path_nodes,
                                                add_col_name=c.LABEL_PID, reference_col_name=unique_id)

    # add rds_id to p2_second_interviews.csv using its newly made unique_id to associate the correct rds_id
    w.add_column_and_data_from_old_nodes_to_csv(path_interviews2, path_nodes,
                                                add_col_name=c.LABEL_RDS_ID, reference_col_name=unique_id)
