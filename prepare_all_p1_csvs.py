import wrangling_functions as w


def prep_all_p1(path, screenings_file='p1_screenings', hiv_file='p1_hivs', hcv_file='p1_hcvs',
                interviews_file='p1_interviews', followups_file='p1_followups', nodes_file="node_index_5_3_17"):
    """Input: General file path; names of all p1 csv files; name of nodes csv file.
    Output: Fixes all files' column labels; adds a project_id column to p1_screenings."""
    replace_with = {'COUPONID': 'rds_id'}

    path_screenings = w.get_full_path(path, screenings_file)
    path_hiv = w.get_full_path(path, hiv_file)
    path_hcv = w.get_full_path(path, hcv_file)
    path_interviews = w.get_full_path(path, interviews_file)
    path_followups = w.get_full_path(path, followups_file)
    path_nodes = w.get_full_path(path, nodes_file)

    w.fix_column_labels_csv(path_screenings, replace_with)
    w.fix_column_labels_csv(path_hiv, replace_with)
    w.fix_column_labels_csv(path_hcv, replace_with)
    w.fix_column_labels_csv(path_interviews, replace_with)
    w.fix_column_labels_csv(path_followups, replace_with)

    w.add_column_and_data_from_nodes_to_csv(path_screenings, path_nodes,
                                            add_col_name='project_id', reference_col_name="rds_id")

#prep_all_p1("C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\")
