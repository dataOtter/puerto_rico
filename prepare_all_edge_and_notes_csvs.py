import wrangling_functions as w


def create_all_edge_csvs(path, edges_file='edges', old_edge_file='edge_index_5_2_17', net_edges_file='network_edges',
                         rds_edges_file='rds_edges', notes_file='notes', note_edges_file='note_edges'):
    """Input: General file path; csv file names of all edge and note files.
    Output: Creates and populates all edge and note files."""
    path_edges = w.get_full_path(path, edges_file)
    path_old_edges = w.get_full_path(path, old_edge_file)
    path_net_edges = w.get_full_path(path, net_edges_file)
    path_rds_edges = w.get_full_path(path, rds_edges_file)
    path_notes = w.get_full_path(path, notes_file)
    path_note_edges = w.get_full_path(path, note_edges_file)

    label_sender, label_receiver, label_edge = 'sender_pid', 'receiver_pid', 'edge_id'
    label_old_net, label_old_rds = 'Net Supplement', 'RDS Edge'
    label_old_cnx, label_old_fn = 'Connection Notes', 'Field Notes'

    replace_with = {'Sender ID': label_sender, 'Receiver ID': label_receiver}
    w.fix_column_labels_csv(path_old_edges, replace_with)

    x = w.get_csv_as_list(path_old_edges)
    old_edge_cols, old_edge_data = x[0], x[1:]

    sender_old_index, receiver_old_index = old_edge_cols.index(label_sender), old_edge_cols.index(label_receiver)

    create_edges_csv(path_edges, old_edge_data, sender_old_index, receiver_old_index)
    sender_receiver_to_edge_id = w.get_sender_receiver_to_edge_id_dict(path_edges, label_edge,
                                                                       label_sender, label_receiver)

    net_index = old_edge_cols.index(label_old_net)
    create_network_edges_csv(path_net_edges, old_edge_data, sender_receiver_to_edge_id,
                             sender_old_index, receiver_old_index, net_index)

    rds_index = old_edge_cols.index(label_old_rds)
    create_rds_edges_csv(path_rds_edges, old_edge_data, sender_receiver_to_edge_id,
                         sender_old_index, receiver_old_index, rds_index)

    create_notes_csv(path_notes, path_old_edges, label_old_cnx, label_old_fn)

    note_name_to_note_id = w.get_no_null_entries_dict_from_csv(path_notes, 'note_name', 'note_id')
    cnx_note_index, fn_index = old_edge_cols.index(label_old_cnx), old_edge_cols.index(label_old_fn)
    create_note_edges_csv(path_note_edges, old_edge_data, sender_old_index, receiver_old_index,
                          cnx_note_index, fn_index, sender_receiver_to_edge_id, note_name_to_note_id)


def create_edges_csv(path_edges, old_edge_data, sender_index, receiver_index,
                     label_sender='sender_pid', label_receiver='receiver_pid', label_edge='edge_id'):
    """Input: edges.csv file path; data from the old edge file;
    sender and receiver index in that file; sender, receiver, edge column labels.
    Output: Creates edges.csv file and populates it with all edge connections (edge id, sender pid, receiver pid)."""
    w.create_csv_add_column_labels(path_edges, [label_edge, label_sender, label_receiver])
    for i in range(1, len(old_edge_data) + 1):
        row = old_edge_data[i - 1]
        w.append_row_to_csv(path_edges, [i, row[sender_index], row[receiver_index]])


def create_network_edges_csv(path_net_edges, old_edge_data, sender_receiver_to_edge_id,
                             sender_index, receiver_index, net_index, label_edge='edge_id'):
    """Input: net_edges.csv file path; data from the old edge file;
    sender, receiver, and network supplement index in that file; edge column label.
    Output: Creates the net_edges.csv file and populates it with all network supplement edge connections."""
    w.create_csv_add_column_labels(path_net_edges, [label_edge])
    for row in old_edge_data:
        if row[net_index] == 'Yes':
            sender_receiver = row[sender_index] + row[receiver_index]
            edge_id = sender_receiver_to_edge_id[sender_receiver]
            w.append_row_to_csv(path_net_edges, [edge_id])


def create_rds_edges_csv(path_rds_edges, old_edge_data, sender_receiver_to_edge_id,
                         sender_index, receiver_index, rds_index, label_edge='edge_id'):
    """Input: rds_edges.csv file path; data from the old edge file;
    sender, receiver, and rds edge index in that file; edge column label.
    Output: Creates the rds_edges.csv file and populates it with all rds edge connections."""
    w.create_csv_add_column_labels(path_rds_edges, [label_edge])
    for row in old_edge_data:
        if row[rds_index] == 'Yes':
            sender_receiver = row[sender_index] + row[receiver_index]
            edge_id = sender_receiver_to_edge_id[sender_receiver]
            w.append_row_to_csv(path_rds_edges, [edge_id])


def create_notes_csv(path_notes, path_old_edges, cnx, fn, label_note_id='note_id', label_note_name='note_name',
                     label_note_type='type', cnx_type='Connection note', fn_type='Field note'):
    """Input: notes.csv file path; connection and field notes column labels in old edges file;
    note name and type column labels; note type entries for connection and field notes.
    Output: Creates notes.csv file and populates it with all unique connection and field note names, and note_ids."""
    w.create_csv_add_column_labels(path_notes, [label_note_name, label_note_type])
    # add all unique connection note names
    w.add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label=cnx, type_entry_name=cnx_type)
    # add all unique field note names
    w.add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label=fn, type_entry_name=fn_type)
    # add note_id column as autoincrement
    w.add_auto_increment_col(path_notes, label_note_id)


def create_note_edges_csv(path_note_edges, old_edge_data, sender_index, receiver_index, cnx_note_index, fn_index,
                          sender_receiver_to_edge_id, note_name_to_note_id,
                          label_edge='edge_id', label_note='note_id', label_note_edge='note_edge_id'):
    """Input: note_edges.csv file path; old edge data as list;
    sender, receiver, connection, field notes indices in old edges file;
    sender+receiver to edge_id dictionary, note name to note id dictionary; edge, note, note_edge column labels.
    Output: Creates note_edges.csv file and populates it with all pairs of edge id and note id, and note_edge_ids."""
    w.create_csv_add_column_labels(path_note_edges, [label_edge, label_note])

    for row in old_edge_data:
        # get edge_id from edges.csv (using dict to look up sender+receiver_id) of current row in old edge file
        edge_id = sender_receiver_to_edge_id[row[sender_index] + row[receiver_index]]
        # append each edge_id and cnx_note_id pair to note_edges.csv
        w.append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, cnx_note_index, note_name_to_note_id,
                                                                         path_note_edges, edge_id)
        # append each edge_id and fn_id pair to note_edges.csv
        w.append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, fn_index, note_name_to_note_id,
                                                                         path_note_edges, edge_id)

    w.add_auto_increment_col(path_note_edges, label_note_edge)

#create_all_edge_csvs("C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\")
