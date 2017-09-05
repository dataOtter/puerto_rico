import wrangling_functions as w
import constants as c

def create_p1_p2_overlaps(path, p1_screenings_file='p1_screenings', p2_network_file='p2_network_interviews',
                          nodes_file=c.NODES_FILE, overlap_file='p1_p2_overlaps'):
    """Input: General file path; names of p1_screenings, p2_network_interviews, nodes, p1_p2_overlaps file.
    Output: Create the overlap file with entries for every participant who was present
    in both p1_screenings and p2_network_interviews; populates it with unique id, project id, rds id."""
    pid, rds, unique = 'project_id', 'rds_id', 'unique_id'

    path_screenings = w.get_full_path(path, p1_screenings_file)
    path_network = w.get_full_path(path, p2_network_file)
    path_nodes = w.get_full_path(path, nodes_file)
    path_overlap = w.get_full_path(path, overlap_file)

    w.create_csv_add_column_labels(path_overlap, [unique, rds, pid])

    scr_rds_data = w.get_data_from_one_col_as_list(path_screenings, rds)
    net_unique_data = w.get_data_from_one_col_as_list(path_network, unique)

    unique_to_rds_dict = w.get_no_null_entries_dict_from_csv(path_nodes, unique, rds)
    unique_to_pid_dict = w.get_no_null_entries_dict_from_csv(path_nodes, unique, pid)

    for unique_id, rds_id in unique_to_rds_dict.items():
        try:
            net_unique_data.remove(unique_id)
        except ValueError:
            continue
        try:
            scr_rds_data.remove(rds_id)
        except ValueError:
            continue
        p_id = unique_to_pid_dict[unique_id]
        row = [unique_id, rds_id, p_id]
        w.append_row_to_csv(path_overlap, row)

#create_p1_p2_overlaps("C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\")
