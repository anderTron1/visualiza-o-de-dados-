# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 19:13:05 2025

@author: ciencia.dados1
"""
import pandas as pd 
import sqlite3
import plotly.express as px 
import dash 
import dash_bootstrap_components as dbc 
from dash import dcc 
from dash.dependencies import Input, Output

conexao = sqlite3.connect("db/loja1.db")

script = "SELECT * FROM PRODUTOS"

dados = pd.read_sql(script, conexao)


# AGRUPANDOS OS DADOS  





# CRIANDO GRAFICOS 






app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id="dropdown-selecao",
                options=[{"label": i, "value": i} 
                    for i in dados["FORNECEDOR"].unique()],
                multi=True,
                className="dbc",
                style={"backgrouColor": "#222", "color": "#000"}
            ), width=4
        ),
    ),
    dbc.Row([    
        dbc.Col([dcc.Graph(id="fig_forn_por_qtd")], width=7),
        dbc.Col([dcc.Graph(id="fig_forn_por_vlr")], width=5)
    ], className="mb-3"),
    dbc.Row([dcc.Graph(id="fig_nome_por_qtd")])
    
])
                     
@app.callback(
    Output("fig_forn_por_qtd", "figure"),
    Output("fig_forn_por_vlr", "figure"),
    Output("fig_nome_por_qtd", "figure"),
    Input("dropdown-selecao", "value"),
    prevent_initial_call=True
)
def atualiza_dash(fornecedores):
    
    # Filtro dos Fornecedores
    dados_forn = dados[dados["FORNECEDOR"].isin(fornecedores)]
    
    # Gráfico de barra
    forn_por_qtd = dados_forn.groupby("FORNECEDOR")["QTDPROD"].sum().reset_index()

    fig_forn_por_qtd = px.bar(forn_por_qtd, x="FORNECEDOR", 
                          y="QTDPROD", color="FORNECEDOR")
    fig_forn_por_qtd.update_layout(template="plotly_dark", showlegend=False)

    # Gráfico de pizza
    
    forn_por_vlr = dados_forn.groupby("FORNECEDOR")["VLRPROD"].sum().reset_index()
    
    fig_forn_por_vlr = px.pie(forn_por_vlr,names="FORNECEDOR", 
                          values="VLRPROD", hole=0.5)
    fig_forn_por_vlr.update_layout(template="plotly_dark")
    
    # Gráfico de barra 
    nome_por_qtd = dados.groupby("NOMEPROD")["QTDPROD"].sum().reset_index()
    
    fig_nome_por_qtd = px.bar(nome_por_qtd, x="NOMEPROD", 
                          y="QTDPROD", color="NOMEPROD")
    fig_nome_por_qtd.update_layout(template="plotly_dark")
    
    return fig_forn_por_qtd, fig_forn_por_vlr, fig_nome_por_qtd

if __name__ == "__main__":
    app.run(debug=False, port=8050, host="localhost")




