from flask import Flask, render_template, make_response, Markup
from flask_bootstrap import Bootstrap
import dash
import dash_html_components as html
import pricedash
from werkzeug.wsgi import DispatcherMiddleware


dash_app = dash.Dash(__name__)
flask_app = Flask(__name__)

application = DispatcherMiddleware(flask_app, {'/dash': dash_app.server})


bootstrap = Bootstrap(flask_app)


@flask_app.route("/")
@flask_app.route("/home")
def home():
    return render_template('home.html', title='Home')


@flask_app.route("/dashgraph")
def dashgraph():
    return render_template('dash/dash.html',
                           # dash_chart=pricedash.show_graphs()
                           )


@flask_app.route("/bootstrap_test")
def bootstrap_test():
    return render_template('bootstraptest.html')


@flask_app.route("/ES")
def es():
    return render_template('ES/ES.html', title='ES')


@flask_app.route("/ES_returns")
def es_ret():
    return render_template('ES/ES_ret.html', title='ES Returns')


@flask_app.route("/ES_price")
def es_price():
    return render_template('ES/ES_price.html', title='ES Price')


@flask_app.route("/ES_ann_vol")
def es_ann_vol():
    return render_template('ES/ES_ann_vol.html', title='ES Annual Volatilitry')


@flask_app.route("/ES_tr_1yr_vol")
def es_tr_1yr_vol():
    return render_template('ES/ES_tr_1yr_vol.html', title='ES Trailing 1 Year Volatility')


@flask_app.route("/ES_largest_daily_return")
def es_largest_daily_return():
    return render_template('ES/ES_largest_daily_return.html', title='ES Largest Daily Return')


@flask_app.route("/ES_largest_ann_return")
def es_largest_ann_return():
    return render_template('ES/ES_largest_ann_return.html', title='ES Largest Annual Return')


@flask_app.route("/CL")
def cl():
    return render_template('CL/CL.html', title='CL')


@flask_app.route("/CL_returns")
def cl_ret():
    return render_template('CL/CL_ret.html', title='CL Returns')


@flask_app.route("/CL_price")
def cl_price():
    return render_template('CL/CL_price.html', title='CL Price')


@flask_app.route("/CL_ann_vol")
def cl_ann_vol():
    return render_template('CL/CL_ann_vol.html', title='CL Annual Volatilitry')


@flask_app.route("/CL_tr_1yr_vol")
def cl_tr_1yr_vol():
    return render_template('CL/CL_tr_1yr_vol.html', title='CL Trailing 1 Year Volatility')


@flask_app.route("/CL_largest_daily_return")
def cl_largest_daily_return():
    return render_template('CL/CL_largest_daily_return.html', title='CL Largest Daily Return')


@flask_app.route("/CL_largest_ann_return")
def cl_largest_ann_return():
    return render_template('CL/CL_largest_ann_return.html', title='CL Largest Annual Return')


@flask_app.route("/NQ")
def nq():
    return render_template('NQ/NQ.html', title='NQ')


@flask_app.route("/NQ_returns")
def nq_ret():
    return render_template('NQ/NQ_ret.html', title='NQ Returns')


@flask_app.route("/NQ_price")
def nq_price():
    return render_template('NQ/NQ_price.html', title='NQ Price')


@flask_app.route("/NQ_ann_vol")
def nq_ann_vol():
    return render_template('NQ/NQ_ann_vol.html', title='NQ Annual Volatility')


@flask_app.route("/NQ_tr_1yr_vol")
def nq_tr_1yr_vol():
    return render_template('NQ/NQ_tr_1yr_vol.html', title='NQ Trailing 1 Year Volatility')


@flask_app.route("/NQ_largest_daily_return")
def nq_largest_daily_return():
    return render_template('NQ/NQ_largest_daily_return.html', title='NQ Largest Daily Return')


@flask_app.route("/NQ_largest_ann_return")
def nq_largest_ann_return():
    return render_template('NQ/NQ_largest_ann_return.html', title='NQ Largest Annual Return')


@flask_app.route("/NG")
def ng():
    return render_template('NG/NG.html', title='NG')


@flask_app.route("/NG_returns")
def ng_ret():
    return render_template('NG/NG_ret.html', title='NG Returns')


@flask_app.route("/NG_price")
def ng_price():
    return render_template('NG/NG_price.html', title='NG Price')


@flask_app.route("/NG_ann_vol")
def ng_ann_vol():
    return render_template('NG/NG_ann_vol.html', title='NG Annual Volatilitry')


@flask_app.route("/NG_tr_1yr_vol")
def ng_tr_1yr_vol():
    return render_template('NG/NG_tr_1yr_vol.html', title='NG Trailing 1 Year Volatility')


@flask_app.route("/NG_largest_daily_return")
def ng_largest_daily_return():
    return render_template('NG/NG_largest_daily_return.html', title='NG Largest Daily Return')


@flask_app.route("/NG_largest_ann_return")
def ng_largest_ann_return():
    return render_template('NG/NG_largest_ann_return.html', title='NG Largest Annual Return')


@flask_app.route("/GC")
def gc():
    return render_template('GC/GC.html', title='GC')


@flask_app.route("/GC_returns")
def gc_ret():
    return render_template('GC/GC_ret.html', title='GC Returns')


@flask_app.route("/GC_price")
def gc_price():
    return render_template('GC/GC_price.html', title='GC Price')


@flask_app.route("/GC_ann_vol")
def gc_ann_vol():
    return render_template('GC/GC_ann_vol.html', title='GC Annual Volatilitry')


@flask_app.route("/GC_tr_1yr_vol")
def gc_tr_1yr_vol():
    return render_template('GC/GC_tr_1yr_vol.html', title='GC Trailing 1 Year Volatility')


@flask_app.route("/GC_largest_daily_return")
def gc_largest_daily_return():
    return render_template('GC/GC_largest_daily_return.html', title='GC Largest Daily Return')


@flask_app.route("/GC_largest_ann_return")
def gc_largest_ann_return():
    return render_template('GC/GC_largest_ann_return.html', title='GC Largest Annual Return')


if __name__ == '__main__':
    flask_app.run(debug=True)
    dash_app.run(debug=True)
