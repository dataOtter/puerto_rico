import wrangling_functions as w


def create_all_edge_csvs(path, edges_file='edges', old_edge_file='edge_index_5_2_17', net_edges_file='network_edges',
                         rds_edges_file='rds_edges', notes_file='notes'):
    """Input: General file path; csv file names of all edge files.
    Output: Creates and populates all edge files."""
    path_edges = path + edges_file + ".csv"
    path_old_edges = path + old_edge_file + ".csv"
    path_net_edges = path + net_edges_file + ".csv"
    path_rds_edges = path + rds_edges_file + ".csv"
    path_notes = path + notes_file + ".csv"

    sender, receiver, edge = 'sender_pid', 'receiver_pid', 'edge_id'
    net, rds = 'Net Supplement', 'RDS Edge'
    cnx, fn = 'Connection Notes', 'Field Notes'
    replace_with = {'Sender ID': sender, 'Receiver ID': receiver}
    w.fix_column_labels_csv(path_old_edges, replace_with)

    x = w.get_csv_as_list(path_old_edges)
    old_edge_cols, old_edge_data = x[0], x[1:]

    sender_index, receiver_index = old_edge_cols.index(sender), old_edge_cols.index(receiver)
    net_index, rds_index = old_edge_cols.index(net), old_edge_cols.index(rds)
    cnx_note_index, fn_index = old_edge_cols.index(cnx), old_edge_cols.index(fn)

    #create_edges_csv(path_edges, old_edge_data, sender_index, receiver_index)
    #create_network_edges_csv(path_net_edges, old_edge_data, sender_index, receiver_index, net_index)
    #create_rds_edges_csv(path_rds_edges, old_edge_data, sender_index, receiver_index, rds_index)
    create_notes_csv(path_notes, path_old_edges, old_edge_data, cnx, cnx_note_index, fn, fn_index, edge='edge_id')


def create_edges_csv(path_edges, old_edge_data, sender_index, receiver_index,
                     sender='sender_pid', receiver='receiver_pid', edge='edge_id'):
    """Input: edges.csv file path; data from the old edge file;
    sender and receiver index in that file; sender, receiver, edge column labels.
    Output: Creates the edges.csv file and
    populates it with all edge connections (edge id, sender pid, receiver pid)."""
    w.create_csv_add_column_labels(path_edges, [edge, sender, receiver])

    for row in old_edge_data:
        w.append_row_to_csv(path_edges, [row[sender_index] + row[receiver_index],
                                         row[sender_index], row[receiver_index]])


def create_network_edges_csv(path_net_edges, old_edge_data, sender_index, receiver_index, net_index, edge='edge_id'):
    """Input: net_edges.csv file path; data from the old edge file;
        sender, receiver, and network supplement index in that file; edge column label.
        Output: Creates the net_edges.csv file and
        populates it with all network supplement edge connections."""
    w.create_csv_add_column_labels(path_net_edges, [edge])
    for row in old_edge_data:
        if row[net_index] == 'Yes':
            w.append_row_to_csv(path_net_edges, [row[sender_index] + row[receiver_index]])


def create_rds_edges_csv(path_rds_edges, old_edge_data, sender_index, receiver_index, rds_index, edge='edge_id'):
    """Input: rds_edges.csv file path; data from the old edge file;
            sender, receiver, and rds edge index in that file; edge column label.
            Output: Creates the rds_edges.csv file and
            populates it with all rds edge connections."""
    w.create_csv_add_column_labels(path_rds_edges, [edge])
    for row in old_edge_data:
        if row[rds_index] == 'Yes':
            w.append_row_to_csv(path_rds_edges, [row[sender_index] + row[receiver_index]])


def create_note_edges_csv(path_rds_edges, old_edge_data, sender_index, receiver_index, rds_index, edge='edge_id'):
    """Input: rds_edges.csv file path; data from the old edge file;
            sender, receiver, and rds edge index in that file; edge column label.
            Output: Creates the rds_edges.csv file and
            populates it with all rds edge connections."""


def create_notes_csv(path_notes, path_old_edges, old_edge_data, cnx, cnx_note_index, fn, fn_index, edge='edge_id'):
    cnx_data = w.get_data_from_one_col_as_list(path_old_edges, cnx)
    fn_data = w.get_data_from_one_col_as_list(path_old_edges, fn)
    cnx_set_list = list(set(cnx_data))
    fn_set_list = list(set(fn_data))

    i = 0
    while i < len(cnx_set_list):
        entry = cnx_set_list[i]
        if ',' in entry:
            entry_split = entry.split(',')
            cnx_set_list.remove(entry)
            for e in entry_split:
                cnx_set_list.append(e.strip())
        i += 1

    j = 0
    while j < len(fn_set_list):
        entry = fn_set_list[j]
        if ',' in entry:
            entry_split = entry.split(',')
            fn_set_list.remove(entry)
            for e in entry_split:
                fn_set_list.append(e.strip())
        elif ';' in entry:
            entry_split = entry.split(';')
            fn_set_list.remove(entry)
            for e in entry_split:
                fn_set_list.append(e.strip())
        else:
            entry.strip()
            j += 1

    unique_cnx_data = set(cnx_set_list)
    unique_fn_data = set(fn_set_list)

    print(len(unique_cnx_data))
    for e in unique_cnx_data:
        print(e)


create_all_edge_csvs("C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\")

# put all unique values in the notes.csv table
# make 