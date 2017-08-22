import csv
import numpy
import mysql.connector


def add_columns(file_path, table_name, db_name, keys):
    reader = csv.reader(open(file_path, "r"),
                        delimiter=",")
    x = list(reader)
    columns = x[0]
    column_positions = {}

    statement = "ALTER TABLE " + table_name

    for i in range(len(columns)):
        c = columns[i]
        if c not in keys:
            statement += " ADD COLUMN `" + c + "` VARCHAR(255),"
        column_positions[c] = i
    #print(column_positions)

    statement = statement[:-1] + ";"
    #print(statement)

    cnx = mysql.connector.connect(user='root', password='password',
                                  host='192.168.4.30',
                                  database=db_name)
    cursor = cnx.cursor()
    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()

    return column_positions


def insert_data(file_path, db_name, column_positions):
    labels, values = '(', '('
    
    for label in column_positions:
        labels += "`" + label + "`" + ","
        values += "%s,"

    labels = labels[:-1] + ")"
    values = values[:-1] + ")"

    insert_row_statement = "INSERT INTO test_table " + labels + " VALUES " + values

    cnx = mysql.connector.connect(user='root', password='password',
                                  host='192.168.4.30',
                                  database=db_name)
    cursor = cnx.cursor()

    reader = csv.reader(open(file_path, "r"),
                        delimiter=",")
    x = list(reader)
    rows = x[1:]

    for row in rows:
        row_values = ()
        for label, index in column_positions.items():
            row_values += (row[index],)
        cursor.execute(insert_row_statement, row_values)
        cnx.commit()

    cursor.close()
    cnx.close()


def drop_table(table_name, db_name):
    cnx = mysql.connector.connect(user='root', password='password',
                                  host='192.168.4.30',
                                  database=db_name)
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE " + table_name)
    cnx.commit()
    cursor.close()
    cnx.close()


def create_table(table_name, db_name, columns):
    cnx = mysql.connector.connect(user='root', password='password',
                                  host='192.168.4.30',
                                  database=db_name)
    cursor = cnx.cursor()

    statement = "CREATE TABLE " + table_name + " ("
    for c in columns:
        statement += "`" + c + "`" + " VARCHAR(255),"
    statement = statement[:-1] + ")"

    cursor.execute(statement)
    cnx.commit()
    cursor.close()
    cnx.close()


fp = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\test_data\\p1\\screener.csv"
tbn = "test_table"
db = 'dev_test'
k = ['COUPID']

#drop_table(tbn, db)
#create_table(tbn, db, k)
#cp = add_columns(fp, tbn, db, k)
#print(cp)
cp = {'COUPID': 0, 'INTID': 1, 'DATE': 2, 'SEED': 3, 'EP1': 4, 'EP2': 5, 'IC1': 6, 'COG1': 7, 'CS1': 8, 'CS2': 9, 'CS3': 10, 'CS4': 11, 'CS5': 12, 'CS6': 13, 'CSScore': 14, 'EP3': 15, 'EP4': 16, 'EP5': 17, 'EP6': 18, 'EP6b': 19, 'EP6c': 20, 'EP6d': 21, 'EP6e': 22, 'EP6f': 23, 'EP6g': 24, 'IC2': 25, 'EP7': 26, 'EP8': 27, 'EP9': 28, 'IC3': 29, 'NOTES': 30}
insert_data(fp, db, cp)
