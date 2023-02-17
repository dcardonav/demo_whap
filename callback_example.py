from dash import dcc, html, Input, Output, Dash

app = Dash()

app.layout = html.Div(
    [
        dcc.Input(id='input_text', value='Change this text', type='text'),
        html.Div(id='output_text', children='')
    ]
)

@app.callback(
    Output(component_id='output_text', component_property='children'),
    Input(component_id='input_text', component_property='value')
)
def updateOutputDiv(input_text):
    return f'Text: {input_text}'

if __name__ == '__main__':
    app.run_server(debug=True)
