from flask import Flask, render_template, request, flash, redirect, url_for
from json import dumps
from sql_data import AppAccess
from trees import Trees

# from datetime import datetime
# import time
# import atexit
# from Flask-APScheduler import APScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = "a secret key"

nod = AppAccess().nod()



def colors(q: int):
    hcolor = 16777215 // q
    if hcolor == 0:
        hcolor = 1
    return hcolor



@app.route('/')
def index():
    global nod
    largest = AppAccess().largest()
    mia = len(AppAccess().missing_numbers())
    found = AppAccess().found()
    return render_template('home.html', home='bold', largest_number=largest[0], largest_step=largest[1], number_of_day=nod[0], found=found, mia=mia, count=nod[1], next=nod[2], loop=nod[3])



@app.route('/trees', methods=['POST', 'GET'])
def trees():
    global nod

    x = AppAccess().max_step_count()
    selections = [i for i in range(3, x + 1)]

    if request.method == 'POST':
        highlighted_number = request.form.get('highlighted-number')
        options = request.form.get('options')
        loop = request.form.get('loop-options')
        steps = request.form.get('steps-number')

        if steps != None:
            src = Trees().steps(count=steps)

        else:
            if options == 'whole_tree':
                src = Trees().whole_tree(highlighted_number=highlighted_number, delete=True)
            if 'equal_tree' == options:
                src = Trees().equal_tree(highlighted_number=highlighted_number)
            if 'line_tree' == options:
                src = Trees().line_tree(highlighted_number=highlighted_number)

        return render_template('trees.html', trees='bold', src=src, selections=selections)

    src = Trees().whole_tree(highlighted_number=nod[0], delete=False)

    return render_template('trees.html', trees='bold', src=src, selections=selections)



@app.route('/charts', methods=['GET', 'POST'])
def charts():
    global nod

    if request.method == 'POST':

        number = request.form.get('graphlookup')
        if number == None or number == '':
            flash('You need to put in a number.')
            return redirect(url_for('charts'))
        if int(number) > int(nod[0]):
            flash('The number cannot be larger than our largest number in our database.')
            return redirect(url_for('charts'))

        data = AppAccess().line(number)
        data[int(number)]['color'] = "#116466"
        x_axis = [i+1 for i in range(data[int(number)]['count'])]

        return render_template('charts.html', charts='bold', lines=data, x_axis=dumps(x_axis), nod=nod[0])

    data = AppAccess().traceback()
    x = max([data[i]['count'] for i in data])
    x_axis = [i+1 for i in range(x)]
    colordiv = colors(len(data))
    c = 0
    for i in data:
        hcolor = hex(colordiv * c)[2:]
        if len(hcolor) < 6:
            color = '#' + ('0' * (6 - len(hcolor))) + str(hcolor)
        else:
            color = '#' + str(hcolor)

        data[i]['color'] = color
        c += 1

    return render_template('charts.html', charts='bold', lines=data, x_axis=dumps(x_axis), nod=nod[0])



@app.route('/missing_numbers')
def missing():
    largest = AppAccess().largest()
    numbers = AppAccess().missing_numbers()
    l = len(numbers)
    return render_template('missing.html', missing='bold', largest=largest[0], numbers=numbers, l=l)



@app.route('/number_details', methods=['GET', 'POST'])
def detail():

    if request.method == 'POST':
        number = request.form.get('number-details')
        deets = AppAccess().deets(number)
        x = len(deets['same_count'])
        return render_template('details.html', details='bold', deets=deets, x=x)

    return render_template('details.html', details='bold', deets=False)