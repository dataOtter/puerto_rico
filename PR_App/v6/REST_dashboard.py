import flask as f
from filters import db_queries as q

app = f.Flask(__name__)


@app.route("/")
def main():
    """Returns the initial html page"""
    return f.render_template('dashboard.html')


@app.route("/get_data", methods=["POST"])
def get_data():
    data = q.get_db_city_agegroup()
    #print(data)

    return f.jsonify({"results": data})


if __name__ == "__main__":
    app.run()

# send over array of dict: [{State: "Puerto Rico"}, freq:{low:4786, mid:1319, high:249}},
# {State:'Dominican Republic', freq:{low:1101, mid:412, high:674}}]
