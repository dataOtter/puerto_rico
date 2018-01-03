"""Functions to run MySQL queries and return columns for extraction."""
import constants as c
import mysql_query_fuctions as q


def get_all_tbl_data_by_cols(tbl_name: str, cols: list):
    statement = "SELECT " + ', '.join(cols) + " FROM " + tbl_name
    data = q.execute_query_return_raw(statement)
    full_data = make_tbl_data_list_of_lists(data, cols)
    return full_data


def get_pids_tbl_data_by_cols(tbl_name: str, cols: list, pids_list: list):
    q.populate_temp_table(pids_list, table_name=c.SQL_FILTER_TEMP_TBL, label=c.SQL_FILTER_TEMP_COL)

    statement = "SELECT " + ', '.join(cols) + " FROM " + tbl_name + " WHERE "

    if tbl_name in c.RDSID_PRIM_KEY_TBLS:
        statement += "rds_id IN (SELECT rds_id FROM subjects_ids WHERE project_id IN " \
                     "(SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + "))"
    elif tbl_name in c.UNIQUEID_PRIM_KEY_TBLS:
        statement += "unique_id IN (SELECT unique_id FROM subjects_ids WHERE project_id IN " \
                     "(SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + "))"
    elif tbl_name in c.EDGEID_PRIM_KEY_TBLS:
        statement += "edge_id IN (SELECT edge_id FROM all_edges_index WHERE sender_pid IN " \
                     "(SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + "))"
    elif tbl_name in c.SENDERPID_PRIM_KEY_TBLS:
        statement += "sender_pid IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"
    elif tbl_name in c.PID_PRIM_KEY_TBLS:
        statement += "project_id IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"

    data = q.execute_query_return_raw(statement)
    full_data = make_tbl_data_list_of_lists(data, cols)
    return full_data


def make_tbl_data_list_of_lists(data: list, cols: list):
    full_data = [cols]
    for row in data:
        full_data.append(list(row))
    return full_data


def get_p1_columns(p1_tbls: list):
    col_labels = {}
    for tbl in p1_tbls:
        statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                    "WHERE TABLE_SCHEMA='puerto_rico' AND TABLE_NAME='" + tbl + "'"
        cols = q.execute_query_return_list(statement)
        #for i in range(len(cols)):
            #cols[i] = tbl + '__' + cols[i]
        col_labels[tbl] = cols
    #print(col_labels)
    return col_labels


def get_p2_columns(p2_tbls: list):
    col_labels = {}
    for tbl in p2_tbls:
        statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                    "WHERE TABLE_SCHEMA='puerto_rico' AND TABLE_NAME='" + tbl + "'"
        cols = q.execute_query_return_list(statement)
        # for i in range(len(cols)):
        # cols[i] = tbl + '__' + cols[i]
        col_labels[tbl] = cols
    #print(col_labels)
    return col_labels


def get_general_columns(general_tbls: list):
    col_labels = {}
    for tbl in general_tbls:
        statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                    "WHERE TABLE_SCHEMA='puerto_rico' AND TABLE_NAME='" + tbl + "'"
        cols = q.execute_query_return_list(statement)
        # for i in range(len(cols)):
        # cols[i] = tbl + '__' + cols[i]
        col_labels[tbl] = cols
    #print(col_labels)
    return col_labels


def get_phase_tbls():
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
    all_cols = {}
    tbls = get_phase_tbls()
    all_cols['phase1'] = get_p1_columns(tbls['p1'])
    all_cols['phase2'] = get_p2_columns(tbls['p2'])
    all_cols['edges&other'] = get_general_columns(tbls['general'])
    return all_cols


def sanity_check():
    all = get_phase_dict_of_tbl_dicts_of_col_lists()

    for phase, tbls in all.items():
        for tbl, cols in tbls.items():
            print(phase + ": " + tbl)
            print(cols)

#sanity_check()

#get_data_by_tbl_cols('p1_interviews', ['AgentId', 'Priority', 'LANG', 'SEED', 'DM4', 'FIN3', 'FIN3O'])
