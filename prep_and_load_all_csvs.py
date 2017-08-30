import load_csv_into_db as c
import prepare_subjects_pids as prep_0
import prepare_all_p1_csvs as prep_p1
import prepare_all_p2_csvs as prep_p2
import prepare_p1_p2_overlaps as prep_3
import prepare_all_edge_and_notes_csvs as prep_4

# in p2_network_interviews: row 81, column P2FLSN (segment of unique id), entry is 3 but should be R

all_csvs_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"

#prep_0.create_sub_pid_csv(all_csvs_path)
#prep_p1.prep_all_p1(all_csvs_path)
#prep_p2.prep_all_p2(all_csvs_path)
#prep_3.create_p1_p2_overlaps(all_csvs_path)
#prep_4.create_all_edge_csvs(all_csvs_path)

csvs = ['subjects_pids',
        'p1_screenings', 'p1_hivs', 'p1_hcvs', 'p1_interviews', 'p1_followups',
        'p2_network_interviews', 'p2_first_interviews', 'p2_second_interviews', 'p2_hivs', 'p2_hcvs',
        'p1_p2_overlap',
        'edges', 'network_edges', 'rds_edges',
        'notes', 'note_edges']  # = tables
#tables = c.get_table_names(db_name, user_name, pwd, host_ip)

db_name, user_name, pwd, host_ip = 'puerto_rico', 'root', 'password', '192.168.4.30'

csvs2 = ['subjects_pids',
        'p1_screenings', 'p1_hivs', 'p1_hcvs', 'p1_interviews', 'p1_followups',
        'p2_network_interviews', 'p2_first_interviews', 'p2_second_interviews',]

for csv in csvs2:
    csv_path = all_csvs_path + csv + '.csv'
    #c.load_one_table(csv_path, csv, db_name, user_name, pwd, host_ip)


csv = 'p2_hivs'
csv_path = all_csvs_path + csv + '.csv'
c.load_one_table(csv_path, csv, db_name, user_name, pwd, host_ip)
