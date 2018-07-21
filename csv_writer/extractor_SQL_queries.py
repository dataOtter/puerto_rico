"""Functions to run MySQL queries and return columns for extraction."""
import constants as c
import mysql_query_fuctions as q


def get_all_tbl_data_by_cols(tbl_name: str, cols: list):
    """Input: Name of table to retrieve data from; name of columns to retrieve data from.
    Output: Returns requested data as rows list of fields lists."""
    cols_str_quotes = ''
    # add `` quotes to be really explicit about column names - e.g. for `INT` - used to be ', '.join(cols)
    for col in cols:
        cols_str_quotes += '`' + col + '`,'
    cols_str_quotes = cols_str_quotes[0:-1]  # get rid of trailing comma
    statement = "SELECT " + cols_str_quotes + " FROM " + tbl_name
    data = q.execute_query_return_raw(statement)
    full_data = make_tbl_data_list_of_lists(data, cols)
    return full_data


def get_single_subjects_tbl_of_all_given_tbls_and_cols(phase_tbl_cols_dict: dict, pids_list: list):
    """Input: Dictionary of study phase to tables to list of columns. List of project IDs to filter on.
    Output: Creates csv of all subject data from given columns of given tables."""
    exclude_cols_list = [c.LABEL_PID, c.LABEL_UNIQUE_ID, c.LABEL_RDS_ID]
    final_cols_list = exclude_cols_list  # to build the massive table
    select_statement = "SELECT " + c.SUBJECTS_IDS_FILE + "." + exclude_cols_list[0] \
                       + ", " + c.SUBJECTS_IDS_FILE + "." + exclude_cols_list[1] \
                       + ", " + c.SUBJECTS_IDS_FILE + "." + exclude_cols_list[2]
    from_statement = "FROM " + c.SUBJECTS_IDS_FILE
    # insert where statement here to filter on only the selected pids

    for phase in phase_tbl_cols_dict:
        for tbl, cols in phase_tbl_cols_dict[phase].items():  # for each table and associated list of columns,

            if tbl in c.RDSID_PRIM_KEY_TBLS:  # join the tables whose primary key is the rds_id
                select_statement += add_cols_to_select_statement(tbl, cols, final_cols_list, exclude_cols_list)
                from_statement += add_left_join_to_from_statement(tbl, c.LABEL_RDS_ID, c.SUBJECTS_IDS_FILE)

            elif tbl in c.UNIQUEID_PRIM_KEY_TBLS:  # join the tables whose primary key is the unique_id
                select_statement += add_cols_to_select_statement(tbl, cols, final_cols_list, exclude_cols_list)
                from_statement += add_left_join_to_from_statement(tbl, c.LABEL_UNIQUE_ID, c.SUBJECTS_IDS_FILE)

    where_statement = "WHERE " + c.SUBJECTS_IDS_FILE + "." + c.LABEL_PID + " IN ('" + "', '".join(pids_list) + "')"
    print((select_statement + " " + from_statement + " " + where_statement))

    data = q.execute_query_return_raw(select_statement + " " + from_statement + " " + where_statement)
    full_data = make_tbl_data_list_of_lists(data, final_cols_list)
    return full_data


def get_single_edges_tbl_of_all_given_tbls_and_cols(phase_tbl_cols_dict: dict, edges_list: list):
    """Input: Dictionary of study phase to tables to list of columns.
    Output: Creates csv of all edge data from given columns of given tables."""
    exclude_cols_list = [c.LABEL_EDGE_ID, c.LABEL_SENDER_PID, c.LABEL_RECEIVER_PID]
    final_cols_list = exclude_cols_list  # to build the massive table
    select_statement = "SELECT " + c.ALL_EDGES_INDEX_FILE + "." + exclude_cols_list[0] \
                       + ", " + c.ALL_EDGES_INDEX_FILE + "." + exclude_cols_list[1] \
                       + ", " + c.ALL_EDGES_INDEX_FILE + "." + exclude_cols_list[2]
    from_statement = "FROM " + c.ALL_EDGES_INDEX_FILE
    # insert where statement here to filter on only the selected edges

    for phase in phase_tbl_cols_dict:
        for tbl, cols in phase_tbl_cols_dict[phase].items():  # for each table and associated list of columns,
            # join the remaining tables whose primary key is the edge_id
            if tbl in c.EDGEID_PRIM_KEY_TBLS and tbl != c.ALL_EDGES_INDEX_FILE:
                # for notes, add a concatenated list of all notes associated with an edge_id
                if tbl == c.EDGES_TO_NOTES_FILE:
                    select_statement += ", GROUP_CONCAT(" + c.EDGES_TO_NOTES_FILE + "." \
                                        + c.LABEL_NOTE_ID + " SEPARATOR ', ') AS `" + c.LABEL_NOTE_ID + "s`"
                    final_cols_list.append(c.LABEL_NOTE_ID + "s")
                else:
                    select_statement += add_cols_to_select_statement(tbl, cols, final_cols_list, exclude_cols_list)
                from_statement += add_left_join_to_from_statement(tbl, c.LABEL_EDGE_ID, c.ALL_EDGES_INDEX_FILE)

    where_statement = " WHERE " + c.ALL_EDGES_INDEX_FILE + "." + c.LABEL_EDGE_ID + " IN (`" + '`, `'.join(edges_list) + "`)"
    # group by edge_id to get list of notes
    statement = select_statement + " " + from_statement + where_statement +\
                " GROUP BY " + c.ALL_EDGES_INDEX_FILE + "." + c.LABEL_EDGE_ID
    data = q.execute_query_return_raw(statement)
    full_data = make_tbl_data_list_of_lists(data, final_cols_list)
    return full_data


def add_cols_to_select_statement(tbl: str, cols: list, final_cols_list: list, exclude_cols_list: list):
    select_statement = ''
    for col in cols:
        if col not in [exclude_cols_list]:  # don't add multiples of these
            full_label = tbl + '.' + col
            final_cols_list.append(full_label)
            select_statement += ", " + full_label + ' AS `' + full_label + '`'
    return select_statement


def add_left_join_to_from_statement(tbl: str, key: str, tbl_to_join_to: str):
    return " LEFT JOIN " + tbl + " ON " + tbl + "." + key + " = " + tbl_to_join_to + "." + key


def get_pids_tbl_data_by_cols(tbl_name: str, cols: list, pids_list: list):
    """Input: Name of table from which to get all data;
    list of columns from which to get all data; list of PIDs of which to get all data.
    Output: Returns all data of the given PIDs from the given table and columns as rows list of fields list."""
    q.populate_temp_table(pids_list, table_name=c.SQL_FILTER_TEMP_TBL, label=c.SQL_FILTER_TEMP_COL)

    cols_str_quotes = ''
    for col in cols:  # add `` quotes to be really explicit about column names
        cols_str_quotes += '`' + col + '`,'
    cols_str_quotes = cols_str_quotes[0:-1]  # get rid of trailing comma

    statement = "SELECT " + cols_str_quotes + " FROM " + tbl_name + " WHERE "

    if tbl_name in c.RDSID_PRIM_KEY_TBLS:
        statement += "rds_id IN (SELECT rds_id FROM subjects_ids WHERE project_id IN " \
                     "(SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + "))"
    elif tbl_name in c.UNIQUEID_PRIM_KEY_TBLS:
        statement += "unique_id IN (SELECT unique_id FROM subjects_ids WHERE project_id IN " \
                     "(SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + "))"
    elif tbl_name in c.EDGEID_PRIM_KEY_TBLS:
        statement += "edge_id IN (SELECT edge_id FROM all_edges_index WHERE sender_pid IN " \
                     "(SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + "))"
    elif tbl_name in c.PID_PRIM_KEY_TBLS:
        statement += "project_id IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"

    data = q.execute_query_return_raw(statement)
    full_data = make_tbl_data_list_of_lists(data, cols)
    return full_data


def make_tbl_data_list_of_lists(data: list, cols: list):
    """Input: Data list of lists; columns list.
    Output: Rows list of fields list of the given data."""
    full_data = [cols]
    for row in data:
        full_data.append(list(row))
    return full_data


def get_phase_tbls_columns_dict(phase_tbls: list):
    """Input: List of names of all tables in given phase.
    Output: Returns dictionary of table name to list of columns in that table."""
    col_labels = {}
    for tbl in phase_tbls:
        statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                    "WHERE TABLE_SCHEMA='puerto_rico' AND TABLE_NAME='" + tbl + "'"
        cols = q.execute_query_return_list(statement)
        col_labels[tbl] = cols
    return col_labels


def get_phase_tbls_dict():
    """Input: None.
    Output: Returns dictionary of phase name to list of tables in that phase."""
    tbls = {'p1': [], 'p2': [], 'general': []}
    for tbl_name in c.ALL_TABLES:
        if 'p1' in tbl_name and 'p2' not in tbl_name:
            tbls['p1'].append(tbl_name)
        elif 'p2' in tbl_name and 'p1' not in tbl_name:
            tbls['p2'].append(tbl_name)
        else:
            tbls['general'].append(tbl_name)
    #print(tbls)
    return tbls


def get_phase_dict_of_tbl_dicts_of_col_lists():
    """Input: None.
    Output: Returns dictionary of phase name to dictionaries of table names to lists of column labels."""
    all_cols = {}
    tbls = get_phase_tbls_dict()
    all_cols['phase1'] = get_phase_tbls_columns_dict(tbls['p1'])
    all_cols['phase2'] = get_phase_tbls_columns_dict(tbls['p2'])
    all_cols['descriptives'] = get_phase_tbls_columns_dict(tbls['general'])
    return all_cols


def sanity_check():
    all = get_phase_dict_of_tbl_dicts_of_col_lists()

    for phase, tbls in all.items():
        for tbl, cols in tbls.items():
            print(phase + ": " + tbl)
            print(cols)

#sanity_check()

#get_all_tbl_data_by_cols('p1_interviews', ['AgentId', 'Priority', 'LANG', 'SEED', 'DM4', 'FIN3', 'FIN3O'])
