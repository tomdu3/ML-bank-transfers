from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def transaction():

    if request.method == 'POST':
        is_fraudulent = False  # Set the default value to False
        print('ok!')
        # typeofaction = request.form.get('typeofaction')
        # etc
        # if result fraudolent
        is_fraudulent = True

        return render_template('index.html', is_fraudulent=is_fraudulent)

    # no warning message at the beginning
    return render_template('index.html', is_fraudulent=None)

if __name__ == '__main__':
    app.run(debug=True)