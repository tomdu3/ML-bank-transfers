from flask import Flask, render_template, request, flash
import numpy as np
import pandas as pd
from joblib import load
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'my_secret_key'


@app.route('/', methods=['GET', 'POST'])
def transaction():

    model = load('models/model.joblib')

    if request.method == 'POST':
        is_fraudulent = False  # Set the default value to False
        invalid_input = False  
        typeofaction = request.form.get('typeofaction')
        sourceid = request.form.get('sourceid')
        destinationid = request.form.get('destinationid')
        amountofmoney = request.form.get('amountofmoney')

        if not sourceid.isdigit():
            flash('Invalid input for Source ID')
            invalid_input = True
        if not destinationid.isdigit():
            flash('Invalid input for Destination ID')
            invalid_input = True
        if not amountofmoney.isdigit():
            flash('Invalid input for Amount of Money')
            invalid_input = True


        if invalid_input:
            return render_template('index.html', is_fraudulent=None)

        date_str = request.form.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        date_str = date_obj.strftime('%Y%m%d')
        date_as_int = int(date_str)

        preds = model.predict([[
            1 if typeofaction == 'Cash-In' else 2,
            int(sourceid),
            int(destinationid),
            int(amountofmoney),
            date_as_int
        ]])

        is_fraudulent = 'fraud' == preds[0]

        return render_template('index.html', is_fraudulent=is_fraudulent)

    return render_template('index.html', is_fraudulent=None)


if __name__ == '__main__':
    app.run(debug=True)