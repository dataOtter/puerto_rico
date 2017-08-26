import wrangling_functions as w


def prep_all_p2(path, network_file='p2_network_interviews', hiv_file='p2_hivs', hcv_file='p2_hcvs',
                interviews1_file='p2_first_interviews', interviews2_file='p2_second_interviews',
                nodes_file="node_index_5_3_17"):
    # get all p2 csv file paths
    path_network = path + network_file + ".csv"
    path_hiv = path + hiv_file + '.csv'
    path_hcv = path + hcv_file + '.csv'
    path_interviews1 = path + interviews1_file + '.csv'
    path_interviews2 = path + interviews2_file + '.csv'
    path_nodes = path + nodes_file + '.csv'

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

    # add project_id to p2_first_interview.csv using its newly made unique_id to associate the correct project_id
    w.add_column_and_data_from_nodes_to_csv(path_interviews1, path_nodes,
                                            add_col_name='project_id', reference_col_name="unique_id")


prep_all_p2("C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\")

    # p2_second_interviews make rds_id column
    # p2_first_interviews make project_id column
