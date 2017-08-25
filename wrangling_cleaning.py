import csv
import os


def get_csv_as_list(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        csv_list = list(reader)
    return csv_list


def create_csv_add_column_labels(file_path, cols):
    os.remove(file_path)
    with open(file_path, "w", newline="\n") as f:  # create csv file
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(cols)   # add column row


def add_row_to_csv(file_path, row):
    with open(file_path, "a", newline="\n") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(row)


def clear_data_from_csv(file_path):
    f = open(file_path, "w+")
    f.close()

'''fp = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\test.csv"
col = ['a']
create_csv_add_column_labels(fp, col)
for i in range(1, 10):
    add_row_to_csv(fp, [str(i)])'''
