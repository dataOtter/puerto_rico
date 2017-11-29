"""Functions to run MySQL queries and return "filtered" project ID lists."""
import constants as c
import mysql_query_fuctions as q


def pids_phase_1():
    """Input: None.
    Output: Returns list of of all phase 1 project IDs."""
    statement = "SELECT DISTINCT project_id FROM p1_screenings"
    return q.execute_query_return_list(statement)


def pids_phase_2():
    """Input: None.
    Output: Returns list of of all phase 2 project IDs."""
    statement = "SELECT DISTINCT sender_pid FROM p2_network_supplement_edges"
    return q.execute_query_return_list(statement)


def pids_gender(pids_list, gender_code):
    """Input: List of project IDs to filter; code indicating which gender to filter on.
    Output: Returns list of all remaining project IDs for the selected gender and given project IDs list."""
    q.populate_temp_table(pids_list, table_name=c.SQL_FILTER_TEMP_TBL, label=c.SQL_FILTER_TEMP_COL)
    query = "SELECT DISTINCT project_id FROM subjects_ids " \
            "WHERE (project_id IN " \
            "(SELECT project_id FROM p1_screenings WHERE rds_id IN " \
            "(SELECT rds_id FROM p1_interviews WHERE GEN = " + str(gender_code) + "))" \
            "OR project_id IN (SELECT project_id FROM p2_first_interviews WHERE P2FIGEN = " + str(gender_code) + "))" \
            "AND project_id IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"
    return q.execute_query_return_list(query)


def pids_age_range(pids_list, min_age=0, max_age=999):
    """Input: List of project IDs to filter; minimum age and maximum age to filter on.
    Output: Returns list of all remaining project IDs for the selected age range and given project IDs list."""
    q.populate_temp_table(pids_list, table_name=c.SQL_FILTER_TEMP_TBL, label=c.SQL_FILTER_TEMP_COL)
    query = "SELECT DISTINCT project_id FROM subjects_ids " \
                 "WHERE (project_id IN " \
                 "(SELECT DISTINCT project_id FROM p1_screenings " \
                    "WHERE EP2 >= " + str(min_age) + " AND EP2 <= " + str(max_age) + \
                 ") OR project_id IN " \
                 "(SELECT DISTINCT project_id FROM p2_first_interviews " \
                    "WHERE P2FIAGE >= " + str(min_age) + " AND P2FIAGE <= " + str(max_age) + \
                 ")) AND project_id IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"
    return q.execute_query_return_list(query)


def pids_drug_use_per_day(pids_list, sign: str, use_per_day):
    """Input: List of project IDs to filter; sign and amount indicating minimum/maximum drug use per day to filter on.
    Output: Returns list of all remaining project IDs for selected daily drug use cutoff and given project IDs list."""
    q.populate_temp_table(pids_list, table_name=c.SQL_FILTER_TEMP_TBL, label=c.SQL_FILTER_TEMP_COL)
    codes = get_drug_use_cutoff_codes(use_per_day)
    p1code, p2code = codes[0], codes[1]
    query = "SELECT project_id FROM subjects_ids " \
            "WHERE (rds_id IN (SELECT rds_id FROM p1_interviews WHERE ID2 " + sign + str(p1code) + \
            ") OR project_id IN (SELECT project_id FROM p2_first_interviews WHERE P2FIID2 " + sign + str(p2code) + \
            ")) AND project_id IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"
    return q.execute_query_return_list(query)


def get_drug_use_cutoff_codes(cutoff):
    """Input: Selected daily drug use cutoff.
    Output: Returns the cutoff's csv file data codes for phases 1 and 2."""
    if cutoff == 1:
        p1code = 3
        p2code = 4
    elif 2 <= cutoff <= 3:
        p1code = 2
        p2code = 3
    elif 4 <= cutoff < 8:
        p1code = 1
        p2code = 2
    elif cutoff >= 8:
        p1code = 1
        p2code = 1
    else:
        p1code = 8
        p2code = 10
    return [p1code, p2code]


def pids_country_born(pids_list, country_code):
    """Input: List of project IDs to filter; code of the country born in to filter on.
    Output: Returns list of all remaining project IDs for the selected country of birth and given project IDs list."""
    q.populate_temp_table(pids_list, table_name=c.SQL_FILTER_TEMP_TBL, label=c.SQL_FILTER_TEMP_COL)
    query = "SELECT DISTINCT project_id FROM subjects_ids " \
            "WHERE (project_id IN " \
            "(SELECT project_id FROM p1_screenings WHERE rds_id IN " \
            "(SELECT rds_id FROM p1_interviews WHERE DM4 = " + str(country_code) + "))" \
            "OR project_id IN (SELECT project_id FROM p2_first_interviews WHERE P2FIDM4 = " + str(country_code) + "))" \
            "AND project_id IN (SELECT * FROM " + c.SQL_FILTER_TEMP_TBL + ")"
    return q.execute_query_return_list(query)


def pids_males(pids_list):
    """Input: List of project IDs to filter.
    Output: Returns project IDs list of all males within the given project IDs list."""
    return pids_gender(pids_list, 1)


def pids_females(pids_list):
    """Input: List of project IDs to filter.
    Output: Returns project IDs list of all females within the given project IDs list."""
    return pids_gender(pids_list, 2)


def pids_transgender(pids_list):
    """Input: List of project IDs to filter.
    Output: Returns project IDs list of all transgenders within the given project IDs list."""
    return pids_gender(pids_list, 3)


def pids_min_drug_use_per_day(pids_list, min_use_per_day=1):
    """Input: List of project IDs to filter; amount of minimum daily drug use, defaulting to 1.
    Output: Returns project IDs list of all participants using at least the given amount of times per day,
    within the given project IDs list."""
    return pids_drug_use_per_day(pids_list, '<=', min_use_per_day)


def pids_max_drug_use_per_day(pids_list, max_use_per_day=1):
    """Input: List of project IDs to filter; amount of maximum daily drug use, defaulting to 1.
    Output: Returns project IDs list of all participants using at most the given amount of times per day,
    within the given project IDs list."""
    return pids_drug_use_per_day(pids_list, '>', max_use_per_day)


def pids_born_pr(pids_list):
    """Input: List of project IDs to filter.
    Output: Returns project IDs list of all participants born in Puerto Rico."""
    return pids_country_born(pids_list, 1)


def pids_born_cont_us(pids_list):
    """Input: List of project IDs to filter.
        Output: Returns project IDs list of all participants born in Continental US."""
    return pids_country_born(pids_list, 2)


def pids_born_dom_rep(pids_list):
    """Input: List of project IDs to filter.
    Output: Returns project IDs list of all participants born in the Dominican Republic."""
    return pids_country_born(pids_list, 3)


def pids_born_other(pids_list):
    """Input: List of project IDs to filter.
    Output: Returns project IDs list of all participants born in other countries."""
    return pids_country_born(pids_list, 4)


def sender_receiver_from_edges(pids_list1, pids_list2):
    """Input: Two pid lists of the groups whose relationship edges to return, e.g. males and females.
    Output: Returns a sender_receiver list of those relationships - including both permutations of each."""
    q.populate_temp_table(pids_list1, table_name='temp1', label='sender_receiver')
    q.populate_temp_table(pids_list2, table_name='temp2', label='sender_receiver')
    query = "SELECT * FROM all_edges_index " \
            "WHERE (sender_pid IN (SELECT * FROM temp1) " \
            "AND receiver_pid IN (SELECT * FROM temp2)) " \
            "OR (sender_pid IN (SELECT * FROM temp2) " \
            "AND receiver_pid IN (SELECT * FROM temp1))"
    return q.execute_query_return_list(query)


def get_full_edge_ids_for_pids_list(pids_list: list):
    """Input: PID list of the participants whose relationship edges to return.
    Output: Returns a sender_receiver list of those relationships - including both permutations of each relationship."""
    q.populate_temp_table(pids_list, table_name='temp', label='sender_or_receiver')
    query = "SELECT full_edge_id FROM all_edges_index " \
            "WHERE sender_pid IN (SELECT * FROM temp) " \
            "OR receiver_pid IN (SELECT * FROM temp)"
    return q.execute_query_return_list(query)


def get_unique_sender_receiver_pairs(sender_receiver_list):
    """Input: List of sender_receiver pairs.
    Output: Returns a sender_receiver list without duplicates (i.e. removes one pair of pid1_pid2 and pid2_pid1)."""
    for sr in sender_receiver_list:
        try:
            sender_receiver_list.remove(sr[5:] + sr[:5])
        except Exception:
            pass
    return sender_receiver_list


'''p1_first_interviews: ID2
[In the last 12 months, on average, how often did you inject drugs?]
1 [4 or more times per day]
2 [2-3 times per day]
3 [One time per day]
4 [2-6 times per week]
5 [One time per week]
6 [2-3 times per month]
7 [One time per month] -- currently max in data
8 [Less than one time per month]
9 [Don't know/refused to answer]

p2_first_interviews: ID2 
[In the past 3 months, on average, how often did you inject drugs? ]
p2_second_interviews: ID2
[Since your last interview, on average, how often did you inject? ]
1 [8 or more times per day]
2 [4-7 times per day]
3 [2-3 times per day]
4 [One time per day]
5 [2-6 times per week]
6 [One time per week]
7 [2-3 times per month]  -- currently max in p2_first_interviews data
8 [One time per month]
10 [Less than one time per month] --  -- currently max in p2_second_interviews data
99 [Don't know/refused to answer]'''
