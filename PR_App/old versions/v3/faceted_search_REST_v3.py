import flask as f
from faceted_search import faceted_search_filter_instances as pidf

app = f.Flask(__name__)
app.secret_key = "It's secret, duh"
fs = pidf.FilterSystem()


@app.route("/")
def main():
    return f.render_template('index_v3.html')


@app.route("/show_init_filters", methods=["POST"])
def show_init_filters():
    # filter kind to list of each category & number of project IDs
    return f.jsonify({"filter_options_dict": fs.get_add_filter_options_str_dict()})


@app.route("/show_results", methods=["POST", "GET"])
def show_result():
    data = f.request.json  # get selected filters options as kind to category/'ALL'/'ASIS' dictionary
    to_apply, to_remove, active_filter_kinds, active_fltrs, rem_fltrs = [], [], [], [], []
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

    for fltr in fs.get_active_filters():
        active_fltrs.append(fltr.get_kind_and_cat())

    return f.jsonify({"res_pids_count": len(fs.get_result_pids()),
                      "active_fltr_kinds": list(set(active_filter_kinds)),
                      "active_fltrs": active_fltrs,
                      "all_fltr_kinds": all_fltr_kinds,
                      "filter_options_dict": fs.get_add_filter_options_str_dict()})


def get_all_fltr_kinds():
    all_fltr_kinds = []
    for kind in fs.get_filters_dict():
        all_fltr_kinds.append(kind)
    return all_fltr_kinds

if __name__ == "__main__":
    app.run()
