from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from joblib import load
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def transaction():

    model = load('models/model.joblib')

    if request.method == 'POST':
        is_fraudulent = False  # Set the default value to False
        typeofaction = 1 if request.form.get('typeofaction')=='Cash-In' else 2
        sourceid = int(request.form.get('sourceid'))
        destinationid = int(request.form.get('destinationid'))
        amountofmoney = int(request.form.get('amountofmoney'))
        date_str = request.form.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        date_str = date_obj.strftime('%Y%m%d')
        date_as_int = int(date_str)
        print(date_as_int)
        preds = model.predict([[
             typeofaction,
             sourceid,
             destinationid,
             amountofmoney,
             date_as_int
        ]])
        print([
             typeofaction,
             sourceid,
             destinationid,
             amountofmoney,
             date_as_int
        ])
        print(preds)
        is_fraudulent = 'fraud' == preds[0]

        return render_template('index.html', is_fraudulent=is_fraudulent)

    
    return render_template('index.html', is_fraudulent=None)

if __name__ == '__main__':
    app.run(debug=True)