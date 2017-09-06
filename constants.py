DB_NAME = 'puerto_rico'
USER_NAME = 'root'
PASSWORD = 'password'
HOST_IP = '192.168.4.30'

ALL_CSVS_PATH = "C:\\Users\\Maisha\\Dropbox\\MB_dev\\Puerto Rico\\csv_data\\"

CSV_NULL_VALUES = '#NULL!'

LOGGING_SQL_STATEMENT = False
LOGGING_SQL_INSERT_STATEMENT = False

#######################################################################################################################
# FILE NAMES AND FILE PATHS
#######################################################################################################################
OLD_NODES_FILE = "node_index_5_3_17"
OLD_NODES_PATH = ALL_CSVS_PATH + OLD_NODES_FILE + ".csv"

OLD_EDGES_FILE = ''
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

EDGES_FILE = 'edges'
EDGES_PATH = ALL_CSVS_PATH + EDGES_FILE + ".csv"

NETWORK_EDGES_FILE = 'network_edges'
NETWORK_EDGES_PATH = ALL_CSVS_PATH + NETWORK_EDGES_FILE + ".csv"

RDS_EDGES_FILE = 'rds_edges'
RDS_EDGES_PATH = ALL_CSVS_PATH + RDS_EDGES_FILE + ".csv"

NOTES_FILE = 'notes'
NOTES_PATH = ALL_CSVS_PATH + NOTES_FILE + ".csv"

NOTE_EDGES_FILE = 'note_edges'
NOTE_EDGES_PATH = ALL_CSVS_PATH + NOTE_EDGES_FILE + ".csv"
#######################################################################################################################
# FILE NAMES AND FILE PATHS
#######################################################################################################################

#######################################################################################################################
# OLD AND NEW (COLUMN) LABELS
#######################################################################################################################
LABEL_PID = "project_id"
LABEL_UNIQUE_ID = "unique_id"
LABEL_RDS_ID = "rds_id"

OLD_LABEL_RDS_ID = 'COUPONID'

LABEL_SENDER_PID = "sender_pid"
LABEL_RECEIVER_PID = "receiver_pid"
LABEL_SENDER_RECEIVER = "sender_receiver"

OLD_LABEL_SENDER_ID = 'Sender ID'
OLD_LABEL_RECEIVER_ID = 'Receiver ID'

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