import wrangling_functions as w
import constants as c


def create_all_edge_and_note_csvs():
    """Output: Creates and populates all edge and note files."""
    path_edges = c.EDGES_PATH
    path_old_edges = c.OLD_EDGES_PATH
    path_net_edges = c.NETWORK_EDGES_PATH
    path_rds_edges = c.RDS_EDGES_PATH
    path_notes = c.NOTES_PATH
    path_note_edges = c.NOTE_EDGES_PATH

    label_old_net, label_old_rds = 'Net Supplement', 'RDS Edge'
    label_old_cnx, label_old_fn = 'Connection Notes', 'Field Notes'

    replace_with = {c.OLD_LABEL_SENDER_ID: c.LABEL_SENDER_PID, c.OLD_LABEL_RECEIVER_ID: c.LABEL_RECEIVER_PID}
    w.fix_column_labels_csv(path_old_edges, replace_with)

    x = w.get_csv_as_list(path_old_edges)
    old_edge_cols, old_edge_data = x[0], x[1:]

    sender_old_index, receiver_old_index = old_edge_cols.index(c.LABEL_SENDER_PID), old_edge_cols.index(c.LABEL_RECEIVER_PID)

    # make and populate the edges.csv file
    create_edges_csv(path_edges, old_edge_data, sender_old_index, receiver_old_index)

    # get a dictionary from sender_receiver to edge_id
    sender_receiver_to_edge_id = w.get_no_null_entries_dict_from_csv(path_edges, c.LABEL_SENDER_RECEIVER, c.LABEL_EDGE_ID)

    # make and populate the network_edges.csv file
    old_net_index = old_edge_cols.index(label_old_net)
    create_network_edges_csv(path_net_edges, old_edge_data, sender_receiver_to_edge_id,
                             sender_old_index, receiver_old_index, old_net_index)

    # make and populate the rds_edges.csv file
    rds_index = old_edge_cols.index(label_old_rds)
    create_rds_edges_csv(path_rds_edges, old_edge_data, sender_receiver_to_edge_id,
                         sender_old_index, receiver_old_index, rds_index)

    # make and populate the notes.csv file
    create_notes_csv(path_notes, path_old_edges, label_old_cnx, label_old_fn)

    # make and populate the note_edges.csv file
    note_name_to_note_id = w.get_no_null_entries_dict_from_csv(path_notes, 'note_name', 'note_id')
    cnx_note_index, fn_index = old_edge_cols.index(label_old_cnx), old_edge_cols.index(label_old_fn)
    create_note_edges_csv(path_note_edges, old_edge_data, sender_old_index, receiver_old_index,
                          cnx_note_index, fn_index, sender_receiver_to_edge_id, note_name_to_note_id)


def create_edges_csv(path_edges, old_edge_data, sender_index, receiver_index):
    """Input: edges.csv file path; data from the old edge file;
    sender and receiver index in that file.
    Output: Creates edges.csv file and populates it with all edge connections."""
    w.create_csv_add_column_labels(path_edges,
                                   [c.LABEL_EDGE_ID, c.LABEL_SENDER_PID, c.LABEL_RECEIVER_PID, c.LABEL_SENDER_RECEIVER])
    for i in range(len(old_edge_data)):
        row = old_edge_data[i]  # get each row from the old edge file
        w.append_row_to_csv(path_edges, [i+1, row[sender_index], row[receiver_index],  # and append the relevant data
                                         row[sender_index] + row[receiver_index]])   # to the new file


def create_network_edges_csv(path_net_edges, old_edge_data, sender_receiver_to_edge_id,
                             sender_index, receiver_index, net_index):
    """Input: net_edges.csv file path; data from the old edge file; sender_receiver to edge_id dictionary;
    sender, receiver, and network supplement index from old edges file; edge column label.
    Output: Creates the net_edges.csv file and populates it with all network supplement edge connections."""
    w.create_csv_add_column_labels(path_net_edges, [c.LABEL_EDGE_ID])
    for row in old_edge_data:  # for each row from the old edge file,
        if row[net_index] == 'Yes':  # if the column Net Supplement reads Yes,
            sender_receiver = row[sender_index] + row[receiver_index]
            edge_id = sender_receiver_to_edge_id[sender_receiver]  # get the edge_id of that sender/receiver pair
            w.append_row_to_csv(path_net_edges, [edge_id])  # and add it to the network_edges table


def create_rds_edges_csv(path_rds_edges, old_edge_data, sender_receiver_to_edge_id,
                         sender_index, receiver_index, rds_index):
    """Input: rds_edges.csv file path; data from the old edge file;
    sender, receiver, and rds edge index in that file; edge column label.
    Output: Creates the rds_edges.csv file and populates it with all rds edge connections."""
    w.create_csv_add_column_labels(path_rds_edges, [c.LABEL_EDGE_ID])
    for row in old_edge_data:  # for each row from the old edge file,
        if row[rds_index] == 'Yes':  # if the column RDS Edge reads Yes,
            sender_receiver = row[sender_index] + row[receiver_index]
            edge_id = sender_receiver_to_edge_id[sender_receiver]  # get the edge_id of that sender/receiver pair
            w.append_row_to_csv(path_rds_edges, [edge_id])  # and add it to the network_edges table


def create_notes_csv(path_notes, path_old_edges, cnx, fn):
    """Input: notes.csv file path; connection and field notes column labels in old edges file;
    note name and type column labels; note type entries for connection and field notes.
    Output: Creates notes.csv file and populates it with all unique connection and field note names, and note_ids."""
    w.create_csv_add_column_labels(path_notes, [c.LABEL_NOTE_NAME, c.LABEL_NOTE_TYPE])
    # add all unique names of connection notes to the notes.csv file
    w.add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label=cnx, type_entry_name=c.TYPE_CNX_NOTE)
    # add all unique names of field notes to the notes.csv file
    w.add_note_name_for_each_unique_note(path_notes, path_old_edges, old_col_label=fn, type_entry_name=c.TYPE_FN)
    # add note_id column as autoincrement to the notes.csv file
    w.add_auto_increment_col(path_notes, c.LABEL_NOTE_ID)


def create_note_edges_csv(path_note_edges, old_edge_data, sender_index, receiver_index, cnx_note_index, fn_index,
                          sender_receiver_to_edge_id, note_name_to_note_id):
    """Input: note_edges.csv file path; old edge data as list;
    sender, receiver, connection, field notes indices in old edges file;
    sender+receiver to edge_id dictionary, note name to note id dictionary; edge, note, note_edge column labels.
    Output: Creates note_edges.csv file and populates it with all pairs of edge id and note id, and note_edge_ids."""
    w.create_csv_add_column_labels(path_note_edges, [c.LABEL_EDGE_ID, c.LABEL_NOTE_ID])
    for row in old_edge_data:
        # get edge_id from edges.csv (using dict to look up sender+receiver_id) of current row in old edge file
        edge_id = sender_receiver_to_edge_id[row[sender_index] + row[receiver_index]]
        # append each edge_id and cnx_note_id pair to note_edges.csv
        w.append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, cnx_note_index, note_name_to_note_id,
                                                                         path_note_edges, edge_id)
        # append each edge_id and fn_id pair to note_edges.csv
        w.append_rows_of_edge_id_note_ids_to_new_file_from_old_edge_data(row, fn_index, note_name_to_note_id,
                                                                         path_note_edges, edge_id)
    w.add_auto_increment_col(path_note_edges, c.LABEL_NOTE_EDGE_ID)