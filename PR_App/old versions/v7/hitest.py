from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('testhi.html')


@app.route("/echo", methods=['POST'])
def echo():
    return render_template('faceted_search.html')


if __name__ == "__main__":
    app.run()