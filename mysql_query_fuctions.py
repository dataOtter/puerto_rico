"""Functions to execute various types of MySQL queries and return retrieved data, where applicable."""
import mysql.connector
import constants as c


def get_sql_db_connection():
    if c.GLOBAL_CNX_COUNT == -1:
        c.GLOBAL_CNX = mysql.connector.connect(user=c.USER_NAME, password=c.PASSWORD, host=c.HOST_IP, database=c.DB_NAME)
        c.GLOBAL_CNX_COUNT += 1  # now counter is 0
    assert (c.GLOBAL_CNX_COUNT == 0), "Extra connection 'opened' but not 'closed'"
    c.GLOBAL_CNX_COUNT += 1  # add 1 for each connection given to a caller
    return c.GLOBAL_CNX


def decr_global_cnx_count():
    assert (c.GLOBAL_CNX_COUNT == 1), "Trying to 'close' a connection not 'opened'"
    c.GLOBAL_CNX_COUNT -= 1


def close_sql_db_connection():
    c.GLOBAL_CNX.close()
    c.GLOBAL_CNX_COUNT = -1


def execute_query(statement: str):
    """Input: MySQL statement as a string; only for statements that do not retrieve any data.
    Output: Executes the given statement using the database details set in the constants file."""
    cnx = get_sql_db_connection()
    cursor = cnx.cursor()
    if c.LOGGING_SQL_QUERIES or c.LOGGING_SQL_INSERT_VALUES:
        print(statement)
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    decr_global_cnx_count()


def execute_query_return_list(statement: str):
    """Input: MySQL statement as a string; only for statements that retrieve data.
    Output: Executes the given statement using the database details set in the constants file.
    Returns the retrieved data as a list of strings."""
    cnx = get_sql_db_connection()
    cursor = cnx.cursor()
    if c.LOGGING_SQL_QUERIES or c.LOGGING_NONE_INSERT_SQL_QUERIES:
        print(statement)
    cursor.execute(statement)
    result_list = [item[0] for item in cursor.fetchall()]  # get result as list of strings, rather than list of tuples
    cnx.commit()
    cursor.close()
    decr_global_cnx_count()
    return result_list


def execute_query_return_raw(statement: str):
    """Input: MySQL statement as a string; only for statements that retrieve data.
        Output: Executes the given statement using the database details set in the constants file.
        Returns the retrieved data raw as is."""
    cnx = get_sql_db_connection()
    cursor = cnx.cursor()
    if c.LOGGING_SQL_QUERIES or c.LOGGING_NONE_INSERT_SQL_QUERIES:
        print(statement)
    cursor.execute(statement)
    res = cursor.fetchall()
    cnx.commit()
    cursor.close()
    decr_global_cnx_count()
    return res


def get_insert_row_statement(table_name: str, col_labels: list):
    """Input: Name of the table into which to insert a row; list of column labels of that table.
    Output: Returns the appropriate MySQL statement for inserting a row into the given table."""
    labels, values = '(', '('
    for label in col_labels:
        labels += "`" + label + "`" + ","
        values += "%s,"
    labels = labels[:-1] + ")"
    values = values[:-1] + ")"
    return "INSERT INTO " + table_name + " " + labels + " VALUES " + values


def execute_query_insert_one_row(row: list, table_name: str, col_labels: list):
    """Input: Single row to be inserted, as a list; name of the table into which to insert a row;
    list of column labels of that table.
    Output: Inserts the given row into the given table using the database details set in the constants file."""
    insert_row_statement = get_insert_row_statement(table_name, col_labels)
    cnx = get_sql_db_connection()
    cursor = cnx.cursor()
    if c.LOGGING_SQL_QUERIES:
        print(insert_row_statement, row)
    cursor.execute(insert_row_statement, row)
    cnx.commit()
    cursor.close()
    decr_global_cnx_count()


def execute_query_insert_multiple_rows(all_rows: list, table_name: str, col_labels: list):
    """Input: Multiple rows to be inserted, as list of lists; name of the table into which to insert a row;
    list of column labels of that table.
    Output: Inserts the given rows into the given table using the database details set in the constants file."""
    insert_row_statement = get_insert_row_statement(table_name, col_labels)
    cnx = get_sql_db_connection()
    cursor = cnx.cursor()
    if c.LOGGING_SQL_INSERT_VALUES:
        print("Inserting " + str(len(all_rows)) + " rows: " + str(all_rows))
    for row in all_rows:
        if isinstance(row, str):
            row = [row]
        if c.LOGGING_SQL_QUERIES:
            print(insert_row_statement, row)
        cursor.execute(insert_row_statement, row)
        cnx.commit()
    decr_global_cnx_count()


def populate_temp_table(pids_list: list, table_name="temp", label="pid"):
    """Input: List of project IDs; name of the table into which to insert a row, defaulting to "temp";
    string of the column label of that table, defaulting to "pid".
    Output: Creates and populates a temporary table for testing purposes
    using the database details set in the constants file."""
    execute_query_drop_table(table_name)
    execute_query_create_table(table_name, [label])
    execute_query_insert_multiple_rows(pids_list, table_name, [label])


def execute_query_drop_table(table_name):
    """Input: Name of the table to delete.
    Output: Deletes the given table using the database details set in the constants file."""
    statement = "DROP TABLE IF EXISTS " + table_name
    execute_query(statement)


def execute_query_create_table(table_name, columns: list, data_type='TEXT'):
    """Input: Name of the table to create; list of columns to add;
    data type to set for each column, defaulting to 'TEXT'.
    Output: Creates the given table and columns using the database details set in the constants file."""
    statement = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
    for c in columns:
        statement += "`" + c + "` " + data_type + ","
    statement = statement[:-1] + ")"
    execute_query(statement)


def execute_query_get_table_names():
    """Input: None.
    Output: Returns a list of all table names using the database details set in the constants file."""
    tables = execute_query_return_list('SHOW TABLES')
    return tables


def get_existing_column_labels_from_db_table(tbl_name):
    """Input: Name of the table from which to get columns labels.
    Output: Returns list of column labels of the given table using the database details set in the constants file."""
    statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                "WHERE TABLE_SCHEMA='" + c.DB_NAME + "' AND TABLE_NAME='" + tbl_name + "'"
    keys = execute_query_return_list(statement)
    return keys  # for PR project, before populating DB, these are the primary and foreign keys


def execute_query_drop_db():
    """Input: Name of the database to delete.
    Output: Deletes the given database using the database details set in the constants file."""
    cnx = mysql.connector.connect(user=c.USER_NAME, password=c.PASSWORD, host=c.HOST_IP)
    cursor = cnx.cursor()
    statement = "DROP DATABASE IF EXISTS " + c.DB_NAME
    if c.LOGGING_SQL_QUERIES or c.LOGGING_NONE_INSERT_SQL_QUERIES:
        print(statement)
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()


def execute_query_create_db():
    execute_query_drop_db()
    cnx = mysql.connector.connect(user=c.USER_NAME, password=c.PASSWORD, host=c.HOST_IP)
    cursor = cnx.cursor()
    f = open(c.CREATE_DB_SQL_FILE_PATH)
    full_sql = f.read()
    sql_commands = full_sql.replace('\n', '').split(';')[:-1]
    for sql_command in sql_commands:
        if c.LOGGING_SQL_QUERIES or c.LOGGING_NONE_INSERT_SQL_QUERIES:
            print(sql_command)
        cursor.execute(sql_command)
        cnx.commit()

    cursor.close()
    cnx.close()
