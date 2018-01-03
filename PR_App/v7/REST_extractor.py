import flask as f
from csv_writer import extractor_SQL_queries as q

app = f.Flask(__name__)


@app.route("/")
def main():
    """Returns the initial html page"""
    return f.render_template('extractor.html')


@app.route("/get_available_cols", methods=["POST"])
def get_cols():
    cols = q.get_phase_dict_of_tbl_dicts_of_col_lists()
    print(cols)

    return f.jsonify({"result": cols})


@app.route("/takeinput", methods=["GET", "POST"])
def takeinput():
    data = f.request.json
    print(data)
    return f.jsonify({"result": data})


if __name__ == "__main__":
    app.run()
