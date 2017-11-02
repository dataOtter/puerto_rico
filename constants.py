DB_NAME = 'puerto_rico'
USER_NAME = 'root'
PASSWORD = 'password'
HOST_IP = '192.168.0.27'

def concat_path(filename):
    return ALL_CSVS_PATH + filename + '.csv'

ALL_CSVS_PATH = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"
CREATE_DB_SQL_FILE_PATH = \
    "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\puerto_rico\\SQL\\python_readable_create_sql_db.sql"

CSV_NULL_VALUES = '#NULL!'

LOGGING_SQL_STATEMENT = False
LOGGING_SQL_INSERT_STATEMENT = False

SQL_FILTER_TEMP_TBL = 'temp'
SQL_FILTER_TEMP_COL = 'pid'

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
TEMP_FILE_PATH = concat_path("temp")

OLD_NODES_FILE = "node_index_9_30_17"
OLD_NODES_PATH = concat_path(OLD_NODES_FILE)

OLD_EDGES_FILE = 'edge_index_9_30_17'
OLD_EDGES_PATH = concat_path(OLD_EDGES_FILE)

SUBJECTS_IDS_FILE = 'subjects_ids'
SUBJECTS_IDS_PATH = concat_path(SUBJECTS_IDS_FILE)

P1_SCREENINGS_FILE = 'p1_screenings'
P1_SCREENINGS_PATH = concat_path(P1_SCREENINGS_FILE)

P1_HIVS_FILE = 'p1_hivs'
P1_HIVS_PATH = concat_path(P1_HIVS_FILE)

P1_HCVS_FILE = 'p1_hcvs'
P1_HCVS_PATH = concat_path(P1_HCVS_FILE)

P1_INTERVIEWS_FILE = 'p1_interviews'
P1_INTERVIEWS_PATH = concat_path(P1_INTERVIEWS_FILE)

P1_FOLLOW_UPS_FILE = 'p1_followups'
P1_FOLLOW_UPS_PATH = concat_path(P1_FOLLOW_UPS_FILE)

P2_DEPRECATED_NET_SUPS_FILE = 'p2_deprecated_net_sups'
P2_DEPRECATED_NET_SUPS_PATH = concat_path(P2_DEPRECATED_NET_SUPS_FILE)

P2_NETWORK_SUPPLEMENT_EDGES_FILE = 'p2_network_supplement_edges'
P2_NETWORK_SUPPLEMENT_EDGES_PATH = concat_path(P2_NETWORK_SUPPLEMENT_EDGES_FILE)

P2_NET_SUPS_EXTRACT_FILE = 'p2_net_sups_extract'
P2_NET_SUPS_EXTRACT_PATH = concat_path(P2_NET_SUPS_EXTRACT_FILE)

P2_FIRST_INTERVIEWS_FILE = 'p2_first_interviews'
P2_FIRST_INTERVIEWS_PATH = concat_path(P2_FIRST_INTERVIEWS_FILE)

P2_SECOND_INTERVIEWS_FILE = 'p2_second_interviews'
P2_SECOND_INTERVIEWS_PATH = concat_path(P2_SECOND_INTERVIEWS_FILE)

P2_HIVS_FILE = 'p2_hivs'
P2_HIVS_PATH = concat_path(P2_HIVS_FILE)

P2_HCVS_FILE = 'p2_hcvs'
P2_HCVS_PATH = concat_path(P2_HCVS_FILE)

P1_P2_OVERLAPS_FILE = 'p1_p2_overlaps'
P1_P2_OVERLAPS_PATH = concat_path(P1_P2_OVERLAPS_FILE)

ALL_EDGES_INDEX_FILE = 'all_edges_index'
ALL_EDGES_INDEX_PATH = concat_path(ALL_EDGES_INDEX_FILE)

NETWORK_EDGES_FILE = 'network_edges'
NETWORK_EDGES_PATH = concat_path(NETWORK_EDGES_FILE)

RDS_EDGES_FILE = 'rds_edges'
RDS_EDGES_PATH = concat_path(RDS_EDGES_FILE)

ALL_NOTES_INDEX_FILE = 'all_notes_index'
ALL_NOTES_INDEX_PATH = concat_path(ALL_NOTES_INDEX_FILE)

EDGES_TO_NOTES_FILE = 'edges_to_notes'
EDGES_TO_NOTES_PATH = concat_path(EDGES_TO_NOTES_FILE)

ALL_CSV = [SUBJECTS_IDS_FILE,
           ALL_EDGES_INDEX_FILE, NETWORK_EDGES_FILE, RDS_EDGES_FILE,
           ALL_NOTES_INDEX_FILE, EDGES_TO_NOTES_FILE,
           P1_SCREENINGS_FILE, P1_HIVS_FILE, P1_HCVS_FILE, P1_INTERVIEWS_FILE, P1_FOLLOW_UPS_FILE,
           P2_NETWORK_SUPPLEMENT_EDGES_FILE, P2_NET_SUPS_EXTRACT_FILE,
           P2_FIRST_INTERVIEWS_FILE, P2_SECOND_INTERVIEWS_FILE, P2_HIVS_FILE, P2_HCVS_FILE,
           P1_P2_OVERLAPS_FILE]
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
LABEL_SENDER_RECEIVER = "full_edge_id"

OLD_LABEL_SENDER_ID = 'Sender ID'
OLD_LABEL_RECEIVER_ID = 'Receiver ID'

LABEL_P2SF = 'P2SF'
LABEL_P2NS1 = 'P2NS1'

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