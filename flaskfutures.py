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


@app.route("/ES_returns")
def es_ret():
    return render_template('ES_ret.html', title='ES Returns')


@app.route("/ES_price")
def es_price():
    return render_template('ES_price.html', title='ES Price')


@app.route("/ES_ann_vol")
def es_ann_vol():
    return render_template('ES_ann_vol.html', title='ES Annual Volatilitry')


@app.route("/ES_tr_1yr_vol")
def es_tr_1yr_vol():
    return render_template('ES_tr_1yr_vol.html', title='ES Trailing 1 Year Volatility')


@app.route("/ES_largest_daily_return")
def es_largest_daily_return():
    return render_template('ES_largest_daily_return.html', title='ES Largest Daily Return')


@app.route("/ES_largest_ann_return")
def es_largest_ann_return():
    return render_template('ES_largest_ann_return.html', title='ES Largest Annual Return')


@app.route("/CL_price")
def cl_price():
    return render_template('CL_price.html', title='CL Price')


if __name__ == '__main__':
    app.run(debug=True)
