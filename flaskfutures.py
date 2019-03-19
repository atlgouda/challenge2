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
    return render_template('ES/ES.html', title='ES')


@app.route("/ES_returns")
def es_ret():
    return render_template('ES/ES_ret.html', title='ES Returns')


@app.route("/ES_price")
def es_price():
    return render_template('ES/ES_price.html', title='ES Price')


@app.route("/ES_ann_vol")
def es_ann_vol():
    return render_template('ES/ES_ann_vol.html', title='ES Annual Volatilitry')


@app.route("/ES_tr_1yr_vol")
def es_tr_1yr_vol():
    return render_template('ES/ES_tr_1yr_vol.html', title='ES Trailing 1 Year Volatility')


@app.route("/ES_largest_daily_return")
def es_largest_daily_return():
    return render_template('ES/ES_largest_daily_return.html', title='ES Largest Daily Return')


@app.route("/ES_largest_ann_return")
def es_largest_ann_return():
    return render_template('ES/ES_largest_ann_return.html', title='ES Largest Annual Return')


@app.route("/CL")
def cl():
    return render_template('CL/CL.html', title='CL')


@app.route("/CL_returns")
def cl_ret():
    return render_template('CL/CL_ret.html', title='CL Returns')


@app.route("/CL_price")
def cl_price():
    return render_template('CL/CL_price.html', title='CL Price')


@app.route("/CL_ann_vol")
def cl_ann_vol():
    return render_template('CL/CL_ann_vol.html', title='CL Annual Volatilitry')


@app.route("/CL_tr_1yr_vol")
def cl_tr_1yr_vol():
    return render_template('CL/CL_tr_1yr_vol.html', title='CL Trailing 1 Year Volatility')


@app.route("/CL_largest_daily_return")
def cl_largest_daily_return():
    return render_template('CL/CL_largest_daily_return.html', title='CL Largest Daily Return')


@app.route("/CL_largest_ann_return")
def cl_largest_ann_return():
    return render_template('CL/CL_largest_ann_return.html', title='CL Largest Annual Return')


@app.route("/NQ")
def nq():
    return render_template('NQ/NQ.html', title='NQ')


@app.route("/NQ_returns")
def nq_ret():
    return render_template('NQ/NQ_ret.html', title='NQ Returns')


@app.route("/NQ_price")
def nq_price():
    return render_template('NQ/NQ_price.html', title='NQ Price')


@app.route("/NQ_ann_vol")
def nq_ann_vol():
    return render_template('NQ/NQ_ann_vol.html', title='NQ Annual Volatilitry')


@app.route("/NQ_tr_1yr_vol")
def nq_tr_1yr_vol():
    return render_template('NQ/NQ_tr_1yr_vol.html', title='NQ Trailing 1 Year Volatility')


@app.route("/NQ_largest_daily_return")
def nq_largest_daily_return():
    return render_template('NQ/NQ_largest_daily_return.html', title='NQ Largest Daily Return')


@app.route("/NQ_largest_ann_return")
def nq_largest_ann_return():
    return render_template('NQ/NQ_largest_ann_return.html', title='NQ Largest Annual Return')


@app.route("/NG")
def ng():
    return render_template('NG/NG.html', title='NG')


@app.route("/NG_returns")
def ng_ret():
    return render_template('NG/NG_ret.html', title='NG Returns')


@app.route("/NG_price")
def ng_price():
    return render_template('NG/NG_price.html', title='NG Price')


@app.route("/NG_ann_vol")
def ng_ann_vol():
    return render_template('NG/NG_ann_vol.html', title='NG Annual Volatilitry')


@app.route("/NG_tr_1yr_vol")
def ng_tr_1yr_vol():
    return render_template('NG/NG_tr_1yr_vol.html', title='NG Trailing 1 Year Volatility')


@app.route("/NG_largest_daily_return")
def ng_largest_daily_return():
    return render_template('NG/NG_largest_daily_return.html', title='NG Largest Daily Return')


@app.route("/NG_largest_ann_return")
def ng_largest_ann_return():
    return render_template('NG/NG_largest_ann_return.html', title='NG Largest Annual Return')


@app.route("/GC")
def gc():
    return render_template('GC/GC.html', title='GC')


@app.route("/GC_returns")
def gc_ret():
    return render_template('GC/GC_ret.html', title='GC Returns')


@app.route("/GC_price")
def gc_price():
    return render_template('GC/GC_price.html', title='GC Price')


@app.route("/GC_ann_vol")
def gc_ann_vol():
    return render_template('GC/GC_ann_vol.html', title='GC Annual Volatilitry')


@app.route("/GC_tr_1yr_vol")
def gc_tr_1yr_vol():
    return render_template('GC/GC_tr_1yr_vol.html', title='GC Trailing 1 Year Volatility')


@app.route("/GC_largest_daily_return")
def gc_largest_daily_return():
    return render_template('GC/GC_largest_daily_return.html', title='GC Largest Daily Return')


@app.route("/GC_largest_ann_return")
def gc_largest_ann_return():
    return render_template('GC/GC_largest_ann_return.html', title='GC Largest Annual Return')


if __name__ == '__main__':
    app.run(debug=True)
