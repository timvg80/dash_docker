import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas_datareader as web
from dateutil.relativedelta import relativedelta
import datetime


app = dash.Dash()

stock_choices = [('Apple', 'AAPL'), ('IBM', 'IBM'), ('Google', 'GOOG'),
                 ('Tesla', 'TSLA'), ('Amazon', 'AMZN')]

stock_lookup = {v: i for i, v in stock_choices}

today_time = datetime.datetime.now()
today = datetime.date(today_time.year, today_time.month, today_time.day)

# The next variable is a year minus a day in the past
# This is because the Robinhood API from pandas_datareader can only go this far
first_date = today - relativedelta(years=1) + relativedelta(days=1)

app.layout = html.Div(
    [
        # The left most dropdown - this is to get the stock of interest
        html.Div(
            [
                html.H1('Pick Stock'),
                dcc.Dropdown(
                    id='stock',
                    options=[
                        {'label': i[0], 'value': i[1]} for i in stock_choices
                    ],
                    value='AAPL'
                )
            ], style={'width': '45%', 'display': 'inline-block',
                      'horizontal-align': 'center', 'vertical-align': 'top'}
        ),
        # The right widget - used to select the date
        html.Div(
            [
                html.H1('Pick Date Range'),
                dcc.DatePickerRange(
                    id='date_range',
                    min_date_allowed=first_date,
                    max_date_allowed=today,
                    start_date=first_date,
                    end_date=today,
                    display_format='MMM Do, YYYY'
                )
            ], style={'width': '45%', 'display': 'inline-block',
                      'textAlign': 'center'}
        ),
        html.P(
            html.Button(
                id='input_button',
                n_clicks=0,
                children='Submit',
                style=dict(fontSize=18)
            )
        ),
        dcc.Graph(
            id='candlestick'
        )
    ]
)


@app.callback(Output('candlestick', 'figure'),
              [Input('input_button', 'n_clicks')],
              [State('stock', 'value'),
               State('date_range', 'start_date'),
               State('date_range', 'end_date')])
def update_graph_wrapper(n_clicks, stock, start, end):
    fig = update_graph(n_clicks, stock, start, end)
    return fig


def update_graph(n_clicks, stock, start, end):
    stock_df = web.DataReader(stock, 'iex', start, end)
    stock_df.reset_index(inplace=True)
    fig = ff.create_candlestick(
        open=stock_df['open'],
        high=stock_df['high'],
        low=stock_df['low'],
        close=stock_df['close'],
        dates=stock_df['date']
    )
    fig['layout']['title'] = 'Candlestick plot for {} stocks' \
        .format(stock_lookup[stock])
    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

