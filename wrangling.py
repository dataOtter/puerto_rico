import wrangling_functions as wrangle


def get_csv_as_list(full_path):
    wrangle.get_csv_as_list(full_path)


def get_first_row_of_csv_as_list(full_path):
    wrangle.get_first_row_of_csv_as_list(full_path)


def create_csv_add_column_labels(full_path, cols):
    wrangle.create_csv_add_column_labels(full_path, cols)


def append_row_to_csv(full_path, row):
    wrangle.append_row_to_csv(full_path, row)


def create_empty_csv(full_path):
    wrangle.create_empty_csv(full_path)


def remove_csv(full_path):
    wrangle.remove_csv(full_path)


def rename_csv(full_path_old, full_path_new):
    wrangle.rename_csv(full_path_old, full_path_new)


def fix_column_labels_csv(full_path1, replace_with):
    wrangle.fix_column_labels_csv(full_path1, replace_with)


def get_new_col_labels_list(full_path, replace_with):
    wrangle.get_new_col_labels_list(full_path, replace_with)


def get_value_index_from_nodes_col(path_nodes, value):
    wrangle.get_value_index_from_nodes_col(path_nodes, value)


def get_value_indices_from_file(full_path, values):
    wrangle.get_value_indices_from_file(full_path, values)


def get_str_list_of_merged_cols(full_path, cols_to_merge):
    wrangle.get_str_list_of_merged_cols(full_path, cols_to_merge)


def add_col_and_data_to_csv(full_path, col_name, values_to_add):
    wrangle.add_col_and_data_to_csv(full_path, col_name, values_to_add)


def add_merged_col_to_csv(full_path, new_col_name, cols_to_merge):
    wrangle.add_merged_col_to_csv(full_path, new_col_name, cols_to_merge)


def get_data_from_one_col_as_list(full_path, col_name):
    wrangle.get_data_from_one_col_as_list(full_path, col_name)


def add_column_and_data_from_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name):
    wrangle.add_column_and_data_from_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name)
