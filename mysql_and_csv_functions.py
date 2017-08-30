import wrangling_functions as w
import mysql_query_fuctions as q
import mysql.connector


def load_one_table(csv_path, tbl_name, db_name, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be used; file path of csv file to be used.
    Output: Inserts the data from the given csv into the given table."""
    keys = q.get_existing_column_labels_from_db_table(db_name, user_name, pwd, host_ip, tbl_name)
    column_positions_dict = add_columns_from_csv_to_db_table(csv_path, tbl_name, db_name, keys,
                                                               user_name, pwd, host_ip)
    insert_data_from_csv(csv_path, db_name, column_positions_dict, user_name, pwd, host_ip, tbl_name)


def add_columns_from_csv_to_db_table(full_path, table_name, db_name, keys, user_name, pwd, host_ip):
    """Input: Database name, username, password and host ip address to open a connection to the desired database;
    name of the table to be used; file path to the csv file to be used;
    list of primary and foreign keys already contained in the given table.
    Output: Adds the columns from the given csv file to the given table, skipping those that already exist.
    Returns a dictionary column_positions of column labels as keys and column indices in the csv as values."""
    csv_columns = w.get_first_row_of_csv_as_list(full_path)
    column_positions = w.get_col_label_to_col_index_in_csv_dict(csv_columns)

    if len(csv_columns) <= len(keys):
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
        q.execute_mysql_statement(db_name, user_name, pwd, host_ip, statement)

    return column_positions


def insert_data_from_csv(full_path, db_name, column_positions, user_name, pwd, host_ip, tbl_name):
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
