"""REST service connecting to the PR database as well as the UI through Jquery"""
import flask as f
from faceted_search import faceted_search_filter_instances as pidf
from csv_writer import extractor_SQL_queries as q
from csv_writer import write_to_csv as csv_zip

import pickle

app = f.Flask(__name__)
app.secret_key = "It's secret, duh"


@app.route("/")
def main():
    """Returns the initial html page"""
    fs = pidf.FilterSystem()
    try:
        f.session['fs'] = pickle.dumps(fs)
    except Exception as e:
        print(e)

    return f.render_template('faceted_search.html')


@app.route("/show_init_filters", methods=["POST"])
def show_init_filters():
    """Returns a json dictionary of all filter options and number of resulting project IDs"""
    fs = pickle.loads(f.session['fs'])
    # filter kind to list of each category & number of project IDs
    return f.jsonify({"filter_options_dict": fs.get_add_filter_options_str_dict(),
                      "total_participants": len(fs.get_result_pids())})


@app.route("/show_results", methods=["POST", "GET"])
def show_result():
    """Returns a json dictionary of: number of project IDs resulting from the applied filter(s);
    list of all currently active filter kinds; list of all currently active filters as a kind and category string;
    list of all possible filter kinds; json dictionary of all filter options and number of resulting project IDs."""
    fs = pickle.loads(f.session['fs'])
    data = f.request.json  # get selected filters options as kind to category/'ALL'/'ASIS' dictionary
    to_apply, to_remove, active_filter_kinds, rem_fltrs = [], [], [], []
    active_fltrs = {}
    all_fltr_kinds = get_all_fltr_kinds()

    for kind in all_fltr_kinds:
        cat = data[kind]
        if cat == 'ALL':
            to_remove.append(kind)  # add kind to the "remove all filter categories of this kind" list
        elif cat == "ASIS":
            active_filter_kinds.append(kind)
        else:  # add kind and category to the "apply this particular filter" list
            to_apply.append(kind + ' ' + cat)

    for fltr in fs.get_inactive_filters():  # loop through all currently inactive filters
        if fltr.get_kind_and_cat() in to_apply:  # if the filter is in the to_apply list
            fs.add_filter(fltr)  # apply this filter
            active_filter_kinds.append(fltr.get_kind())  # add to list of all active filter kinds

    for fltr in fs.get_active_filters():  # loop through all currently active filters
        if fltr.get_kind() in to_remove:  # if the filter's kind is in the remove filter kinds list
            rem_fltrs.append(fltr)  # add this particular filter to a list to remove later

    for fltr in rem_fltrs:  # loop through all filters to be removed
        fs.remove_filter(fltr)  # remove each filter

    f.session['fs'] = pickle.dumps(fs)

    for fltr in fs.get_active_filters():
        kind = fltr.get_kind()
        if kind in active_fltrs:
            active_fltrs[kind].append(fltr.get_cat())
        else:
            active_fltrs[kind] = [fltr.get_cat()]

    return f.jsonify({"res_pids_count": len(fs.get_result_pids()),
                      "active_fltr_kinds": list(set(active_filter_kinds)),
                      "active_fltrs": active_fltrs,
                      "all_fltr_kinds": all_fltr_kinds,
                      "filter_options_dict": fs.get_add_filter_options_str_dict()})


def get_all_fltr_kinds():
    """Returns a list of all possible filter kinds."""
    fs = pickle.loads(f.session['fs'])
    all_fltr_kinds = []
    for kind in fs.get_filters_dict():
        all_fltr_kinds.append(kind)
    return all_fltr_kinds


###############################################################################
#extractor
###############################################################################
@app.route("/send_to_extractor", methods=["GET"])
def send_pids_to_extractor():
    """"""
    return f.render_template('testhi.html')


@app.route("/send_available_cols", methods=["POST"])
def send_cols():
    # send these to the the extractor to show only columns that match these
    # for now, still show all columns
    cols = q.get_phase_dict_of_tbl_dicts_of_col_lists()
    #print(cols)
    return f.jsonify({"result": cols})


@app.route("/receive_selected_cols", methods=["POST"])
def receive_cols():
    data = f.request.json
    fs = pickle.loads(f.session['fs'])
    pids_list = fs.get_result_pids()
    return f.jsonify({"zip_folder_name": csv_zip.make_zip_folder(data, pids_list)})


@app.route("/takeinput", methods=["GET", "POST"])
def takeinput():
    data = f.request.json
    print(data)
    return f.jsonify({"result": data})
# extractor

if __name__ == "__main__":
    app.run(debug=True)
