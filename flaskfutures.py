from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/futures")
def futures():
    return render_template('futures.html', title='Futures')


@app.route("/ES")
def es():
    return render_template('ES.html', title='ES')


@app.route("/CL_price")
def cl_price():
    return render_template('CL_price.html', title='CL Price')


if __name__ == '__main__':
    app.run(debug=True)
