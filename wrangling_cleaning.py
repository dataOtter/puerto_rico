import csv


def get_csv_as_list(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        csv_list = list(reader)
    return csv_list


def create_csv_add_column_labels(file_path, cols):
    with open(file_path, "w") as f: # create subjects_pid.csv file
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(cols)  # add column row
