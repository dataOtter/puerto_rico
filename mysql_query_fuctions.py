import mysql.connector


def execute_mysql_statement(db_name, user_name, pwd, host_ip, statement: str):
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()


def drop_table(table_name, db_name, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a
    connection to the desired database; name of the table to be dropped.
    Output: Deletes the given table."""
    statement = "DROP TABLE IF EXISTS " + table_name
    execute_mysql_statement(db_name, user_name, pwd, host_ip, statement)


def create_table(table_name, db_name, columns, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be created; list of columns to be added while creating the table.
    Output: Creates a table with the given inputs."""
    statement = "CREATE TABLE " + table_name + " ("
    for c in columns:
        statement += "`" + c + "`" + " VARCHAR(255),"
    statement = statement[:-1] + ")"
    execute_mysql_statement(db_name, user_name, pwd, host_ip, statement)


def get_table_names(db_name, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database.
    Output: Returns a list of all table names that exist in the given database."""
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute('SHOW TABLES')
    tbls = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()

    tables = []
    for tbl in tbls:
        tables.append(tbl[0])

    return tables


def get_existing_column_labels_from_db_table(db_name, user_name, pwd, host_ip, tbl_name):
    """Input: Database name, username, password and host ip address to open
    a connection to the desired database; name of the table to be used.
    Output: Returns a list of column labels that already exist in the table
     -- for PR project the are the primary and foreign keys."""
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   "WHERE TABLE_SCHEMA='" + db_name + "' AND TABLE_NAME='" + tbl_name + "'")
    keys_messy = cursor.fetchall()

    cnx.commit()
    cursor.close()
    cnx.close()

    keys = []
    for key in keys_messy:
        keys.append(key[0])

    return keys


