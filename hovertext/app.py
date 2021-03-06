import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df1 = pd.read_csv('https://raw.githubusercontent.com/divyachandran-ds/dataset/master/Air_Quality.csv')
df = df1[df1[
             "MeasureName"] == 'Annual average ambient concentrations of PM2.5 in micrograms per cubic meter (based on seasonal averages and daily measurement)']
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Air Quality Around United States")
    ], className="row", style={"text-align": "center"}),
    html.Div([
        html.Span("State Name", style={"text-align": "center", "display": "block"}),
        dcc.Dropdown(id="select-state",
                     options=[{'label': i, 'value': i} for i in df.StateName.unique()],
                     value='New York'
                     )
    ], className="row", style={"display": "block",
                               "margin-left": "auto",
                               "margin-right": "auto",
                               "width": "60%"}),
    html.Div([
        dcc.Graph(id="my-graph")
    ], className="row"),
    html.Div([
        dcc.RangeSlider(id="select-year",
                        min=df['ReportYear'].min(),
                        max=df['ReportYear'].max(),
                        value=[1999, 2000],
                        marks={str(year): year for year in df['ReportYear'].unique()}
                        )
    ], className="row", style={"margin": 20, "padding": 30}),
    html.Div([
        html.Span("Hover Text & Formatting", className="row",
                  style={"text-align": "center", "text-decoration": "underline", "display": "block", "padding": 20}),
        html.A(" https://github.com/d3/d3-format/blob/master/README.md#locale_format", className="row",
               style={"text-align": "center", "display": "block", "padding": 20}),
        html.Div([
            html.Div([
                html.Span("Hover Text", className="six columns", style={"text-align": "right", "display": "block"}),
                html.Div([daq.BooleanSwitch(id="hover-text", on=True)], className="six columns")
            ], className="four columns", style={"width": "25%"}),
            html.Div([
                html.Span("Select Hover Format", className="six columns",
                          style={"text-align": "right", "display": "block", "padding": 10}),
                dcc.Dropdown(id="hover-format",
                             options=[{'label': "One-decimal place", 'value': ".1f"},
                                      {'label': "Two-decimal place", 'value': ".2f"},
                                      {'label': "Zero decimal place", 'value': "f"},
                                      {'label': "Rounded percentage", 'value': ".0%"},
                                      {'label': "Dot-filled and centered", 'value': ".^20"}],
                             value='.2f',
                             className="six columns"
                             )
            ], className="eight columns", style={"width": "65%", "margin": 0})
        ], className="row")
    ], className="row", style={"margin": 3, "padding": 5, "border": "1px solid black"})

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-state", "value"),
     dash.dependencies.Input("select-year", "value"),
     dash.dependencies.Input("hover-text", "on"),
     dash.dependencies.Input("hover-format", "value")]
)
def update_graph(state, year, text, format):
    dff = df[df["StateName"] == state]
    df_year = dff[(dff["ReportYear"] >= year[0]) & (dff["ReportYear"] <= year[1])]

    trace = go.Scatter(
        x=dff["CountyName"],
        y=df_year['Value'],
        mode='markers',
        marker={
            "color": "#fc8d59",
            "size": 10,
            "line": {"color": "#e34a33", "width": 0.5}
        },

    )
    layout = go.Layout(
        title="Air Quality vs County Name",

        yaxis={
            "title": "Concentrations of PM2.5 (micrograms/cu.m)",
            "hoverformat": format
        },
        xaxis={
            "title": "County Names"
        }
    )
    figure = {

        "data": [trace],
        "layout": layout
    }
    if text == True:
        # noinspection PyTypeChecker
        trace.update(go.Scatter(
            hoverinfo='x + y'
        ))
        # noinspection PyTypeChecker
        layout.update(go.Layout(
            hovermode="closest",
        ))
        return figure
    else:
        # noinspection PyTypeChecker
        layout.update(go.Layout(
            hovermode=False,
        ))
        return figure


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
