"""REST service connecting to the PR database as well as the UI through Jquery"""
import flask as f
from faceted_search import faceted_search_filter_instances as pidf
from csv_writer import write_to_csv as csv_zip

app = f.Flask(__name__)
app.secret_key = "It's secret, duh"
#fs = pidf.FilterSystem()


@app.route("/")
def main():
    """Returns the initial html page"""
    if 'fs' not in f.session:
        fs = pidf.FilterSystem()
        f.session['fs'] = fs
    return f.render_template('faceted_search.html')


@app.route("/show_init_filters", methods=["POST"])
def show_init_filters():
    """Returns a json dictionary of all filter options and number of resulting project IDs"""
    fs = f.session['fs']
    # filter kind to list of each category & number of project IDs
    return f.jsonify({"filter_options_dict": fs.get_add_filter_options_str_dict()})


@app.route("/generate_download_zip", methods=["POST"])
def generate_download_zip():
    """Generates a zip files containing a nodes.csv and edges.csv based on the current project IDs selection"""
    fs = f.session['fs']
    return f.jsonify({"zip_folder_name": csv_zip.make_zip_folder_of_nodes_and_edges(fs.get_result_pids())})


@app.route("/show_results", methods=["POST", "GET"])
def show_result():
    """Returns a json dictionary of: number of project IDs resulting from the applied filter(s);
    list of all currently active filter kinds; list of all currently active filters as a kind and category string;
    list of all possible filter kinds; json dictionary of all filter options and number of resulting project IDs."""
    fs = f.session['fs']
    data = f.request.json  # get selected filters options as kind to category/'ALL'/'ASIS' dictionary
    to_apply, to_remove, active_filter_kinds, rem_fltrs = [], [], [], []
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

    active_fltrs = {}
    for fltr in fs.get_active_filters():
        active_fltrs[fltr.get_kind()] = fltr.get_cat()

    return f.jsonify({"res_pids_count": len(fs.get_result_pids()),
                      "active_fltr_kinds": list(set(active_filter_kinds)),
                      "active_fltrs": active_fltrs,
                      #"all_fltr_kinds": all_fltr_kinds,
                      "filter_options_dict": fs.get_add_filter_options_str_dict()})


def get_all_fltr_kinds():
    """Returns a list of all possible filter kinds."""
    fs = f.session['fs']
    all_fltr_kinds = []
    for kind in fs.get_filters_dict():
        all_fltr_kinds.append(kind)
    return all_fltr_kinds


if __name__ == "__main__":
    app.run()
