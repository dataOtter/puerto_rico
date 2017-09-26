import flask as f

app = f.Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


@app.route("/")
def main():
    return f.render_template('main_page.html')


@app.route("/hi", methods=["POST"])
def show_hi():
    gender = f.request.form['gender']

    return gender

if __name__ == "__main__":
    app.run()
