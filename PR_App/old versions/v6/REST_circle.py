import flask as f

app = f.Flask(__name__)


@app.route("/")
def main():
    """Returns the initial html page"""
    return f.render_template('circle.html')


@app.route("/show_num", methods=["POST"])
def show_num():
    return f.jsonify({"total": 350,
                      "selected": 230})

if __name__ == "__main__":
    app.run()
