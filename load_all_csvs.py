import load_csv_into_db as c

all_csvs_path = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"
# get list of csv file names -- actually they are the same as the table names, where a csv exists
csvs = ['p1_screenings'] # = tables
#tables = c.get_table_names(db_name, user_name, pwd, host_ip)
#keys = ['rds_id', 'project_id']    now redundant, added function to get keys

db_name = 'puerto_rico'
user_name = 'root'
pwd = 'password'
host_ip = '192.168.4.30'

for csv in csvs:
    csv_path = all_csvs_path + csv + '.csv'
    c.load_one_table(csv_path, csv, db_name, user_name, pwd, host_ip)
