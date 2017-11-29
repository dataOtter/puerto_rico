"""Function to create and populate the phase 1/phase 2 overlap csv file."""
import constants as c
from ETL import wrangling_functions as w


def create_p1_p2_overlaps():
    """Input: None.
    Output: Create the overlap file with entries for every participant who was present
    in both p1_screenings and p2_network_interviews; populates it with unique id, project id, rds id."""
    path_screenings = c.P1_SCREENINGS_PATH
    path_network = c.P2_NET_SUPS_EXTRACT_PATH
    path_nodes = c.OLD_NODES_PATH
    path_overlap = c.P1_P2_OVERLAPS_PATH

    pid, rds, unique = c.LABEL_PID, c.LABEL_RDS_ID, c.LABEL_UNIQUE_ID
    w.create_csv_add_column_labels(path_overlap, [pid, rds, unique])

    # get rds_ids from p1_screenings and unique_ids from p2_network_interviews
    screening_rds_id_data = w.get_data_from_one_col_as_list(path_screenings, rds)
    net_unique_id_data = w.get_data_from_one_col_as_list(path_network, unique)

    # makes dictionaries from unique_ids to rds_ids and from unique_ids to pids, extracted from the old nodes files
    unique_to_rds_dict = w.get_no_null_entries_dict_from_csv(path_nodes, unique, rds)
    unique_to_pid_dict = w.get_no_null_entries_dict_from_csv(path_nodes, unique, pid)

    for unique_id, rds_id in unique_to_rds_dict.items():  # for every unique_id/rds_id pair that exists in whole dataset
        try:  # try to remove the unique_id from p2_network_interviews
            net_unique_id_data.remove(unique_id)
        except ValueError:  # if it does not exist in p2_netowrk_interviews,
            continue  # do not add it to the overlap file and try the next unique_id/rds_id pair
        try:  # try to remove the rds_id from p1_screenings
            screening_rds_id_data.remove(rds_id)
        except ValueError:  # if it does not exist in p1_screenings,
            continue  # do not add it to the overlap file and try the next unique_id/rds_id pair
        p_id = unique_to_pid_dict[unique_id]  # if unique_id/rds_id exist in p2/p1 respectively, get the associated pid
        row = [p_id, rds_id, unique_id]
        w.append_row_to_csv(path_overlap, row)  # add this p1/p2 overlap row of ids to the overlap file
