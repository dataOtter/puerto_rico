import mysql_query_fuctions as q
import wrangling_functions as w


def pids_phase_1(db_name, user_name, pwd, host_ip):
    statement = "SELECT DISTINCT project_id FROM p1_screenings"
    return q.execute_query_return_list(statement, db_name, user_name, pwd, host_ip)


def pids_phase_2(db_name, user_name, pwd, host_ip):
    statement = "SELECT DISTINCT project_id FROM subjects_ids " \
                "WHERE unique_id IN (SELECT unique_id FROM p2_network_interviews)"
    return q.execute_query_return_list(statement, db_name, user_name, pwd, host_ip)


def pids_union_p1_p2(db_name, user_name, pwd, host_ip):
    pids1 = pids_phase_1(db_name, user_name, pwd, host_ip)
    pids2 = pids_phase_2(db_name, user_name, pwd, host_ip)
    return w.get_union_of_lists(pids1, pids2)


def pids_intersections_p1_p2(db_name, user_name, pwd, host_ip):
    pids1 = pids_phase_1(db_name, user_name, pwd, host_ip)
    pids2 = pids_phase_2(db_name, user_name, pwd, host_ip)
    return w.get_intersection_of_lists(pids1, pids2)



# TEST THIS OUT

def pids_subset_males(pids_list, db_name, user_name, pwd, host_ip, temp_table='temp', col='pid'):
    q.populate_temp_table(pids_list, db_name, user_name, pwd, host_ip, table_name=temp_table, label=col)
    sub_query = "SELECT * FROM " + temp_table

    main_query_p1 = "SELECT project_id FROM p1_screenings " \
                    "WHERE rds_id IN (SELECT rds_id FROM p1_interviews WHERE GEN = 1) " \
                    "AND project_id IN (" + sub_query + ")"
    males_p1 = q.execute_query_return_list(main_query_p1, db_name, user_name, pwd, host_ip)

    main_query_p2 = "SELECT project_id FROM p2_second_interviews " \
                    "WHERE P2FIGEN = 1 " \
                    "AND project_id IN (" + sub_query + ")"
    males_p2 = q.execute_query_return_list(main_query_p2, db_name, user_name, pwd, host_ip)

    return w.get_union_of_lists(males_p1, males_p2)


db_name, user_name, pwd, host_ip = 'puerto_rico', 'root', 'password', '192.168.4.30'


'''In Phase X
How many men were there?
How many people between X and Y?
How many people many used drugs more than X times a day?
How many people many used drugs less than X times a day?
'''