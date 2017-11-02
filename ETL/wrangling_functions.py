"""Functions to do various data wrangling operations with/on csv files."""
import csv
import os
import constants as c


def get_csv_as_list(full_path):
    """Input: File path of the csv to return.
    Output: Returns list containing each row of the csv file as another list."""
    with open(full_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        csv_list = list(reader)
    return csv_list


def get_first_row_of_csv_as_list(full_path):
    """Input: File path of the csv whose first row to return.
    Output: Returns list containing the first row of the csv file."""
    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    first_row = next(reader)
    f.close()
    return first_row


def create_csv_add_column_labels(full_path, col_labels: list):
    """Input: File path of the csv to create; column labels to add to this file.
    Output: Creates a csv with the given column labels as the first row."""
    create_empty_csv(full_path)
    append_row_to_csv(full_path, col_labels)


def append_row_to_csv(full_path, row: list):
    """Input: File path of the csv; the row to append to that csv.
    Output: Appends the given row to the end of the given file."""
    with open(full_path, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        writer.writerow(row)


def create_empty_csv(full_path):
    """Input: File path of the csv to create.
    Output: Creates an empty file at the given location."""
    remove_csv(full_path)
    f = open(full_path, "w", newline="")
    f.close()


def remove_csv(full_path):
    """Input: File path of the csv to delete.
    Output: Deletes the given file if it exists at that location."""
    try:
        os.remove(full_path)
    except FileNotFoundError:
        pass


def rename_csv(full_path_old, full_path_new):
    """Input: File path of the current csv; what the new file path should be.
    Output: Renames the given file to the given new name."""
    try:
        remove_csv(full_path_new)
        os.rename(full_path_old, full_path_new)
        remove_csv(full_path_old)
    except Exception:
        print("Renaming not possible, check caller")


def fix_column_labels_csv(full_path, replace_with: dict):
    """Input: File path of the csv whose column labels to update;
    dictionary of current column labels and what to replace them with.
    Output: Replaces the given old column labels with the given new labels."""
    file_path_temp = full_path[:-4] + "2.csv"
    create_empty_csv(file_path_temp)

    f1 = open(full_path, 'r')
    reader = csv.reader(f1, delimiter=',')

    new_cols = get_new_col_labels_list(full_path, replace_with)  # get updated column labels row
    append_row_to_csv(file_path_temp, new_cols)  # append it to the new file, as first row
    next(reader)  # move reader to the first row containing data of the original csv

    for row in reader:
        append_row_to_csv(file_path_temp, row)  # append every row of data to the new csv

    f1.close()
    rename_csv(file_path_temp, full_path)  # rename the new csv to the old name, thus "updating" the column labels


def get_new_col_labels_list(full_path, replace_with: dict):
    """Input: File path of the csv whose column labels to update;
    dictionary of current column labels and what to replace them with.
    Output: Returns updated column labels row as list."""
    cols = get_first_row_of_csv_as_list(full_path)  # get current column labels row
    for old, new in replace_with.items():  # for every pair of old and new column labels,
        if old in cols:
            i = cols.index(old)  # get the list/row location of the old column label,
            cols[i] = new  # replace the old column label with the new label
    return cols


def get_index_of_file_col(full_path, col_name):
    """Input: File path of the csv whose column index to fetch; name of the column whose index to fetch.
    Output: Returns the index of the given column in the given file."""
    cols = get_first_row_of_csv_as_list(full_path)
    return cols.index(col_name)


def get_indices_of_file_col(full_path, col_names: list):
    """Input: File path of the csv whose column indices to fetch; name of the columns whose indices to fetch.
    Output: Returns the indices of the given columns in the given file, as a list."""
    indices = []
    for col_name in col_names:
        indices.append(get_index_of_file_col(full_path, col_name))
    return indices


def get_str_list_of_merged_cols(full_path, cols_to_merge: list):
    """Input: File path of the csv whose given columns to merge to a new one; list of labels of the columns to merge.
    Output: Returns the new, merged column as a string."""
    indices_cols_to_merge = get_indices_of_file_col(full_path, cols_to_merge)
    merged_cols_strings = []

    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    next(reader)  # skip first row (column labels)

    for row in reader:
        temp_merged_str = ''
        for index in indices_cols_to_merge:
            temp_merged_str += row[index]  # add the value from each column in the current row to a string
        merged_cols_strings.append(temp_merged_str)  # add this new string to the list of merged columns
    f.close()
    return merged_cols_strings


def add_col_and_data_to_csv(full_path, col_name, values_to_add: list):
    """Input: File path of the csv to add a column and its data to; name of the column to add; data to add to that column.
    Output: Adds the given column (label and data) to the given csv file."""
    cols = get_first_row_of_csv_as_list(full_path)
    if col_name in cols:  # check that this new column doesn't already exist
        return 1

    path_temp = c.TEMP_FILE_PATH
    create_empty_csv(path_temp)

    cols.append(col_name)
    append_row_to_csv(path_temp, cols)  # populate new csv with old column labels plus the new column label

    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    next(reader)  # already added first row (column labels)
    i = 0
    while i < len(values_to_add):  # need while so that we can increase i with each new row read
        for row in reader:
            row.append(values_to_add[i])  # add the appropriate value to this current row, as a value of the new column
            append_row_to_csv(path_temp, row)  # add this extended row to the temp csv file
            i += 1
    f.close()
    rename_csv(path_temp, full_path)  # rename the temp csv to the original name, thus "adding" the new column


def add_merged_col_to_csv(full_path, new_col_name, cols_to_merge):
    """Input: File path of the csv to add a column and its data to; name of the column to add; data to add to that column.
    Output: Adds the given column (label and data) to the given csv file."""
    cols = get_first_row_of_csv_as_list(full_path)
    if new_col_name in cols:
        return 1
    values_to_add = get_str_list_of_merged_cols(full_path, cols_to_merge)
    add_col_and_data_to_csv(full_path, new_col_name, values_to_add)


def get_data_from_one_col_as_list(full_path, col_name):
    """Input: File path of the csv from which to get column data; name of the column from which to get data.
    Output: Returns the data from the given table and column as a list."""
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
    """Input: File path of the csv from which to get column data; names of the columns from which to get data.
    Output: Returns the data from the given table and columns as a list of lists."""
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


def add_column_and_data_from_old_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name):
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
    """Input: CSV file path, names of columns to be key and value.
    Output: Returns a dictionary of the specified key, value pairs extracted from the given file."""
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
    """No usage."""
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
    """Input: List of strings of the original data of which to get true set.
        Output: Returns a list of the input data without duplicates or multiple entries per element/string."""
    data_set_list = list(set(original_data))
    for no_note in c.NO_ENTRIES:  # remove the elements that indicate no note entry exists (empty string, 'NA')
        try:
            data_set_list.remove(no_note)
        except ValueError:
            pass
    i = 0
    # split up multiple entries per field
    while i < len(data_set_list):  # this ensures that any entries that have not been fully split are examined again
        entry = data_set_list[i]
        if ',' in entry:
            split_and_append_entry_of_list(data_set_list, entry, ',')
        elif ';' in entry:  # elifs so that each loop we only split on one kind of separator; splits are iterated over
            split_and_append_entry_of_list(data_set_list, entry, ';')
        elif ':' in entry:
            split_and_append_entry_of_list(data_set_list, entry, ':')
        else:
            entry.strip()
            i += 1

    unique_data_list = list(set(data_set_list))
    return unique_data_list


def split_and_append_entry_of_list(set_list, entry, sym):
    """Input: A list of strings; a particular entry from that list; the separator symbol used within that entry.
    Output: Splits up the given multi-entry list entry and appends it to the list."""
    entry_split = entry.split(sym)
    set_list.remove(entry)
    for e in entry_split:
        set_list.append(e.strip())


def add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label, type_of_entry):
    """Input: File path to the new notes.csv file; file path to the old edges file;
    old edge file label of note column to be appended to new file; name of the note type for type column in new file.
    Output: Adds a row to column note_name of new file for each unique note name from the given old edge file column."""
    original_col_data = get_data_from_one_col_as_list(path_old_edges, old_col_label)
    unique_data = get_unique_single_entry_list(original_col_data)
    # append a row for each unique field note to the notes.csv file
    # assumes that column 1 is note_name, column 2 is note_type
    for one_entry in unique_data:
        append_row_to_csv(path_notes, [one_entry, type_of_entry])


def get_full_csv_path(file_name):
    """Input: Name of csv file of which to get full file path.
    Output: Returns the full file path of the given csv file."""
    return c.ALL_CSVS_PATH + file_name + '.csv'


def get_note_ids_from_given_row(row: list, note_index, note_name_to_note_id_dict):
    """Input: Row as a list; index of the note column; dictionary from note name to note ID.
    Output: Returns list of unique note IDs from the given row's note column field."""
    # get all entries for note in the given row
    notes = get_unique_single_entry_list([row[note_index]])
    note_ids = []
    # get note ids from notes.csv
    for note in notes:
        note_ids.append(note_name_to_note_id_dict[note])

    return note_ids


def append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row: list, note_index, note_name_to_note_id,
                                                                   path_note_edges, edge_id):
    """Input: Row as a list; index of the note column; dictionary from note name to note ID;
    file path of note_edges.csv; this row's edge ID of sender-receiver pair as string.
    Output: Appends row(s) to the note_edges.csv file for each edge ID - note ID pair found in the given row."""
    # get note ids from notes.csv of current row in old edge file
    note_ids = get_note_ids_from_given_row(row, note_index, note_name_to_note_id)
    # add row to note_edges.csv for each edge_id note_id pair
    for one_id in note_ids:
        append_row_to_csv(path_note_edges, [edge_id, one_id])


def add_auto_increment_col(full_path, col_label):
    """Input: File path of csv to which to add an autoincrement column; name of that new column.
    Output: Adds an autoincrement column to the given csv file."""
    num_rows = len(get_csv_as_list(full_path)[1:])
    column_ids = range(1, num_rows + 1)
    add_col_and_data_to_csv(full_path, col_label, list(column_ids))


def get_col_label_to_longest_entry_dict(full_path):
    """Input: File path of csv of which to get each column's longest entry length.
    Output: Returns dictionary of column label to that column's longest row entry length."""
    cols = get_first_row_of_csv_as_list(full_path)
    col_label_to_longest_entry = {}

    for col in cols:
        col_data = get_data_from_one_col_as_list(full_path, col)
        longest = len(max(col_data, key=len))
        col_label_to_longest_entry[col] = longest

    return col_label_to_longest_entry


def get_unique_pids_from_old_edges(old_edge_full_path):
    """Input: File path of old edge csv file.
    Output: Returns all unique project IDs from the old edge file, from the sender and receiver columns."""
    senders_set_list = list(set(get_data_from_one_col_as_list(old_edge_full_path, c.LABEL_SENDER_PID)))
    receivers_set_list = list(set(get_data_from_one_col_as_list(old_edge_full_path, c.LABEL_RECEIVER_PID)))
    for sender in senders_set_list:
        receivers_set_list.append(sender)
    unique_pids_from_old_edges = list(set(receivers_set_list))
    return unique_pids_from_old_edges


def get_distinct_column_entries_from_csv(full_path, col_label):
    """Input: File path of csv from which to get a column's distinct entries; column label.
    Output: Returns list of the given file column's distinct entries."""
    return list(set(get_data_from_one_col_as_list(full_path, col_label)))


def get_distinct_ids_from_multiple_csvs(list_of_full_paths: list, id_col_label: str):
    """No usage.
    Input: List of file paths of csvs from which to get all ID columns' distinct entries; ID column label.
    Output: Returns list of the given file's columns' distinct entries."""
    disctinct_ids = []
    for full_path in list_of_full_paths:
        temp_distinct_ids = get_distinct_column_entries_from_csv(full_path, id_col_label)
        disctinct_ids.extend(temp_distinct_ids)
        disctinct_ids = list(set(disctinct_ids))
    return disctinct_ids


def get_discrepancy_pids_only_in_old_edge_not_node(old_edge_full_path, old_node_full_path):
    """Input: File paths of old edge csv and old node csv.
    Output: Returns list of project IDs that occur only in old edge csv file and not in old node csv file."""
    unique_pids_from_old_edges = get_unique_pids_from_old_edges(old_edge_full_path)
    unique_pids_from_old_nodes = get_data_from_one_col_as_list(old_node_full_path, c.OLD_LABEL_PID)
    only_in_old_edges = []
    for edge_pid in unique_pids_from_old_edges:
        if edge_pid not in unique_pids_from_old_nodes:
            only_in_old_edges.append(edge_pid)
    return only_in_old_edges


def get_discrepancy_pids_only_in_old_node_not_edge(old_edge_full_path, old_node_full_path):
    """Input: File paths of old edge csv and old node csv.
    Output: Returns list of project IDs that occur only in old edge csv file and not in old node csv file."""
    unique_pids_from_old_edges = get_unique_pids_from_old_edges(old_edge_full_path)
    unique_pids_from_old_nodes = get_data_from_one_col_as_list(old_node_full_path, c.OLD_LABEL_PID)
    only_in_old_nodes = []
    for node_pid in unique_pids_from_old_nodes:
        if node_pid not in unique_pids_from_old_edges:
            only_in_old_nodes.append(node_pid)
    return only_in_old_nodes


def get_and_remove_discrepancy_rows_and_indices_from_old_edges():
    """Input: None.
    Output: Returns list of rows as lists that contained at least one pid that occurred in
    the old edge file, but not the node file; remove those discrepancy rows from the old edge file."""
    old_edge_full_path = get_full_csv_path(c.OLD_EDGES_FILE)
    old_node_full_path = get_full_csv_path(c.OLD_NODES_FILE)

    only_in_old_edges = get_discrepancy_pids_only_in_old_edge_not_node(old_edge_full_path, old_node_full_path)
    # not too relevant: there can be nodes that do not appear in the edges file
    only_in_old_nodes = get_discrepancy_pids_only_in_old_node_not_edge(old_edge_full_path, old_node_full_path)

    x = get_csv_as_list(old_edge_full_path)
    original_edge_data = x[1:]
    original_edge_col = x[0]

    temp_file_path = get_full_csv_path(c.OLD_EDGES_FILE + '2')
    create_csv_add_column_labels(temp_file_path, original_edge_col)

    discrepancy_rows = []

    for i in range(len(original_edge_data)):
        row = original_edge_data[i]  # for every row from the original data
        to_add = 1
        for pid in only_in_old_edges:
            if pid in row:  # if the pid that occurs only in the old edge file (but not the node file) is in this row
                #discrepancy_rows.append([original_edge_data.index(row) + 2] + row)
                # append to discrepancy_rows this row and its real index (not counting column label row, starting at 1)
                discrepancy_rows.append([i + 2] + row)
                to_add = 0
                break  # stop trying to find discrepancy pids in this row if we already found one
        if to_add == 1:  # if we did not find any discrepancy pids in this row, append it to the temp file as "clean".
            append_row_to_csv(temp_file_path, row)

    rename_csv(temp_file_path, old_edge_full_path)  # replace old edge file with temp file (discrepancy rows removed)

    return discrepancy_rows


def get_col_label_to_col_index_dict(columns: list):
    """Input: List of csv column labels.
    Output: Returns dictionary of column label to index of that column."""
    column_positions = {}
    for i in range(len(columns)):
        col = columns[i]
        column_positions[col] = i
    return column_positions


def get_ids_not_in_sub_ids(phase: str, comparison_file: str, id_name: str):
    """Input: Phase or file name for string writing purposes;
    name of file to check against subjects_ids.csv file; name of ID to check.
    Output: Returns list of all pids that occur in given file but not in subjects_ids.csv and
    pids that occur in subjects_ids.csv but not in given file."""
    path_comp = get_full_csv_path(comparison_file)
    path_sub_ids = get_full_csv_path(c.SUBJECTS_IDS_FILE)

    phase_ids = get_distinct_column_entries_from_csv(path_comp, id_name)
    sub_ids_ids = get_distinct_column_entries_from_csv(path_sub_ids, id_name)

    in_phase_only_not_in_sub_ids = [id_name + " in " + phase + " files but not in subjects_ids file"]
    in_sub_ids_only_not_in_phase = [id_name + " in subjects_ids file but not in " + phase]

    for one_id in phase_ids:
        if one_id not in sub_ids_ids:
            in_phase_only_not_in_sub_ids.append(one_id)

    for one_id in sub_ids_ids:
        if one_id not in phase_ids:
            in_sub_ids_only_not_in_phase.append(one_id)

    return [in_phase_only_not_in_sub_ids] + [in_sub_ids_only_not_in_phase]


def get_union_of_lists(list1, list2):
    """Input: Two lists of which to get the union (all unique members of both).
    Output: Returns one list of all unique member from both input lists."""
    return list(set(list1) | set(list2))


def get_intersection_of_lists(list1, list2):
    """Input: Two lists of which to get the intersection (only those list members that occur in both lists).
    Output: Returns one list of all unique members that occur in both input lists."""
    return list(set(list1) & set(list2))


def get_difference_list1_only(list1, list2):
    """Input: Two lists of which to get the difference (all unique members that occur only in list1).
    Output: Returns one list of all unique members that occur only in input list1."""
    return list(set(list1) - set(list2))


#print(get_and_remove_discrepancy_rows_and_indices_from_old_edges())

#print(get_ids_not_in_sub_ids("P1", 'p1_screenings', 'rds_id'))

#print(get_ids_not_in_sub_ids("P2", 'p2_network_interviews', 'unique_id'))
#print(get_ids_not_in_sub_ids("P2_second_interviews", 'p2_second_interviews', 'rds_id'))
# no new rds ids here, where do the two additional ones come from in subjects_ids???

# would like to add pid foreign key from subjects_ids to p2_network_interviews
# and rds id foreign key from subjects_ids to p1_screenings
