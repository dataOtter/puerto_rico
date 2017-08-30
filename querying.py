import mysql_query_fuctions as q


def execute_mysql_statement(db_name, user_name, pwd, host_ip, statement: str):
    q.execute_mysql_statement(db_name, user_name, pwd, host_ip, statement)


def drop_table(table_name, db_name, user_name, pwd, host_ip):
    q.drop_table(table_name, db_name, user_name, pwd, host_ip)


def create_table(table_name, db_name, columns, user_name, pwd, host_ip):
    q.create_table(table_name, db_name, columns, user_name, pwd, host_ip)


def get_table_names(db_name, user_name, pwd, host_ip):
    q.get_table_names(db_name, user_name, pwd, host_ip)


def get_existing_column_labels_from_db_table(db_name, user_name, pwd, host_ip, tbl_name):
    q.get_existing_column_labels_from_db_table(db_name, user_name, pwd, host_ip, tbl_name)


