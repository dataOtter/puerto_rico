import flask as f
from faceted_search import faceted_search_filter_instances as pidf
import json as j

app = f.Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


@app.route("/")
def main():
    return f.render_template('index_v1.html', result='this is main', fltrs=[])


@app.route("/show_results", methods=["POST", "GET"])
def show_result():
    data = f.request.json
    fs = pidf.FilterSystem()
    to_apply = []

    if data['gender'] != 'ALL':
        to_apply.append("Gender " + data['gender'])

    if data['age'] != 'ALL':
        to_apply.append("Age " + data['age'])

    if data['mindrugs'] != 'ALL':
        to_apply.append("MinDrugUse " + data['mindrugs'])

    if data['maxdrugs'] != 'ALL':
        to_apply.append("MaxDrugUse " + data['maxdrugs'])

    for fltr in fs.get_inactive_filters():
        if fltr.get_kind_and_cat() in to_apply:
            fs.add_filter(fltr)

    result = len(fs.get_result_pids())

    print(result)

    fltr_dict = {"filters": to_apply, "results": result}

    return f.jsonify(fltr_dict)


if __name__ == "__main__":
    app.run()
