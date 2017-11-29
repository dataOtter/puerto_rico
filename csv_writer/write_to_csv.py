import csv
import constants as c
from ETL import wrangling_functions as w
import uuid
from filters import filter_SQL_queries as q
import os
import zipfile


def make_nodes_csv_from_input_pids(pids: list, filename):
    filepath = c.DOWNLOAD_FILES_PATH + filename
    w.create_csv_add_column_labels(filepath, ['project_id'])

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        for pid in pids:
            writer.writerow([pid])


def make_edges_csv_from_input_pids(pids: list, filename):
    filepath = c.DOWNLOAD_FILES_PATH + filename
    w.create_csv_add_column_labels(filepath, ['unique_sender_receiver_pairs'])

    edge_ids = q.get_full_edge_ids_for_pids_list(pids)
    unique_edge_ids = q.get_unique_sender_receiver_pairs(edge_ids)

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        for edge_id in unique_edge_ids:
            writer.writerow([edge_id])


def zip_up_files(ziphandle, filenames: list):
    for root, dirs, files in os.walk(c.DOWNLOAD_FILES_PATH):
        for file in files:
            if file in filenames:
                ziphandle.write(os.path.join(root, file), file)


def make_zip_folder():
    unique_name = uuid.uuid1()
    print(unique_name)
    filename_nodes = str(unique_name) + '_nodes.csv'
    filename_edges = str(unique_name) + '_edges.csv'
    make_nodes_csv_from_input_pids(
        ['2344', '21445', '12435', '8909656', '24324', '23434', '090-9', '234345', '23434', '78854'], filename_nodes)
    make_edges_csv_from_input_pids(["P1439", "P2015", "P1005", "P1175", "P1018", "P1134", "P2002"], filename_edges)

    zipf = zipfile.ZipFile(c.DOWNLOAD_FILES_PATH + str(unique_name) + '.zip', 'w')
    zip_up_files(zipf, [filename_nodes, filename_edges])
    zipf.close()


make_zip_folder()

