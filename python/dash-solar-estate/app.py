"""
Dash Solar Estate App
Solar estate management and visualization dashboard
Uses Dash/Plotly for real-time visualization
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Initialize app
app = dash.Dash(__name__)

# Sample data
def generate_solar_data():
    dates = pd.date_range(start='2025-01-01', periods=365, freq='D')
    data = {
        'date': dates,
        'irradiance': np.random.normal(600, 150, 365),
        'temperature': np.random.normal(25, 10, 365),
        'power_output': np.random.normal(500, 100, 365),
        'efficiency': np.random.normal(0.82, 0.05, 365)
    }
    return pd.DataFrame(data)

df_solar = generate_solar_data()

# Layout
app.layout = html.Div([
    html.Header([
        html.H1('☀️ Dash Solar Estate', style={'color': '#FFD700', 'textAlign': 'center'}),
        html.P('Real-time solar energy management dashboard', style={'textAlign': 'center', 'color': '#ccc'})
    ], style={'background': '#1a1a2e', 'padding': '20px', 'marginBottom': '20px', 'borderBottom': '2px solid #FFD700'}),

    html.Div([
        html.Div([
            html.Div([
                html.H3('Solar Irradiance', style={'color': '#FFD700'}),
                dcc.Graph(id='irradiance-graph', style={'height': '400px'})
            ], style={'flex': 1, 'padding': '15px', 'border': '1px solid #FFD700', 'borderRadius': '8px', 'background': 'rgba(255, 215, 0, 0.05)'}),

            html.Div([
                html.H3('Power Output', style={'color': '#FFD700'}),
                dcc.Graph(id='power-graph', style={'height': '400px'})
            ], style={'flex': 1, 'padding': '15px', 'border': '1px solid #FFD700', 'borderRadius': '8px', 'background': 'rgba(255, 215, 0, 0.05)', 'marginLeft': '20px'})
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

        html.Div([
            html.Div([
                html.H3('System Efficiency', style={'color': '#FFD700'}),
                dcc.Graph(id='efficiency-graph', style={'height': '350px'})
            ], style={'flex': 1, 'padding': '15px', 'border': '1px solid #FFD700', 'borderRadius': '8px', 'background': 'rgba(255, 215, 0, 0.05)'}),

            html.Div([
                html.H3('Statistics', style={'color': '#FFD700'}),
                html.Div([
                    html.Div([
                        html.P('Avg Irradiance:', style={'color': '#ccc'}),
                        html.P(f"{df_solar['irradiance'].mean():.1f} W/m²", style={'color': '#FFD700', 'fontSize': '18px', 'fontWeight': 'bold'})
                    ], style={'padding': '10px', 'borderBottom': '1px solid #FFD700'}),
                    html.Div([
                        html.P('Avg Efficiency:', style={'color': '#ccc'}),
                        html.P(f"{df_solar['efficiency'].mean():.1%}", style={'color': '#FFD700', 'fontSize': '18px', 'fontWeight': 'bold'})
                    ], style={'padding': '10px', 'borderBottom': '1px solid #FFD700'}),
                    html.Div([
                        html.P('Peak Power:', style={'color': '#ccc'}),
                        html.P(f"{df_solar['power_output'].max():.0f} kW", style={'color': '#FFD700', 'fontSize': '18px', 'fontWeight': 'bold'})
                    ], style={'padding': '10px'})
                ])
            ], style={'flex': 1, 'padding': '15px', 'border': '1px solid #FFD700', 'borderRadius': '8px', 'background': 'rgba(255, 215, 0, 0.05)', 'marginLeft': '20px'})
        ], style={'display': 'flex', 'gap': '20px'})
    ], style={'padding': '20px', 'background': '#1a1a2e'})
])

# Callbacks
@app.callback(
    Output('irradiance-graph', 'figure'),
    Input('irradiance-graph', 'id')
)
def update_irradiance(id_val):
    fig = px.line(df_solar, x='date', y='irradiance', title='Solar Irradiance Over Time')
    fig.update_traces(line_color='#FFD700')
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        plot_bgcolor='rgba(26, 26, 46, 0.5)',
        paper_bgcolor='rgba(26, 26, 46, 0.5)'
    )
    return fig

@app.callback(
    Output('power-graph', 'figure'),
    Input('power-graph', 'id')
)
def update_power(id_val):
    fig = px.line(df_solar, x='date', y='power_output', title='Power Output Over Time')
    fig.update_traces(line_color='#00FF00')
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        plot_bgcolor='rgba(26, 26, 46, 0.5)',
        paper_bgcolor='rgba(26, 26, 46, 0.5)'
    )
    return fig

@app.callback(
    Output('efficiency-graph', 'figure'),
    Input('efficiency-graph', 'id')
)
def update_efficiency(id_val):
    fig = px.line(df_solar, x='date', y='efficiency', title='System Efficiency Over Time')
    fig.update_traces(line_color='#00BFFF')
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        plot_bgcolor='rgba(26, 26, 46, 0.5)',
        paper_bgcolor='rgba(26, 26, 46, 0.5)'
    )
    return fig
if __name__ == "__main__":
    print("Starting Dash Solar Estate Dashboard...")
    app.run(debug=True, port=8050)

