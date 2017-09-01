import mysql.connector


def execute_query(statement: str, db_name, user_name, pwd, host_ip):
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()


def execute_query_return_list(statement: str, db_name, user_name, pwd, host_ip):
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(statement)
    result_list = [item[0] for item in cursor.fetchall()]  # get result as list of strings, rather than list of tuples
    cnx.commit()
    cursor.close()
    cnx.close()
    return result_list


def execute_query_insert_one_row(row_list, table_name, labels_list, db_name, user_name, pwd, host_ip):
    labels, values = '(', '('
    for label in labels_list:
        labels += "`" + label + "`" + ","
        values += "%s,"
    labels = labels[:-1] + ")"
    values = values[:-1] + ")"
    insert_row_statement = "INSERT INTO " + table_name + " " + labels + " VALUES " + values

    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(insert_row_statement, row_list)
    cnx.commit()
    cursor.close()
    cnx.close()


def execute_query_insert_multiple_rows(rows_list_of_lists, table_name, labels_list, db_name, user_name, pwd, host_ip):
    labels, values = '(', '('
    for label in labels_list:
        labels += "`" + label + "`" + ","
        values += "%s,"
    labels = labels[:-1] + ")"
    values = values[:-1] + ")"
    insert_row_statement = "INSERT INTO " + table_name + " " + labels + " VALUES " + values

    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    for row in rows_list_of_lists:
        cursor.execute(insert_row_statement, row)
        cnx.commit()
    cursor.close()
    cnx.close()


def populate_temp_table(pids_list: list, db_name, user_name, pwd, host_ip, table_name="temp", label="pid"):
    execute_query_drop_table(table_name, db_name, user_name, pwd, host_ip)
    execute_query_create_table(table_name, [label], db_name, user_name, pwd, host_ip)
    execute_query_insert_multiple_rows(pids_list, table_name, [label], db_name, user_name, pwd, host_ip)


def execute_query_drop_table(table_name, db_name, user_name, pwd, host_ip):
    statement = "DROP TABLE IF EXISTS " + table_name
    execute_query(statement, db_name, user_name, pwd, host_ip)


def execute_query_create_table(table_name, columns, db_name, user_name, pwd, host_ip):
    statement = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
    for c in columns:
        statement += "`" + c + "`" + " VARCHAR(255),"
    statement = statement[:-1] + ")"
    execute_query(statement, db_name, user_name, pwd, host_ip)


def execute_query_get_table_names(db_name, user_name, pwd, host_ip):
    tables = execute_query_return_list('SHOW TABLES', db_name, user_name, pwd, host_ip)
    return tables


def get_existing_column_labels_from_db_table(tbl_name, db_name, user_name, pwd, host_ip):
    """Output: Returns a list of column labels that already exist in the table
     -- for PR project they are the primary and foreign keys."""
    statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                "WHERE TABLE_SCHEMA='" + db_name + "' AND TABLE_NAME='" + tbl_name + "'"
    keys = execute_query_return_list(statement, db_name, user_name, pwd, host_ip)
    return keys

db_name, user_name, pwd, host_ip = 'puerto_rico', 'root', 'password', '192.168.4.30'
print()

