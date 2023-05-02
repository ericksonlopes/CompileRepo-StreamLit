import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers import GitHub

st.set_page_config(
    page_title='CompileRepo',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='auto'
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Gerador de Grafo de diretórios")


@st.cache_data
def load_data():
    return "https://github.com/ericksonlopes/SearchInExportChat"


repository_url = st.text_input("Digite o repositório: ", value=load_data())

# if not st.button("Gerar"):
#     st.stop()

github = GitHub()

nx_graph = nx.Graph()

with st.spinner('Carregando...'):
    # Cria uma barra de progresso
    st_progress_bar = st.progress(0, text=repository_url)

    nx_graph = github.build_graph(repository_url, nx_graph, st_progress_bar)

# Define a posição dos nós com espaçamento
pos = nx.spring_layout(nx_graph, seed=60, k=1.5, iterations=200)

# Define o tamanho da figura
fig, ax = plt.subplots(figsize=(14, 7))

# Desenha o grafo
nx.draw(nx_graph, pos, with_labels=True, node_size=600, ax=ax, font_size=8)

# Exibe a imagem com o Streamlit
st.pyplot(fig)

st.markdown("## Arquivos: ")
df_file = pd.DataFrame(github.files)
df_file = df_file.drop(columns=['path', 'type'])
df_file = df_file[['name', 'extension', 'size', 'lines', 'link']]
df_file = df_file.rename(columns={'name': 'Nome', 'extension': 'Extensão', 'size': 'Tamanho (KB)', 'lines': 'Linhas'})

st.table(df_file)

st.markdown("## Gráfico: ")

df_file = df_file.sort_values(by='Linhas', ascending=False)

fig = px.bar(df_file, x='Nome', y='Linhas', color='Extensão', title='Linhas por arquivo')

st.plotly_chart(fig, use_container_width=True)
