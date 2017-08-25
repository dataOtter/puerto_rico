import csv
import mysql.connector


def add_columns(file_path, table_name, db_name, keys, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be used; file path to the csv file to be used;
    list of primary and foreign keys already contained in the given table.
    Output: Adds the columns from the given csv file to the given table, skipping those that already exist.
    Returns a dictionary column_positions of column labels as keys and column indices in the csv as values."""
    reader = csv.reader(open(file_path, "r"), delimiter=",")
    x = list(reader)
    columns = x[0]
    column_positions = {}

    statement = "ALTER TABLE " + table_name

    for i in range(len(columns)):
        c = columns[i]
        if c not in keys:
            statement += " ADD COLUMN `" + c + "` VARCHAR(255),"
        column_positions[c] = i

    statement = statement[:-1] + ";"

    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()

    return column_positions


def insert_data(file_path, db_name, column_positions, user_name, pwd, host_ip, tbl_name):
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

    reader = csv.reader(open(file_path, "r"), delimiter=",")
    x = list(reader)
    rows = x[1:]

    for row in rows:
        row_values = ()
        for label, index in column_positions.items():
            if row[index] == '#NULL!':
                row_values += ('',)
            else:
                row_values += (row[index],)
        cursor.execute(insert_row_statement, row_values)
        cnx.commit()

    cursor.close()
    cnx.close()


def drop_table(table_name, db_name, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a
    connection to the desired database; name of the table to be dropped.
    Output: Deletes the given table."""
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    cnx.commit()
    cursor.close()
    cnx.close()


def create_table(table_name, db_name, columns, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be created; list of columns to be added while creating the table.
    Output: Creates a table with the given inputs."""
    cnx = mysql.connector.connect(user=user_name, password=pwd, host=host_ip, database=db_name)
    cursor = cnx.cursor()

    statement = "CREATE TABLE " + table_name + " ("
    for c in columns:
        statement += "`" + c + "`" + " VARCHAR(255),"
    statement = statement[:-1] + ")"

    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()


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
