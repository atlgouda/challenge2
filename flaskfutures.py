from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import dash
import no_callbacks
from werkzeug.wsgi import DispatcherMiddleware

dash_app = dash.Dash(__name__)
flask_app = Flask(__name__)
bootstrap = Bootstrap(flask_app)

application = DispatcherMiddleware(flask_app, {'/dashgraph': dash_app.server})
# it seems like DispatcherMiddleware is being used to "bind routes from other servers onto the "flask_app"
# so , you need to bind the routs in key-value dict, and then look and see in tutorial how application is used


@flask_app.route("/")
@flask_app.route("/home")
def home():
    return render_template('home.html', title='Home')


@flask_app.route("/dashgraph")
def dashgraph():
    return render_template('dash/dash.html', dash_chart=no_callbacks.show_graphs())


@flask_app.route("/dashboard/<futures_code>/")
def chart_series(futures_code):
    return render_template(futures_code + str("/") + futures_code + str(".html"))


@flask_app.route("/charts/<futures_code>/")
def all_charts(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_all_charts.html"))


@flask_app.route("/price/<futures_code>/")
def chart_price(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_price.html"))


@flask_app.route("/returns/<futures_code>/")
def chart_returns(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_ret.html"))


@flask_app.route("/ann_vol/<futures_code>/")
def chart_ann_vol(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_ann_vol.html"))


@flask_app.route("/tr_1yr_vol/<futures_code>/")
def chart_tr_1yr_vol(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_tr_1yr_vol.html"))


@flask_app.route("/largest_daily_return/<futures_code>/")
def chart_largest_daily_return(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_largest_daily_return.html"))


@flask_app.route("/largest_ann_return/<futures_code>/")
def chart_largest_ann_return(futures_code):
    return render_template(futures_code + str("/") + futures_code + str("_largest_ann_return.html"))


if __name__ == '__main__':
    flask_app.run(debug=True)
    dash_app.run(debug=True)
