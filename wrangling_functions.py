import csv
import os
# get_csv_as_list(file_path)
# get_first_row_of_csv_as_list(file_path)
# get_new_col_labels_list(full_path, replace_with)
# get_value_index_from_nodes_col(path_nodes, value)
# get_value_indices_from_file(full_path, values)
# get_str_list_of_merged_cols(full_path, cols_to_merge)

# create_csv_add_column_labels(full_path, cols)
# create_empty_csv(full_path)

# append_row_to_csv(full_path, row)
# add_col_and_data_to_csv(full_path, col_name, values_to_add)
# add_merged_col_to_csv(full_path, new_col_name, cols_to_merge)
# remove_csv(full_path)
# rename_csv(full_path_old, full_path_new)
# fix_column_labels_csv(full_path1, replace_with)


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


def create_csv_add_column_labels(full_path, cols):
    create_empty_csv(full_path)
    append_row_to_csv(full_path, cols)


def append_row_to_csv(full_path, row):
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
        os.rename(full_path_old, full_path_new)
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
    remove_csv(full_path1)
    rename_csv(file_path2, full_path1)


def get_new_col_labels_list(full_path, replace_with):
    cols = get_first_row_of_csv_as_list(full_path)
    for old, new in replace_with.items():
        if old in cols:
            i = cols.index(old)
            cols[i] = new
    return cols


def get_value_index_from_nodes_col(path_nodes, value):
    col = get_first_row_of_csv_as_list(path_nodes)
    return col.index(value)


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
    remove_csv(full_path)
    rename_csv(full_path2, full_path)


def add_merged_col_to_csv(full_path, new_col_name, cols_to_merge):
    cols = get_first_row_of_csv_as_list(full_path)
    if new_col_name in cols:
        return 1
    values_to_add = get_str_list_of_merged_cols(full_path, cols_to_merge)
    add_col_and_data_to_csv(full_path, new_col_name, values_to_add)


def get_data_from_one_col_as_list(full_path, col_name):
    cols = get_first_row_of_csv_as_list(full_path)
    index = cols.index(col_name)
    data_list = []

    f = open(full_path, 'r')
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        data_list.append(row[index])

    f.close()
    return data_list


def add_column_and_data_from_nodes_to_csv(full_path_csv_grow, full_path_nodes, add_col_name, reference_col_name):
    """Input: Path of csv file to add column to; nodes indices of column to add and
    column to use as comparison to associate new column with correct row; data of nodes file.
        Output: Adds column to be added to the specified file and populates it."""
    nodes_data = get_csv_as_list(full_path_nodes)[1:]  # data of nodes csv as list
    nodes_add_col_index = get_value_index_from_nodes_col(full_path_nodes, add_col_name)
    nodes_reference_col_index = get_value_index_from_nodes_col(full_path_nodes, reference_col_name)

    x = get_csv_as_list(full_path_csv_grow)
    csv_grow_cols = x[0]  # column labels of csv to grow, as list
    if add_col_name in csv_grow_cols:
        return 1
    csv_grow_cols.append(add_col_name)
    csv_grow_data = x[1:]  # data of csv to grow, to as list

    # remove original csv_grow file, make new one with add_col
    create_csv_add_column_labels(full_path_csv_grow, csv_grow_cols)

    reference_col_to_add_col = {}
    for row in nodes_data:
        if row[nodes_reference_col_index] != '#NULL!' and row[nodes_reference_col_index] != '':
            # make reference_col to add_col dict
            reference_col_to_add_col[row[nodes_reference_col_index]] = row[nodes_add_col_index]

    csv_grow_reference_col_index = csv_grow_cols.index(reference_col_name)

    for row in csv_grow_data:
        # use reference_col from each row in csv_grow to get add_col from reference_col_to_add_col dictionary
        try:
            add_col = reference_col_to_add_col[row[csv_grow_reference_col_index]]
        except KeyError:
            continue
        row.append(add_col)  # append the retrieved add_col value to the row, under the newly added add_col column label
        append_row_to_csv(full_path_csv_grow, row)

fp = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\test.csv"
fp2 = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\test2.csv"
fp3 = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\p2_hivs.csv"
#col = ['c', 'd']
#replace_with = {'d': 'e'}
#create_csv_add_column_labels(fp, col)
#create_empty_csv(fp)
#for i in range(1, 10):
    #add_row_to_csv(fp, [str(i)])
#fix_column_labels_csv(fp, replace_with)
#cols_to_merge = ['P2FLFN', 'P2FLBM', 'P2BD', 'P2FLMN', 'P2FLSN', 'P2EDAD']
#add_merged_col_to_csv(fp3, 'unique_id', cols_to_merge)
#print(get_data_from_one_col_as_list(fp3, 'unique_id'))
