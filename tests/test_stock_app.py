import os
import datetime
import pandas as pd
import pandas_datareader as web
from app.financial_time_series_plots import update_graph

current_dir = os.path.dirname(__file__)

input_data = pd.read_csv('{}/input_data.csv'.format(current_dir),
                         index_col='date', parse_dates=True)
start = datetime.date(2019, 1, 1)
end = datetime.date(2019, 1, 9)


def test_update_graph(mocker):
    mocker.patch.object(web, 'DataReader')
    web.DataReader.return_value = input_data
    return_fig = update_graph(1, 'GOOG', start, end)
    assert 'Googe' in return_fig['layout']['title']['text']
