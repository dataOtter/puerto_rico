import csv
import numpy
import mysql.connector


def add_columns(file_path, table_name, db_name):

    reader = csv.reader(open(file_path, "r"),
                        delimiter=",")

    x = list(reader)
    columns = x[0]
    #row1 = x[1]
    #rows = x[1:]

    statement = "ALTER TABLE " + table_name

    for i in range(len(columns)):
        statement += " ADD COLUMN `" + columns[i] + "` VARCHAR(255),"

    statement = statement[:-1] + ";"

    #print(statement)

    #result = numpy.array(x).astype("float")

    cnx = mysql.connector.connect(user='root', password='password',
                                  host='192.168.4.30',
                                  database=db_name)

    cursor = cnx.cursor()

    cursor.execute(statement)

    row_no = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()


fp = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\PR_test_data\\p1\\testerrr.csv"
tbn = "test_table"
db = 'dev_test'

add_columns(fp, tbn, db)
