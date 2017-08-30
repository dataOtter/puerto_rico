import csv
import mysql.connector
import wrangling_functions as w


def add_columns_from_csv_to_db_table(full_path, table_name, db_name, keys, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be used; file path to the csv file to be used;
    list of primary and foreign keys already contained in the given table.
    Output: Adds the columns from the given csv file to the given table, skipping those that already exist.
    Returns a dictionary column_positions of column labels as keys and column indices in the csv as values."""
    csv_columns = w.get_first_row_of_csv_as_list(full_path)
    column_positions = get_col_label_to_col_index_in_csv_dict(csv_columns)

    if len(csv_columns) == len(keys):
        return column_positions

    else:
        statement = "ALTER TABLE " + table_name
        col_label_to_longest_entry = w.get_col_label_to_longest_entry_dict(full_path)

        for col in csv_columns:
            if col not in keys:
                max_col_len = col_label_to_longest_entry[col] + 1
                statement += " ADD COLUMN `" + col + "` "
                if max_col_len >= 255:
                    statement += "TEXT,"
                else:
                    statement += "VARCHAR(" + str(max_col_len) + "),"

        statement = statement[:-1] + ";"
        execute_mysql_statement(db_name, user_name, pwd, host_ip, statement)

    return column_positions


def get_col_label_to_col_index_in_csv_dict(csv_columns: list):
    column_positions = {}
    for i in range(len(csv_columns)):
        col = csv_columns[i]
        column_positions[col] = i
    return column_positions


def execute_mysql_statement(db_name, user_name, pwd, host_ip, statement: str):
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_data(full_path, db_name, column_positions, user_name, pwd, host_ip, tbl_name):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be used; file path to the csv file to be used;
    dictionary of column_positions linking column labels to row indices in the csv.
    Output: Inserts the data contained in the given csv into the given table."""
    labels, values = '(', '('
    
    for label in column_positions:
        labels += "`" + label + "`" + ","
        values += "%s,"

    labels = labels[:-1] + ")"
    values = values[:-1] + ")"

    insert_row_statement = "INSERT INTO " + tbl_name + " " + labels + " VALUES " + values

    cnx = mysql.connector.connect(user=user_name, password=pwd,
                                  host=host_ip,
                                  database=db_name)
    cursor = cnx.cursor()

    rows = w.get_csv_as_list(full_path)[1:]

    for row in rows:
        row_values = ()
        for label, index in column_positions.items():
            if row[index] == '#NULL!':
                row_values += ('',)
            else:
                row_values += (row[index],)
        print(row_values)
        cursor.execute(insert_row_statement, row_values)
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


def get_keys_from_db(db_name, user_name, pwd, host_ip, tbl_name):
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


'''fp = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\test_data\\p1\\screener.csv"
tbn = "p1_screenings"
db = 'puerto_rico'
k = ['COUPID']
user = 'root'
pwd = 'password'
host_ip = '192.168.4.30'''''

#get_keys_from_db(db,user,pwd,host_ip,tbn)
#drop_table(tbn, db, user, pwd, host_ip)
#create_table(tbn, db, k, user, pwd, host_ip)
#cp = add_columns(fp, tbn, db, k, user, pwd, host_ip)
#insert_data(fp, db, cp, user, pwd, host_ip)
