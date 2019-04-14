from flask import Flask, render_template, Markup
from flask_bootstrap import Bootstrap
from analysis import chart_contracts_dynamic, chart_returns_dynamic, chart_daily_return_dynamic, chart_tr_1yr_dynamic, chart_ann_vol_dynamic, chart_annual_return_dynamic

flask_app = Flask(__name__)
bootstrap = Bootstrap(flask_app)


@flask_app.route("/")
@flask_app.route("/home")
def home():
    return render_template('home.html', title='Home')


@flask_app.route("/charts/<futures_code>/")
@flask_app.route("/dashboard/<futures_code>/")
def chart_series(futures_code):
    return render_template('charts_base.html', contract_family=futures_code,
                           chart=Markup(chart_contracts_dynamic(futures_code)),
                           chart_ret=Markup(chart_returns_dynamic(futures_code)),
                           chart_daily_ret=Markup(chart_daily_return_dynamic(futures_code)),
                           chart_tr_1yr=Markup(chart_tr_1yr_dynamic(futures_code)),
                           chart_ann_vol=Markup(chart_ann_vol_dynamic(futures_code)),
                           chart_annual_ret=Markup(chart_annual_return_dynamic(futures_code)),
                           )


@flask_app.route("/price/<futures_code>/")
def chart_price(futures_code):
    return render_template('price.html', contract_family=futures_code,
                           chart=Markup(chart_contracts_dynamic(futures_code)))


@flask_app.route("/returns/<futures_code>/")
def chart_returns(futures_code):
    return render_template('returns.html', contract_family=futures_code,
                           chart_ret=Markup(chart_contracts_dynamic(futures_code)))


@flask_app.route("/ann_vol/<futures_code>/")
def chart_ann_vol(futures_code):
    return render_template('ann_vol.html', contract_family=futures_code,
                           chart_ann_vol=Markup(chart_daily_return_dynamic(futures_code)),
                           )


@flask_app.route("/tr_1yr_vol/<futures_code>/")
def chart_tr_1yr_vol(futures_code):
    return render_template('tr_1yr.html', contract_family=futures_code,
                           chart_tr_1yr=Markup(chart_tr_1yr_dynamic(futures_code)),
                           )


@flask_app.route("/largest_daily_return/<futures_code>/")
def chart_largest_daily_return(futures_code):
    return render_template('daily.html', contract_family=futures_code,
                           chart_daily_ret=Markup(chart_daily_return_dynamic(futures_code)),
                           )


@flask_app.route("/largest_ann_return/<futures_code>/")
def chart_largest_ann_return(futures_code):
    return render_template('annual.html', contract_family=futures_code,
                           chart_annual_ret=Markup(chart_annual_return_dynamic(futures_code)),
                           )


if __name__ == '__main__':
    flask_app.run(debug=True)
    dash_app.run(debug=True)
