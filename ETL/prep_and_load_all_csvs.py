"""Execute all ETL operations, at the end populating the MySQL database."""
from ETL import prepare_subjects_ids as prep_0, \
    prepare_all_p1_csvs as prep_p1, \
    prepare_all_p2_csvs as prep_p2, \
    prepare_p1_p2_overlaps as prep_3, \
    prepare_all_edge_and_notes_csvs as prep_4, \
    mysql_and_csv_functions as sqlcsv
import constants as c

# may have to call w.get_and_remove_discrepancy_rows_and_indices_from_old_edges(old_edge_full_path, old_node_full_path)
# down the line, make function to copy all new incoming files into new directory


def prep_all_csvs():
    """Input: None.
    Output: Runs all cleaning and preparations functions for all incoming data."""
    prep_0.create_sub_ids_csv()
    prep_p1.prep_all_p1()
    prep_p2.prep_all_p2()
    prep_3.create_p1_p2_overlaps()
    prep_4.create_all_edge_and_note_csvs()


def load_all_csvs_into_db():
    """Input: None.
    Output: Populates the database with all csv data."""
    for csv in c.ALL_CSV:
        csv_path = c.ALL_CSVS_PATH + csv + '.csv'
        sqlcsv.load_one_table_from_csv_into_db(csv_path, csv)

prep_all_csvs()
load_all_csvs_into_db()
