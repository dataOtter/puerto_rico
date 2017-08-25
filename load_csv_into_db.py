import create_edit_tables as t
import mysql.connector


def load_one_table(csv_path, tbl_name, db_name, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be used; file path of csv file to be used.
    Output: Inserts the data from the given csv into the given table."""
    keys = t.get_keys_from_db(db_name, user_name, pwd, host_ip, tbl_name)
    column_positions_dict = t.add_columns(csv_path, tbl_name, db_name, keys, user_name, pwd, host_ip)
    t.insert_data(csv_path, db_name, column_positions_dict, user_name, pwd, host_ip, tbl_name)


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
