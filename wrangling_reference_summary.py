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


def get_index_of_file_col(path_nodes, value):
    wrangle.get_index_of_file_col(path_nodes, value)


def get_value_indices_from_file(full_path, values):
    wrangle.get_indices_of_file_col(full_path, values)


def get_str_list_of_merged_cols(full_path, cols_to_merge):
    wrangle.get_str_list_of_merged_cols(full_path, cols_to_merge)


def add_col_and_data_to_csv(full_path, col_name, values_to_add):
    wrangle.add_col_and_data_to_csv(full_path, col_name, values_to_add)


def add_merged_col_to_csv(full_path, new_col_name, cols_to_merge):
    wrangle.add_merged_col_to_csv(full_path, new_col_name, cols_to_merge)


def get_data_from_one_col_as_list(full_path, col_name):
    wrangle.get_data_from_one_col_as_list(full_path, col_name)


def get_data_from_multiple_columns_as_list_of_lists(full_path, columns: list):
    wrangle.get_data_from_multiple_columns_as_list_of_lists(full_path, columns)


def add_column_and_data_from_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name):
    wrangle.add_column_and_data_from_old_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name)


def get_nodes_dict(full_path_nodes, key_col_name, value_col_name):
    wrangle.get_no_null_entries_dict_from_csv(full_path_nodes, key_col_name, value_col_name)


def get_sender_receiver_to_edge_id_dict(path_edges, edge, sender, receiver):
    wrangle.get_sender_receiver_to_edge_id_dict(path_edges, edge, sender, receiver)


def get_unique_single_entry_list(original_data):
    wrangle.get_unique_single_entry_list(original_data)


def split_and_append_entry_of_list(set_list, entry, sym):
    wrangle.split_and_append_entry_of_list(set_list, entry, sym)


def add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label, type_entry_name):
    wrangle.add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label, type_entry_name)


def get_full_path(path, file_name):
    wrangle.get_full_path(path, file_name)


def get_note_ids_from_row(row: list, note_index, note_name_to_note_id_dict):
    wrangle.get_note_ids_from_given_row(row, note_index, note_name_to_note_id_dict)


def add_auto_increment_col(full_path, col_label):
    wrangle.add_auto_increment_col(full_path, col_label)


def append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, note_index, note_name_to_note_id,
                                                                   path_note_edges, edge_id):
    wrangle.append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, note_index, note_name_to_note_id,
                                                                   path_note_edges, edge_id)


def get_unique_pids_from_old_edges(old_edge_full_path):
    wrangle.get_unique_pids_from_old_edges(old_edge_full_path)


def get_discrepancy_pids_old_edge_and_node(old_edge_full_path, old_node_full_path):
    wrangle.get_discrepancy_pids_only_in_old_edge_not_node(old_edge_full_path, old_node_full_path)


def get_and_remove_discrepancy_rows_and_indices_from_old_edges(old_edge_full_path, old_node_full_path):
    wrangle.get_and_remove_discrepancy_rows_and_indices_from_old_edges(old_edge_full_path, old_node_full_path)


def get_col_label_to_col_index_in_csv_dict(csv_columns: list):
    wrangle.get_col_label_to_col_index_in_csv_dict(csv_columns)


def get_distinct_ids_from_csv(full_path, id_col_label):
    wrangle.get_distinct_ids_from_csv(full_path, id_col_label)


def get_distinct_ids_from_multiple_csvs(list_of_full_paths: list, id_col_label: str):
    wrangle.get_distinct_ids_from_multiple_csvs(list_of_full_paths, id_col_label)


def get_ids_not_in_sub_ids(path, phase: str, comparison_file: str, id_name: str, sub_ids_file='subjects_ids'):
    wrangle.get_ids_not_in_sub_ids(path, phase, comparison_file, id_name)




