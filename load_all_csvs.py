import load_csv_into_db as c
import prepare_subjects_pids as prep_0
import prepare_all_p1_csvs as prep_p1
import prepare_all_p2_csvs as prep_p2

all_csvs_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"

csvs = ['subjects_pids',
        'p1_screenings', 'p1_hivs', 'p1_hcvs', 'p1_interviews', 'p1_followups',
        'p2_network_interviews', 'p2_first_interviews', 'p2_second_interviews', 'p2_hivs', 'p2_hcvs',
        'p1_p2_overlap',
        ]  # = tables
#tables = c.get_table_names(db_name, user_name, pwd, host_ip)

db_name, user_name, pwd, host_ip = 'puerto_rico', 'root', 'password', '192.168.4.30'


prep_0.create_sub_pid_csv(all_csvs_path)
prep_p1.prep_all_p1(all_csvs_path)
prep_p2.


for csv in csvs:
    csv_path = all_csvs_path + csv + '.csv'
    c.load_one_table(csv_path, csv, db_name, user_name, pwd, host_ip)