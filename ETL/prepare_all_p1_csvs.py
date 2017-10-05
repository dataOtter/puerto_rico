"""Function to clean all phase 1 csv files."""
import constants as c
from ETL import wrangling_functions as w


def prep_all_p1():
    """Input: None.
    Output: Fixes all phase 1 files' column labels; adds a project_id column to p1_screenings."""
    replace_with = {c.OLD_LABEL_RDS_ID: c.LABEL_RDS_ID}
    path_screenings = c.P1_SCREENINGS_PATH
    path_hiv = c.P1_HIVS_PATH
    path_hcv = c.P1_HCVS_PATH
    path_interviews = c.P1_INTERVIEWS_PATH
    path_followups = c.P1_FOLLOW_UPS_PATH
    path_nodes = c.OLD_NODES_PATH

    w.fix_column_labels_csv(path_screenings, replace_with)
    w.fix_column_labels_csv(path_hiv, replace_with)
    w.fix_column_labels_csv(path_hcv, replace_with)
    w.fix_column_labels_csv(path_interviews, replace_with)
    w.fix_column_labels_csv(path_followups, replace_with)

    w.add_column_and_data_from_old_nodes_to_csv(path_screenings, path_nodes,
                                                add_col_name=c.LABEL_PID, reference_col_name=c.LABEL_RDS_ID)
