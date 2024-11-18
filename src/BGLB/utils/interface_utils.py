from http.client import responses
import dash
from dash import dcc, html, Input, Output, ctx
import requests
import plotly.express as px

# Inicializando o app Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("DADOS SOBRE A AREA DE DADOS NO BRASIL"),
    dcc.Dropdown(
        id="dropdown-selecao",
        options=[
            {'label': 'Distribuição de Faixa Etária', 'value': 'faixa_etaria'},
            {'label': 'Distribuição de Gênero', 'value': 'genero'},
            {'label': 'Distribuição de faixa salarial', 'value': 'faixa_salarial'},
            {'label': 'Distribuição de Raças', 'value': 'raca'},
            {'label': 'Distribuição de Pessoas com Deficiencia', 'value': 'pcd'}
        ],
        value='faixa_etaria',  # Valor inicial
        style={'width': '50%'}
    ),
    dcc.Graph(id="grafico"),
    dcc.Interval(
        id="intervalo-atualizacao",
        interval=60000,  # Atualiza a cada 10 segundos
        n_intervals=0  # Inicializa com 0 intervalos
    )
])

# Funções para obter dados das APIs
def obter_dados_faixa_etaria():
    url = "http://localhost:5001/data1"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        print(f"Dados da API faixa etária: {dados}")
        return dados
    return {'faixa_18_25': [0], 'faixa_26_35': [0], 'faixa_36_50': [0], 'faixa_50_plus': [0]}

def obter_dados_genero():
    url = "http://localhost:5001/data2"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        print(f"Dados da API gênero: {dados}")
        return dados
    return {'Masculino': [0], 'Feminino': [0], 'Prefiro não dizer / Outros': [0]}

def obter_raca():
    url = "http://localhost:5001/data4"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        print(f"Dados da API raças: {dados}")
        return dados
    return {'Branca': [0], 'Parda': [0], 'Preta': [0], 'Amarela': [0], 'Indio': [0], 'Outro': [0]}

def obter_pcd():
    url = "http://localhost:5001/data5"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        print(f"Dados da API PCD: {dados}")
        return dados
    return {'Sim': [0], 'Nao': [0]}

def obter_dados_faixa_salarial():
    url = "http://localhost:5001/data3"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        print(f"Dados da API faixa salarial: {dados}")
        return dados
    return {
        'faixa_1001_2000': [0],
        'faixa_2001_3000': [0],
        'faixa_3001_4000': [0],
        'faixa_4001_6000': [0],
        'faixa_6001_8000': [0],
        'faixa_8001_12000': [0],
        'faixa_12001_16000': [0],
        'faixa_16001_20000': [0],
        'faixa_20001_25000': [0]
    }

# Cache para evitar chamadas desnecessárias
cache_selecao = None

# Função callback para atualizar o gráfico com base na seleção e no intervalo
@app.callback(
    Output("grafico", "figure"),
    [Input("dropdown-selecao", "value"), Input("intervalo-atualizacao", "n_intervals")]
)
def atualizar_grafico(selecao, n):
    global cache_selecao

    # Verifica se o dropdown mudou
    if ctx.triggered_id == "dropdown-selecao" or cache_selecao != selecao:
        cache_selecao = selecao
        print(f"Atualizando dados com base na seleção: {selecao}")

    # Escolhe a função de API com base na seleção
    if cache_selecao == "faixa_etaria":
        dados = obter_dados_faixa_etaria()
        fig = px.pie(
            names=['18-25', '26-35', '36-50', '50+'],
            values=[
                dados['faixa_18_25'][0],
                dados['faixa_26_35'][0],
                dados['faixa_36_50'][0],
                dados['faixa_50_plus'][0]
            ],
            title="Distribuição de Faixa Etária"
        )
    elif cache_selecao == "genero":
        dados = obter_dados_genero()
        fig = px.pie(
            names=['Masculino', 'Feminino', 'Prefiro não dizer / Outros'],
            values=[
                dados['Masculino'][0],
                dados['Feminino'][0],
                dados['Prefiro não dizer / Outros'][0]
            ],
            title="Distribuição de Gênero"
        )
    elif cache_selecao == "faixa_salarial":
        dados = obter_dados_faixa_salarial()
        faixas = [
            'R$ 1.001 a R$ 2.000', 'R$ 2.001 a R$ 3.000', 'R$ 3.001 a R$ 4.000',
            'R$ 4.001 a R$ 6.000', 'R$ 6.001 a R$ 8.000', 'R$ 8.001 a R$ 12.000',
            'R$ 12.001 a R$ 16.000', 'R$ 16.001 a R$ 20.000', 'R$ 20.001 a R$ 25.000'
        ]
        contagem = [
            dados['faixa_1001_2000'][0], dados['faixa_2001_3000'][0],
            dados['faixa_3001_4000'][0], dados['faixa_4001_6000'][0],
            dados['faixa_6001_8000'][0], dados['faixa_8001_12000'][0],
            dados['faixa_12001_16000'][0], dados['faixa_16001_20000'][0],
            dados['faixa_20001_25000'][0]
        ]
        fig = px.bar(
            x=faixas,
            y=contagem,
            title="Distribuição de Faixa Salarial",
            labels={'x': 'Faixa Salarial', 'y': 'Contagem'},
            color=contagem,
            color_continuous_scale='Viridis'
        )
    elif cache_selecao == "raca":
        dados = obter_raca()
        fig = px.pie(
            names=['Brancas', 'Pardas', 'Pretas', 'Amarelas', 'Indígenas', 'Outros'],
            values=[
                dados['Branca'][0],
                dados['Parda'][0],
                dados['Preta'][0],
                dados['Amarela'][0],
                dados['Indio'][0],
                dados['Outro'][0]
            ],
            title="Distribuição de Raças"
        )
    elif cache_selecao == "pcd":
        dados = obter_pcd()
        fig = px.pie(
            names=['Sim', 'Não'],
            values=[dados['Sim'][0], dados['Nao'][0]],
            title="Distribuição de Pessoas com Deficiência"
        )
    else:
        fig = px.scatter(title="Selecione um dado para visualizar")

    return fig

# Rodando o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
