import wrangling_functions as w


def prep_all_p2(path, network_file='p2_network_interviews', hiv_file='p2_hivs', hcv_file='p2_hcvs',
                interviews1_file='p2_first_interviews', interviews2_file='p2_second_interviews',
                nodes_file="node_index_5_3_17"):
    """Input: General file path; names of all p2 csv files; name of nodes csv file.
        Output: Merges all files' unique id fragment columns, adding a unique_id column;
        adds a project_id column to p2_first_interviews.csv; adds a rds_id column to p2_second_interviews.csv."""
    # get all p2 csv file paths
    path_network = w.get_full_path(path, network_file)
    path_hiv = w.get_full_path(path, hiv_file)
    path_hcv = w.get_full_path(path, hcv_file)
    path_interviews1 = w.get_full_path(path, interviews1_file)
    path_interviews2 = w.get_full_path(path, interviews2_file)
    path_nodes = w.get_full_path(path, nodes_file)

    # get all unique_id segments column titles
    network_hcv_hiv_cols_to_merge = ['P2FLFN', 'P2FLBM', 'P2BD', 'P2FLMN', 'P2FLSN', 'P2EDAD']
    interviews1_cols_to_merge = ['P2FIFLFN', 'P2FIFLBM', 'P2FIBD', 'P2FIFLMN', 'P2FIFLSN', 'P2FIEDAD']
    interviews2_cols_to_merge = ['P2SIFLFN', 'P2SIFLBM', 'P2SIBD', 'P2SIFLMN', 'P2SIFLSN', 'P2SIEDAD']

    # use unique_id segments to make unique_id and add it to each p2 csv file
    w.add_merged_col_to_csv(path_hiv, 'unique_id', network_hcv_hiv_cols_to_merge)
    w.add_merged_col_to_csv(path_hcv, 'unique_id', network_hcv_hiv_cols_to_merge)
    w.add_merged_col_to_csv(path_interviews1, 'unique_id', interviews1_cols_to_merge)
    w.add_merged_col_to_csv(path_interviews2, 'unique_id', interviews2_cols_to_merge)
    w.add_merged_col_to_csv(path_network, 'unique_id', network_hcv_hiv_cols_to_merge)

    # add project_id to p2_first_interviews.csv using its newly made unique_id to associate the correct project_id
    w.add_column_and_data_from_nodes_to_csv(path_interviews1, path_nodes,
                                            add_col_name='project_id', reference_col_name="unique_id")

    # add rds_id to p2_second_interviews.csv using its newly made unique_id to associate the correct rds_id
    w.add_column_and_data_from_nodes_to_csv(path_interviews2, path_nodes,
                                            add_col_name='rds_id', reference_col_name="unique_id")

#prep_all_p2("C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\")
