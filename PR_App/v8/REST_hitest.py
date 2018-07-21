from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('testhi.html')


@app.route("/echo", methods=['GET'])
def echo():
    print("here")
    return render_template('testhi2.html')


if __name__ == "__main__":
    app.run()