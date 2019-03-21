import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from sklearn import datasets
from sqlalchemy import create_engine

localhost = create_engine('mysql://root:password@localhost/solution')


def load_df():
    iris = datasets.load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df.head()
    return df


app = dash.Dash()
df = load_df()
cols = df.columns

app.layout = html.Div([
    html.H2('Contract Visualization'),
    html.Div([
        dcc.Dropdown(
            id="dropdown1",
            options=[{'label': i, 'value': i} for i in df.columns[:4]],
            value=cols[0]
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id="dropdown2",
            options=[{'label': i, 'value': i} for i in df.columns[:4]],
            value=cols[1]
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
