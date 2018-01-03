"""Functions to write data from the SQL database to csv files and zip them up."""
import csv
import constants as c
from ETL import wrangling_functions as w
import uuid
from filters import filter_SQL_queries as fq
import os
import zipfile
from csv_writer import extractor_SQL_queries as eq


def make_csv(cols: list, filename: str):
    full_data = eq.get_all_tbl_data_by_cols(filename, cols)

    filepath = c.DOWNLOAD_FILES_PATH + str(uuid.uuid1()) + '__' + filename + '.csv'
    w.create_csv_add_column_labels(filepath, cols)

    print(full_data)

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        for row in full_data[1:]:
            writer.writerow(row)


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

    edge_ids = fq.get_full_edge_ids_for_pids_list(pids)
    unique_edge_ids = fq.get_unique_sender_receiver_pairs(edge_ids)

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        for edge_id in unique_edge_ids:
            writer.writerow([edge_id])


def zip_up_files(ziphandle, filenames: list):
    for root, dirs, files in os.walk(c.DOWNLOAD_FILES_PATH):
        for file in files:
            if file in filenames:
                ziphandle.write(os.path.join(root, file), file)


def make_zip_folder(pids_list: list):
    unique_name = uuid.uuid1()
    #print(unique_name)
    filename_nodes = str(unique_name) + '_nodes.csv'
    filename_edges = str(unique_name) + '_edges.csv'
    #make_nodes_csv_from_input_pids(
        #["P1439", "P2015", "P1005", "P1175", "P1018", "P1134", "P2002"], filename_nodes)
    #make_edges_csv_from_input_pids(["P1439", "P2015", "P1005", "P1175", "P1018", "P1134", "P2002"], filename_edges)
    make_nodes_csv_from_input_pids(pids_list, filename_nodes)
    make_edges_csv_from_input_pids(pids_list, filename_edges)

    zipf = zipfile.ZipFile(c.DOWNLOAD_FILES_PATH + str(unique_name) + '.zip', 'w')
    zip_up_files(zipf, [filename_nodes, filename_edges])
    zipf.close()

    return str(unique_name) + '.zip'


make_csv(['AgentId', 'Priority', 'LANG', 'SEED', 'DM4', 'FIN3', 'FIN3O'], 'p1_interviews')
