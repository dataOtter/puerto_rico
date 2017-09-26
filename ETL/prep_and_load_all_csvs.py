from ETL import prepare_all_p1_csvs as prep_p1, prepare_all_p2_csvs as prep_p2, prepare_p1_p2_overlaps as prep_3, \
    prepare_all_edge_and_notes_csvs as prep_4, prepare_subjects_ids as prep_0, mysql_and_csv_functions as sqlcsv

all_csvs_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"

# may have to call w.get_and_remove_discrepancy_rows_and_indices_from_old_edges(old_edge_full_path, old_node_full_path)
# down the line, make function to copy all new incoming files into new directory

prep_0.create_sub_ids_csv()
prep_p1.prep_all_p1()
prep_p2.prep_all_p2()
prep_3.create_p1_p2_overlaps()
prep_4.create_all_edge_and_note_csvs()

csvs = ['subjects_ids',
        'p1_screenings', 'p1_hivs', 'p1_hcvs', 'p1_interviews', 'p1_followups',
        'p2_network_interviews', 'p2_first_interviews', 'p2_second_interviews', 'p2_hivs', 'p2_hcvs',
        'p1_p2_overlaps',
        'edges', 'network_edges', 'rds_edges',
        'notes', 'note_edges']

for csv in csvs:
    csv_path = all_csvs_path + csv + '.csv'
    sqlcsv.load_one_table(csv_path, csv)
