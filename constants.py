DB_NAME = 'puerto_rico'
USER_NAME = 'root'
PASSWORD = 'password'
HOST_IP = '192.168.4.30'

ALL_CSVS_PATH = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"
CREATE_DB_SQL_FILE_PATH = \
    "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\puerto_rico\\SQL\\for_python_create_sql_db.sql"

CSV_NULL_VALUES = '#NULL!'

LOGGING_SQL_STATEMENT = False
LOGGING_SQL_INSERT_STATEMENT = False

#######################################################################################################################
# MEMOIZING
#######################################################################################################################
MEMOIZE = True  # if turning on again, be sure to call clear table function in memoize!
MEMOIZING_TABLE_NAME = 'top_secret_highly_confidential_cheat_sheet'
MEMOIZING_TABLE_COLUMN_LABELS = ['filters', 'pids', 'hash_index']
MEMOIZING_HASH_COLUMN_LABEL = MEMOIZING_TABLE_COLUMN_LABELS[2]
#######################################################################################################################
# MEMOIZING
#######################################################################################################################

#######################################################################################################################
# FILE NAMES AND FILE PATHS FOR CSVS AND MAIN DB TABLES
#######################################################################################################################
OLD_NODES_FILE = "node_index_9_30_17"
OLD_NODES_PATH = ALL_CSVS_PATH + OLD_NODES_FILE + ".csv"

OLD_EDGES_FILE = 'edge_index_9_30_17'
OLD_EDGES_PATH = ALL_CSVS_PATH + OLD_EDGES_FILE + ".csv"

SUBJECTS_IDS_FILE = 'subjects_ids'
SUBJECTS_IDS_PATH = ALL_CSVS_PATH + SUBJECTS_IDS_FILE + ".csv"

P1_SCREENINGS_FILE = 'p1_screenings'
P1_SCREENINGS_PATH = ALL_CSVS_PATH + P1_SCREENINGS_FILE + ".csv"

P1_HIVS_FILE = 'p1_hivs'
P1_HIVS_PATH = ALL_CSVS_PATH + P1_HIVS_FILE + ".csv"

P1_HCVS_FILE = 'p1_hcvs'
P1_HCVS_PATH = ALL_CSVS_PATH + P1_HCVS_FILE + ".csv"

P1_INTERVIEWS_FILE = 'p1_interviews'
P1_INTERVIEWS_PATH = ALL_CSVS_PATH + P1_INTERVIEWS_FILE + ".csv"

P1_FOLLOW_UPS_FILE = 'p1_followups'
P1_FOLLOW_UPS_PATH = ALL_CSVS_PATH + P1_FOLLOW_UPS_FILE + ".csv"

P2_NETWORK_INTERVIEWS_FILE = 'p2_network_interviews'
P2_NETWORK_INTERVIEWS_PATH = ALL_CSVS_PATH + P2_NETWORK_INTERVIEWS_FILE + ".csv"

P2_FIRST_INTERVIEWS_FILE = 'p2_first_interviews'
P2_FIRST_INTERVIEWS_PATH = ALL_CSVS_PATH + P2_FIRST_INTERVIEWS_FILE + ".csv"

P2_SECOND_INTERVIEWS_FILE = 'p2_second_interviews'
P2_SECOND_INTERVIEWS_PATH = ALL_CSVS_PATH + P2_SECOND_INTERVIEWS_FILE + ".csv"

P2_HIVS_FILE = 'p2_hivs'
P2_HIVS_PATH = ALL_CSVS_PATH + P2_HIVS_FILE + ".csv"

P2_HCVS_FILE = 'p2_hcvs'
P2_HCVS_PATH = ALL_CSVS_PATH + P2_HCVS_FILE + ".csv"

P1_P2_OVERLAPS_FILE = 'p1_p2_overlaps'
P1_P2_OVERLAPS_PATH = ALL_CSVS_PATH + P1_P2_OVERLAPS_FILE + ".csv"

EDGES_FILE = 'all_edges_index'
EDGES_PATH = ALL_CSVS_PATH + EDGES_FILE + ".csv"

NETWORK_EDGES_FILE = 'network_edges'
NETWORK_EDGES_PATH = ALL_CSVS_PATH + NETWORK_EDGES_FILE + ".csv"

RDS_EDGES_FILE = 'rds_edges'
RDS_EDGES_PATH = ALL_CSVS_PATH + RDS_EDGES_FILE + ".csv"

NOTES_FILE = 'all_notes_index'
NOTES_PATH = ALL_CSVS_PATH + NOTES_FILE + ".csv"

NOTE_EDGES_FILE = 'edges_to_notes'
NOTE_EDGES_PATH = ALL_CSVS_PATH + NOTE_EDGES_FILE + ".csv"

ALL_CSV = [SUBJECTS_IDS_FILE,
            P1_SCREENINGS_FILE, P1_HIVS_FILE, P1_HCVS_FILE, P1_INTERVIEWS_FILE, P1_FOLLOW_UPS_FILE,
            P2_NETWORK_INTERVIEWS_FILE, P2_FIRST_INTERVIEWS_FILE, P2_SECOND_INTERVIEWS_FILE, P2_HIVS_FILE, P2_HCVS_FILE,
            P1_P2_OVERLAPS_FILE,
            EDGES_FILE, NETWORK_EDGES_FILE, RDS_EDGES_FILE,
            NOTES_FILE, NOTE_EDGES_FILE]
#######################################################################################################################
# FILE NAMES AND FILE PATHS
#######################################################################################################################

#######################################################################################################################
# OLD AND NEW (COLUMN) LABELS FOR CSVS AND MAIN DB TABLES
#######################################################################################################################
LABEL_PID = "project_id"
LABEL_UNIQUE_ID = "unique_id"
LABEL_RDS_ID = "rds_id"

OLD_LABEL_RDS_ID = 'COUPONID'
OLD_LABEL_PID = 'Project IDs'  # in node_index_9_30_17.csv

LABEL_SENDER_PID = "sender_pid"
LABEL_RECEIVER_PID = "receiver_pid"
LABEL_SENDER_RECEIVER = "sender_receiver"

OLD_LABEL_SENDER_ID = 'Sender ID'
OLD_LABEL_RECEIVER_ID = 'Receiver ID'

OLD_LABEL_NET = 'Net Supplement'  # Column that says whether or not the edge came from the network supplement
OLD_LABEL_RDS = 'RDS Edge'  # Column that says whether or not the edge came from a rds/coupon referral
OLD_LABEL_CNX = 'Connection Notes'  # Column that has name of relevant connection note(s), if any
OLD_LABEL_FN = 'Field Notes'  # Column that has name of relevant field note(s), if any

NO_ENTRIES = ['', 'NA']  # All possible entries indicating "no note"

LABEL_EDGE_ID = "edge_id"
LABEL_NOTE_ID = "note_id"
LABEL_NOTE_EDGE_ID = "note_edge_id"
LABEL_NOTE_NAME = "note_name"
LABEL_NOTE_TYPE = "note_type"
TYPE_CNX_NOTE = "Connection note"
TYPE_FN = "Field note"
#######################################################################################################################
# OLD AND NEW COLUMN LABELS
#######################################################################################################################

NETWORK_HCV_HIV_COLS_TO_MERGE = ['P2FLFN', 'P2FLBM', 'P2BD', 'P2FLMN', 'P2FLSN', 'P2EDAD']
INTERVIEWS1_COLS_TO_MERGE = ['P2FIFLFN', 'P2FIFLBM', 'P2FIBD', 'P2FIFLMN', 'P2FIFLSN', 'P2FIEDAD']
INTERVIEWS2_COLS_TO_MERGE = ['P2SIFLFN', 'P2SIFLBM', 'P2SIBD', 'P2SIFLMN', 'P2SIFLSN', 'P2SIEDAD']