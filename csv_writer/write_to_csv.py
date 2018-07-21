"""Functions to write data from the SQL database to csv files and zip them up."""
import csv
import constants as c
from ETL import wrangling_functions as w
import uuid
from filters import filter_SQL_queries as fq
import os
import zipfile
from csv_writer import extractor_SQL_queries as eq


def make_zip_folder(phase_tbl_cols_dict: dict, pids_list):
    """Input: Dictionary of phase name to dictionary of table name to column label list.
    Output: Returns name of the zip folder containing all subjects data from the given columns of the given tables.
    File path set in constants."""
    '''
    # this version returns a csv for each database table
    for phase in phase_tbl_cols_dict:  # for each phase,
        # for each table and associated list of columns in that phase,
        for tbl, cols in phase_tbl_cols_dict[phase].items():
            temp_name = unique_id + '__' + phase + '__' + tbl + '.csv'  # make a csv file name for the table
            filenames.append(temp_name)  # keep track of the file name
            # make a csv file with the data associated with the given columns of the table
            full_data = eq.get_all_tbl_data_by_cols(tbl, cols)
            write_list_to_csv(temp_name, full_data)
            '''
    filenames = []
    unique_id = str(uuid.uuid1())

    full_data_nodes = eq.get_single_subjects_tbl_of_all_given_tbls_and_cols(phase_tbl_cols_dict, pids_list)
    file_name_nodes = unique_id + '__nodes_all_selected_data.csv'  # make a csv file name for the table
    write_list_to_csv(file_name_nodes, full_data_nodes)

    edges_list = fq.get_full_edge_ids_for_pids_list(pids_list)
    full_data_edges = eq.get_single_edges_tbl_of_all_given_tbls_and_cols(phase_tbl_cols_dict, edges_list)
    file_name_edges = unique_id + '__edges_all_selected_data.csv'  # make a csv file name for the table
    write_list_to_csv(file_name_edges, full_data_edges)

    filenames.append(file_name_edges)
    filenames.append(file_name_nodes)

    zipf = zipfile.ZipFile(c.DOWNLOAD_FILES_PATH + unique_id + '.zip', 'w')  # create zip-handle
    zip_up_files(zipf, filenames)  # zip up the files
    zipf.close()

    return unique_id + '.zip'  # return the name of the zip folder


def make_nodes_csv_from_input_pids(pids: list, filename):
    """Input: List of PIDs; full file name to use (without path).
    Output: Creates a CSV file containing the given PIDs."""
    pids = [c.LABEL_PID] + pids
    write_list_to_csv(filename, pids, is_list_of_lists=False)


def make_edges_csv_from_input_pids(pids: list, filename):
    """Input: List of PIDs; full file name to use (without path).
    Output: Creates CSV file containing the unique sender_receiver pairs that contain at least one of the given PIDs."""
    edge_ids = fq.get_full_edge_ids_for_pids_list(pids)
    unique_edge_ids = ['unique_sender_receiver_pairs'] + fq.get_unique_sender_receiver_pairs(edge_ids)
    write_list_to_csv(filename, unique_edge_ids, is_list_of_lists=False)


def zip_up_files(ziphandle, filenames: list):
    """Input: Ziphandle object; list of full file name (sub-)selection
    of those files contained in the constants file path to zip up.
    Output: Zips up the selection of files."""
    for root, dirs, files in os.walk(c.DOWNLOAD_FILES_PATH):
        for file in files:
            if file in filenames:
                ziphandle.write(os.path.join(root, file), file)


def make_zip_folder_of_nodes_and_edges(pids_list: list):
    unique_name = uuid.uuid1()
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


def write_list_to_csv(filename: str, data: list, is_list_of_lists=True):
    """Input: List of data to be written to a csv; filename; if data is lists of strings be sure to change the flag.
    File-path is set in constants.
    Output: Creates a csv of the given data, with each list being a row."""
    filepath = c.DOWNLOAD_FILES_PATH + filename
    w.create_empty_csv(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=",")
        for row in data:
            if is_list_of_lists:
                writer.writerow(row)
            else:
                writer.writerow([row])