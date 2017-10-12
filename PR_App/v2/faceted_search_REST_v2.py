import flask as f
from faceted_search import faceted_search_filter_instances as pidf

app = f.Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
fs = pidf.FilterSystem()


@app.route("/")
def main():
    return f.render_template('index_v2.html', result='this is main', fltrs=[])


@app.route("/show_results", methods=["POST", "GET"])
def show_result():
    data = f.request.json
    to_apply = []
    to_remove = []
    print("incoming data:")
    print(data)

    if data['Gender'] == 'ALL':
        to_remove.append("Gender")
    elif data['Gender'] != "ASIS":
        to_apply.append("Gender " + data['Gender'])

    if data['Age'] == 'ALL':
        to_remove.append("Age")
    elif data['Age'] != 'ASIS':
        to_apply.append("Age " + data['Age'])

    if data['MinDrugUse'] == 'ALL':
        to_remove.append("MinDrugUse")
    elif data['MinDrugUse'] != 'ASIS':
        to_apply.append("MinDrugUse " + data['MinDrugUse'])

    if data['MaxDrugUse'] == 'ALL':
        to_remove.append("MaxDrugUse")
    elif data['MaxDrugUse'] != 'ASIS':
        to_apply.append("MaxDrugUse " + data['MaxDrugUse'])

    active_filter_kinds = []
    for fltr in fs.get_inactive_filters():
        if fltr.get_kind_and_cat() in to_apply:
            print("Applying filter: " + fltr.get_kind_and_cat())
            fs.add_filter(fltr)  # add all selected filters
            active_filter_kinds.append(fltr.get_kind())

    print("In to remove list:")
    print(to_remove)
    rem_fltrs = []
    for fltr in fs.get_active_filters():
        print("Active filter: " + fltr.get_kind_and_cat())
        if fltr.get_kind() in to_remove:
            print("Adding to remove filter list: " + fltr.get_kind_and_cat())
            rem_fltrs.append(fltr)

    for fltr in rem_fltrs:
        fs.remove_filter(fltr)  # remove all deselected filters

    aslist = fs.get_add_filter_options_list()  # update filter options and get current filter options as list of strings

    print("outgoing string list:")
    print(aslist)

    result = len(fs.get_result_pids())

    fltr_dict = {"filters": to_apply, "results": result, "testing": aslist, "fltr_kinds": list(set(active_filter_kinds))}

    return f.jsonify(fltr_dict)


if __name__ == "__main__":
    app.run()
