import flask as f
from faceted_search import faceted_search_filter_instances as pidf
import json as j

app = f.Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


@app.route("/")
def main():
    return f.render_template('temp_index.html', result='this is main', fltrs=[])


@app.route("/show_results", methods=["POST"])
def show_result():
    fs = pidf.FilterSystem()
    to_apply = []
    '''gender, age = f.request.form['gender'], f.request.form['age']
    mindrugs, maxdrugs = f.request.form['mindrugs'], f.request.form['maxdrugs']

    if gender != 'ALL':
        to_apply.append("Gender " + gender)

    if age != 'ALL':
        to_apply.append("Age " + age)

    if mindrugs != 'ALL':
        to_apply.append("MinDrugUse " + mindrugs)

    if maxdrugs != 'ALL':
        to_apply.append("MaxDrugUse " + maxdrugs)

    for fltr in fs.get_inactive_filters():
        if fltr.get_kind_and_cat() in to_apply:
            fs.add_filter(fltr)

    result = len(fs.get_result_pids())'''

    #wordlist = j.loads(f.request.args.get('wordlist'))
    #print(wordlist)

    return f.render_template("temp_index.html", result='this is show', fltrs=to_apply)


@app.route("/testingJSON", methods=["POST"])
def testingJSON():
    data = f.request.json
    print("this is it!")
    print(data, type(data))
    for key, value in data.items():
        print(key, value)
    return f.render_template('temp_index.html', result='this is testing json', fltrs=[])
    # no, result will have to be sent to html back through ajax - I think...


if __name__ == "__main__":
    app.run()
