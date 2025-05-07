import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import redis
import plotly.graph_objs as go
import time

# Inicializar app Dash
app = dash.Dash(__name__)
app.title = "Sistema de Insultos - Dashboard"

# Configuración Redis y RabbitMQ API
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
RABBIT_API = "http://localhost:15672/api/queues"
AUTH = ("guest", "guest")

# Layout
app.layout = html.Div([
    html.H1("Dashboard del sistema de insultos (RabbitMQ + PyRO + Redis)", style={"textAlign": "center"}),

    dcc.Interval(id='interval', interval=5*1000, n_intervals=0),

    html.Div([
        html.Div([dcc.Graph(id='queue-status')], className='six columns'),
        html.Div([dcc.Graph(id='scaling-status')], className='six columns')
    ], className='row'),

    html.Div([
        html.Div([dcc.Graph(id='throughput-status')], className='six columns'),
        html.Div([
            html.H3("Últimos 5 insultos enviados por Notifier"),
            html.Ul(id='last-insults')
        ], className='six columns')
    ], className='row')
])

# Callbacks
@app.callback(
    Output('queue-status', 'figure'),
    Output('scaling-status', 'figure'),
    Output('throughput-status', 'figure'),
    Output('last-insults', 'children'),
    Input('interval', 'n_intervals')
)
def update_dashboard(n):
    # RabbitMQ queue sizes
    try:
        response = requests.get(RABBIT_API, auth=AUTH)
        data = response.json()
        insult_q = next((q['messages'] for q in data if q['name'] == 'insult_queue'), 0)
        text_q = next((q['messages'] for q in data if q['name'] == 'text_queue'), 0)
    except:
        insult_q, text_q = 0, 0

    queue_fig = go.Figure()
    queue_fig.add_trace(go.Bar(x=['insult_queue', 'text_queue'], y=[insult_q, text_q]))
    queue_fig.update_layout(title='Estado de colas RabbitMQ', yaxis_title='Mensajes en cola')

    # Scaling info
    insult_instances = len([k for k in r.keys() if k.startswith("scaling_insult_")])
    filter_instances = len([k for k in r.keys() if k.startswith("scaling_filter_")])
    scaling_fig = go.Figure()
    scaling_fig.add_trace(go.Bar(x=['InsultService', 'FilterService'], y=[insult_instances, filter_instances]))
    scaling_fig.update_layout(title='Nº instancias activas', yaxis_title='Nodos')

    # Throughput (simulado por diferencia entre llamadas)
    tp_insult = int(r.get("throughput_insult") or 0)
    tp_filter = int(r.get("throughput_filter") or 0)
    throughput_fig = go.Figure()
    throughput_fig.add_trace(go.Indicator(mode="number", value=tp_insult, title="InsultService req/s"))
    throughput_fig.add_trace(go.Indicator(mode="number", value=tp_filter, title="FilterService req/s", domain={'x': [0.5, 1]}))
    throughput_fig.update_layout(title="Throughput actual")

    # Últimos 5 insultos del Notifier
    insults = r.lrange("notifier_events", -5, -1)[::-1]
    insult_list = [html.Li(ins) for ins in insults]

    return queue_fig, scaling_fig, throughput_fig, insult_list

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
