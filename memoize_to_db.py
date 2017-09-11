import mysql_query_fuctions as q
import constants as c
import pid_filter_instances as pidf
import copy
import hashlib as h


def get_filters_string(filters: list):
    f_string_list = []
    for f in filters:
        f_string_list.append(f.get_kind_and_cat())
    f_sorted_list = sorted(f_string_list)
    f_string = ','.join(f_sorted_list)
    return f_string


def get_pids_string(pids: list):
    return ','.join(pids)


def add_filter_pid_pair_to_db_table(filters_list: list, pids_list: list):
    filters_str = get_filters_string(filters_list)
    pids_str = get_pids_string(pids_list)
    filters_hash = h.md5(filters_str.encode()).hexdigest()
    row = [filters_str, pids_str, filters_hash]
    exists = get_row_from_db_table(filters_hash, col_to_get=c.MEMOIZING_TABLE_COLUMN_LABELS[0])
    if not exists:
        q.execute_query_insert_one_row(row, c.MEMOIZING_TABLE_NAME, c.MEMOIZING_TABLE_COLUMN_LABELS,
                                       c.DB_NAME, c.USER_NAME, c.PASSWORD, c.HOST_IP)


def get_row_from_db_table(comparison_str, col_to_get: str):
    query = "SELECT " + col_to_get + " FROM " + c.MEMOIZING_TABLE_NAME + \
            " WHERE " + c.MEMOIZING_HASH_COLUMN_LABEL + " = '" + comparison_str + "'"
    row_string_list = q.execute_query_return_list(query, c.DB_NAME, c.USER_NAME, c.PASSWORD, c.HOST_IP)
    if len(row_string_list) > 0:
        if len(row_string_list[0]) == 0:
            row_list = []
        else:
            row_list = row_string_list[0].split(',')
    else:
        row_list = None
    return row_list


def get_filters_result_pids_from_memo_table(filters: list):
    filters_str = get_filters_string(filters)
    filters_hash = h.md5(filters_str.encode()).hexdigest()
    results_pids = get_row_from_db_table(filters_hash, col_to_get=c.MEMOIZING_TABLE_COLUMN_LABELS[1])
    return results_pids


def clear_memoize_table():
    q.execute_query_drop_table(c.MEMOIZING_TABLE_NAME, c.DB_NAME, c.USER_NAME, c.PASSWORD, c.HOST_IP)
    q.execute_query_create_table(c.MEMOIZING_TABLE_NAME, c.MEMOIZING_TABLE_COLUMN_LABELS, data_type='TEXT')
    q.execute_query("ALTER TABLE " + c.MEMOIZING_TABLE_NAME + " MODIFY COLUMN " +
                    c.MEMOIZING_HASH_COLUMN_LABEL + " VARCHAR(255), ADD INDEX " +
                    c.MEMOIZING_HASH_COLUMN_LABEL + " (" + c.MEMOIZING_HASH_COLUMN_LABEL + ")")


def get_filter_subsets(all_individual_filters: list, all_filter_subsets: list, fs):
    to_print = []
    for fltr in all_individual_filters:
        to_print.append(fltr.get_kind_and_cat())
    print(to_print)  # print remaining filters to be checked and potentially added to the db

    if len(all_individual_filters) >= 1:  # if there are filters,
        first_filter = all_individual_filters[0]  # get the first (new/unused) filter of the given list of filters
        subsets_copy = copy.deepcopy(all_filter_subsets)  # make a copy of the all_filter_subsets list of lists

        for prev_filter_combo in subsets_copy:  # for every filter-combo (list) in that copy,
            new_filter_combo = copy.deepcopy(prev_filter_combo)
            new_filter_combo.append(first_filter)  # append the first new/unused filter

            # get the pids from the memo table
            temp_pids_list_exists = get_filters_result_pids_from_memo_table(new_filter_combo)
            if not temp_pids_list_exists:  # if this filter combo has not been entered yet

                # get pids from previous filter combo, then add just that filter to it
                prev_filter_combo_pids = get_filters_result_pids_from_memo_table(prev_filter_combo)
                if prev_filter_combo_pids is None:
                    filter_combo_pids = fs.apply_all_given_filters_to_all_pids(new_filter_combo)
                # get pids with current temp filters
                #filter_combo_pids = fs.apply_all_given_filters_to_all_pids(new_filter_combo)
                else:
                    filter_combo_pids = fs.apply_one_filter_to_given_pids(first_filter, prev_filter_combo_pids)

                # and add the filter-combo and its pids to the memo table
                add_filter_pid_pair_to_db_table(new_filter_combo, filter_combo_pids)
            else:
                filter_combo_pids = temp_pids_list_exists

            # if this filter-combo returns pids (if not, no need to explore this combo as part of other combos),
            if len(filter_combo_pids) > 0:
                all_filter_subsets.append(new_filter_combo)  # append it to the list of filter subsets

    filters2 = all_individual_filters[1:]  # remove first filter
    if len(filters2) >= 1:  # if this shorter list of filters still has filters left,
        #  do recursion call with shorter filters list and updated subsets list
        all_filter_subsets = get_filter_subsets(filters2, all_filter_subsets, fs)
    return all_filter_subsets


def make_memoize_table():
    clear_memoize_table()
    fs = pidf.FilterSystem()
    get_filter_subsets(fs.get_inactive_filters(), [[]], fs)
