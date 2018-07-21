import flask as f
from csv_writer import extractor_SQL_queries as q
from csv_writer import write_to_csv as csv_zip

app = f.Flask(__name__)


@app.route("/")
def main():
    """Returns the initial html page"""
    return f.render_template('extractor.html')


@app.route("/send_available_cols", methods=["POST"])
def send_cols():
    cols = q.get_phase_dict_of_tbl_dicts_of_col_lists()
    #print(cols)
    return f.jsonify({"result": cols})


@app.route("/receive_selected_cols", methods=["POST"])
def receive_cols():
    data = f.request.json
    '''for phase in data:
        print('\n' + phase)
        for table in data[phase]:
            print('\n' + table)
            print(data[phase][table])'''
    return f.jsonify({"zip_folder_name": csv_zip.make_zip_folder(data)})


@app.route("/takeinput", methods=["GET", "POST"])
def takeinput():
    data = f.request.json
    print(data)
    return f.jsonify({"result": data})


if __name__ == "__main__":
    app.run()
