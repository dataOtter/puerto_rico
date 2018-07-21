"""Functions operating on CSVs as well as MySQL database - load csv data into database."""
import mysql.connector

import constants as c
import mysql_query_fuctions as q
from ETL import wrangling_functions as w


def load_one_table_from_csv_into_db(csv_path, tbl_name):
    """Input: Name of the table to be used; file path of csv file to be used.
    Output: Inserts the data from the given csv into the given table
    using the database details set in the constants file."""
    keys = q.get_existing_column_labels_from_db_table(tbl_name)
    column_positions_dict = add_columns_from_csv_to_db_table(csv_path, tbl_name, keys)
    insert_data_from_csv(csv_path, column_positions_dict, tbl_name)


def add_columns_from_csv_to_db_table(full_path, table_name, keys):
    """Input: Name of the table to be used; file path to the csv file to be used;
    list of primary and foreign keys already contained in the given table.
    Output: Adds the columns from the given csv file to the given table, skipping those that already exist,
    using the database details set in the constants file.
    Returns a dictionary column_positions of column labels as keys and column indices in the csv as values."""
    csv_columns = w.get_first_row_of_csv_as_list(full_path)
    column_positions = w.get_col_label_to_col_index_dict(csv_columns)

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
        q.execute_query(statement)

    return column_positions


def insert_data_from_csv(full_path, column_positions, tbl_name):
    """Input: Name of the table to be used; file path to the csv file to be used;
    dictionary of column_positions linking column labels to row indices in the csv.
    Output: Inserts the data contained in the given csv into the given table
    using the database details set in the constants file."""
    labels = []
    for label in column_positions:
        labels.append(label)

    insert_row_statement = q.get_insert_row_statement(tbl_name, labels)

    cnx = mysql.connector.connect(user=c.USER_NAME, password=c.PASSWORD, host=c.HOST_IP, database=c.DB_NAME)
    cursor = cnx.cursor()

    rows = w.get_csv_as_list(full_path)[1:]  # without column labels row

    for row in rows:
        row_values = ()
        for label, index in column_positions.items():
            if row[index] == c.CSV_NULL_VALUES:
                row_values += ('',)
            else:
                row_values += (row[index],)
        if c.LOGGING_SQL_INSERT_VALUES:
            print(row_values)
        if c.LOGGING_SQL_QUERIES:
            print(insert_row_statement, row_values)
        cursor.execute(insert_row_statement, row_values)
        cnx.commit()

    cursor.close()
    cnx.close()
