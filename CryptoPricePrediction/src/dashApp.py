import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import dbController
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

df = dbController.readDB()
dff = df.copy()


app.layout = html.Div(children = [
    html.Div(children=[
        html.H1('CryptoCurrencies Dashboard'), 
    ], className='row'), 
    html.Div(children=[
        html.Div(children=[
             dcc.Dropdown(
                 id='coinselector', 
                 options = [{'label':'Bitcoin', 'value': 'BTC'}, 
                            {'label':'Ethereum', 'value': 'ETH'}, 
                            {'label':'Litecoin', 'value': 'LTC'}, 
                            {'label':'Ripple', 'value': 'XRP'}, 
                 ], 
                 value = 'BTC', 
                 className='coinselector'
             )
        ], className='three columns div-user-controls'), 
        html.Div(children=[
            dcc.Graph(id='timeseries'), 
            dcc.Graph(id='change'), 
        ], className='nine columns'), 
        
    ], className='row')
])

@app.callback(Output('timeseries', 'figure'), 
              [Input('coinselector', 'value')])
def update_timeseries(selected_dropdown_value):
    coin = selected_dropdown_value
    print(coin)
    fig  = px.line(dff, x=dff.index, y=f'{coin}_value')
    fig.update_layout(hovermode='x')
    fig.update_xaxes(
        rangeslider = dict(
            visible = True,
        ),
        type = 'date', 
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig

@app.callback(Output('change', 'figure'), 
              [Input('coinselector', 'value')])
def update_changes(selected_dropdown_value):
    coin = selected_dropdown_value
    diffs = dff.diff()
    fig = px.bar(diffs, x=diffs.index, y = f'{coin}_value')
    fig.update_layout(hovermode='x')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
