import csv
import os


def get_csv_as_list(full_path):
    with open(full_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        csv_list = list(reader)
    return csv_list


def get_first_row_of_csv_as_list(full_path):
    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    first_row = next(reader)
    f.close()
    return first_row


def create_csv_add_column_labels(full_path, cols: list):
    create_empty_csv(full_path)
    append_row_to_csv(full_path, cols)


def append_row_to_csv(full_path, row: list):
    with open(full_path, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        writer.writerow(row)


def create_empty_csv(full_path):
    remove_csv(full_path)
    f = open(full_path, "w", newline="")
    f.close()


def remove_csv(full_path):
    try:
        os.remove(full_path)
    except FileNotFoundError:
        pass


def rename_csv(full_path_old, full_path_new):
    try:
        remove_csv(full_path_new)
        os.rename(full_path_old, full_path_new)
        remove_csv(full_path_old)
    except Exception:
        print("Renaming not possible, check caller")


def fix_column_labels_csv(full_path1, replace_with: dict):
    file_path2 = full_path1[:-4] + "2.csv"
    create_empty_csv(file_path2)

    f1 = open(full_path1, 'r')
    reader1 = csv.reader(f1, delimiter=',')

    new_cols = get_new_col_labels_list(full_path1, replace_with)
    append_row_to_csv(file_path2, new_cols)
    next(reader1)

    for row in reader1:
        append_row_to_csv(file_path2, row)

    f1.close()
    rename_csv(file_path2, full_path1)


def get_new_col_labels_list(full_path, replace_with):
    cols = get_first_row_of_csv_as_list(full_path)
    for old, new in replace_with.items():
        if old in cols:
            i = cols.index(old)
            cols[i] = new
    return cols


def get_index_of_file_col(full_path, col_name):
    cols = get_first_row_of_csv_as_list(full_path)
    return cols.index(col_name)


def get_value_indices_from_file(full_path, values):
    col = get_first_row_of_csv_as_list(full_path)
    indices = []
    for value in values:
        indices.append(col.index(value))
    return indices


def get_str_list_of_merged_cols(full_path, cols_to_merge):
    indices_cols_to_merge = get_value_indices_from_file(full_path, cols_to_merge)
    merged_cols_strings = []

    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    next(reader)

    for row in reader:
        temp_merged_str = ''
        for index in indices_cols_to_merge:
            temp_merged_str += row[index]
        merged_cols_strings.append(temp_merged_str)

    f.close()
    return merged_cols_strings


def add_col_and_data_to_csv(full_path, col_name, values_to_add: list):
    full_path2 = full_path[:-4] + "2.csv"
    create_empty_csv(full_path2)

    cols = get_first_row_of_csv_as_list(full_path)
    cols.append(col_name)
    append_row_to_csv(full_path2, cols)  # populate new csv with old column labels plus the new column label

    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    next(reader)  # already added first row (column labels)

    i = 0
    while i < len(values_to_add):
        for row in reader:
            row.append(values_to_add[i])
            append_row_to_csv(full_path2, row)
            i += 1

    f.close()
    rename_csv(full_path2, full_path)


def add_merged_col_to_csv(full_path, new_col_name, cols_to_merge):
    cols = get_first_row_of_csv_as_list(full_path)
    if new_col_name in cols:
        return 1
    values_to_add = get_str_list_of_merged_cols(full_path, cols_to_merge)
    add_col_and_data_to_csv(full_path, new_col_name, values_to_add)


def get_data_from_one_col_as_list(full_path, col_name):
    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')

    cols = next(reader)
    index = cols.index(col_name)
    data_list = []

    for row in reader:
        data_list.append(row[index])

    f.close()
    return data_list


def get_data_from_multiple_columns_as_list_of_lists(full_path, columns: list):
    cols = get_first_row_of_csv_as_list(full_path)
    indices = []
    for col in columns:
        indices.append(cols.index(col))
    data_list = []

    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        data_row = []
        for index in indices:
            data_row.append(row[index])
        data_list.append(data_row)

    f.close()
    return data_list


def add_column_and_data_from_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name):
    """Input: Path of csv file to add column to; nodes indices of column to add and
    column to use as comparison to associate new column with correct row; data of nodes file.
        Output: Adds column to be added to the specified file and populates it."""
    ref_col_to_add_col_dict = get_no_null_entries_dict_from_csv(full_path_nodes, reference_col_name, add_col_name)

    x = get_csv_as_list(full_path_csv_grow)
    csv_grow_cols = x[0]  # column labels of csv to grow, as list
    if add_col_name in csv_grow_cols:
        return 1
    csv_grow_cols.append(add_col_name)
    csv_grow_data = x[1:]  # data of csv to grow, to as list

    # remove original csv_grow file, make new one with add_col
    create_csv_add_column_labels(full_path_csv_grow, csv_grow_cols)

    csv_grow_reference_col_index = csv_grow_cols.index(reference_col_name)

    for row in csv_grow_data:
        # use reference_col from each row in csv_grow to get add_col from ref_col_to_add_col_dict dictionary
        try:
            add_col = ref_col_to_add_col_dict[row[csv_grow_reference_col_index]]
        except KeyError:
            continue
        row.append(add_col)  # append the retrieved add_col value to the row, under the newly added add_col column label
        append_row_to_csv(full_path_csv_grow, row)


def get_no_null_entries_dict_from_csv(full_path, key_col_name, value_col_name):
    """Input: Nodes csv file path, names of columns to be key and value.
    Output: Returns a dictionary of the specified key, value pairs extracted from the nodes file."""
    full_data = get_csv_as_list(full_path)[1:]
    value_col_index = get_index_of_file_col(full_path, value_col_name)
    key_col_index = get_index_of_file_col(full_path, key_col_name)

    key_value_dict = {}
    for row in full_data:
        key = row[key_col_index]
        value = row[value_col_index]
        if key != '#NULL!' and key != '' and value != '#NULL!' and value != '':
            key_value_dict[key] = value

    return key_value_dict


def get_sender_receiver_to_edge_id_dict(path_edges, edge, sender, receiver):
    edges_data = get_csv_as_list(path_edges)[1:]
    edges_value_col_index = get_index_of_file_col(path_edges, edge)
    edges_key_col_index1 = get_index_of_file_col(path_edges, sender)
    edges_key_col_index2 = get_index_of_file_col(path_edges, receiver)

    sender_receiver_to_edge_id = {}
    for row in edges_data:
        sender_receiver_to_edge_id[row[edges_key_col_index1] + row[edges_key_col_index2]] = row[
            edges_value_col_index]

    return sender_receiver_to_edge_id


def get_unique_single_entry_list(original_data: list):
    data_set_list = list(set(original_data))
    if '' in data_set_list:
        data_set_list.remove('')
    i = 0
    # split up the field note row entries with multiple entries per row
    while i < len(data_set_list):
        entry = data_set_list[i]
        if ',' in entry:
            split_and_append_entry_of_list(data_set_list, entry, ',')
        elif ';' in entry:
            split_and_append_entry_of_list(data_set_list, entry, ';')
        else:
            entry.strip()
            i += 1

    unique_data_list = list(set(data_set_list))
    return unique_data_list


def split_and_append_entry_of_list(set_list, entry, sym):
    """Input: A list of strings, a particular entry from that list,
    the separator symbol used within that entry.
    Output: Splits up the given multi-entry list entry and appends it to the list."""
    entry_split = entry.split(sym)
    set_list.remove(entry)
    for e in entry_split:
        set_list.append(e.strip())


def add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label, type_entry_name):
    """Input: File path to the new notes.csv file; file path to the old edges file;
    old edge file label of note column to be appended to new file; name of the note type for type column in new file.
    Output: Adds a row to column note_name of new file for each unique note name from the given old edge file column."""
    original_col_data = get_data_from_one_col_as_list(path_old_edges, old_col_label)
    unique_data = get_unique_single_entry_list(original_col_data)
    # append a row for each unique field note to the notes.csv file
    # assumes that column 1 is note_name, column 2 is note_type
    for one_entry in unique_data:
        append_row_to_csv(path_notes, [one_entry, type_entry_name])


def get_full_path(path, file_name):
    return path + file_name + '.csv'


def get_note_ids_from_given_row(row: list, note_index, note_name_to_note_id_dict):
    # get all entries for note in the given row
    notes = get_unique_single_entry_list([row[note_index]])
    note_ids = []
    # get note ids from notes.csv
    for note in notes:
        note_ids.append(note_name_to_note_id_dict[note])

    return note_ids


def append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, note_index, note_name_to_note_id,
                                                                   path_note_edges, edge_id):
    # get note ids from notes.csv of current row in old edge file
    note_ids = get_note_ids_from_given_row(row, note_index, note_name_to_note_id)
    # add row to note_edges.csv for each edge_id note_id pair
    for one_id in note_ids:
        append_row_to_csv(path_note_edges, [edge_id, one_id])


def add_auto_increment_col(full_path, col_label):
    num_rows = len(get_csv_as_list(full_path)[1:])
    note_ids = range(1, num_rows + 1)
    add_col_and_data_to_csv(full_path, col_label, list(note_ids))


def get_col_label_to_longest_entry_dict(full_path):
    cols = get_first_row_of_csv_as_list(full_path)
    col_label_to_longest_entry = {}

    for col in cols:
        col_data = get_data_from_one_col_as_list(full_path, col)
        longest = len(max(col_data, key=len))
        col_label_to_longest_entry[col] = longest

    return col_label_to_longest_entry


def get_unique_pids_from_old_edges(old_edge_full_path):
    senders_set_list = list(set(get_data_from_one_col_as_list(old_edge_full_path, 'sender_pid')))
    receivers_set_list = list(set(get_data_from_one_col_as_list(old_edge_full_path, 'receiver_pid')))
    for sender in senders_set_list:
        receivers_set_list.append(sender)
    unique_pids_from_old_edges = list(set(receivers_set_list))
    return unique_pids_from_old_edges


def get_discrepancy_pids_old_edge_and_node(old_edge_full_path, old_node_full_path):
    unique_pids_from_old_edges = get_unique_pids_from_old_edges(old_edge_full_path)
    unique_pids_from_subjects_pids = get_data_from_one_col_as_list(old_node_full_path, 'project_id')
    only_in_old_edges = []
    for edge_pid in unique_pids_from_old_edges:
        if edge_pid not in unique_pids_from_subjects_pids:
            only_in_old_edges.append(edge_pid)
    return only_in_old_edges


def get_and_remove_discrepancy_rows_and_indices_from_old_edges(path, old_edge_file='edge_index_5_2_17',
                                                               old_node_file='node_index_5_3_17'):
    old_edge_full_path = get_full_path(path, old_edge_file)
    old_node_full_path = get_full_path(path, old_node_file)

    only_in_old_edges = get_discrepancy_pids_old_edge_and_node(old_edge_full_path, old_node_full_path)

    x = get_csv_as_list(old_edge_full_path)
    original_edge_data = x[1:]
    edge_col = x[0]

    temp_file = get_full_path(path, old_edge_file + '2')
    create_csv_add_column_labels(temp_file, edge_col)

    discrepancy_rows = []

    for i in range(len(original_edge_data)):
        row = original_edge_data[i]
        for pid in only_in_old_edges:
            if pid in row:
                discrepancy_rows.append([original_edge_data.index(row) + 2] + row)
                to_add = 0
                break
            else:
                to_add = 1
        if to_add == 1:
            append_row_to_csv(temp_file, row)

    rename_csv(temp_file, old_edge_full_path)

    print(only_in_old_edges)
    for row in discrepancy_rows:
        print(row)

    return discrepancy_rows

all_csvs_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"

#get_and_remove_discrepancy_rows_and_indices_from_old_edges(all_csvs_path)
