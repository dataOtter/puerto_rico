def add_col_and_data_to_csv(full_path, col_name, values_to_add):
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