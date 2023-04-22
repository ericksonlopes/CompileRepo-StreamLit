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

st.title("Gerador de árvore de diretórios")


@st.cache_data
def load_data():
    return "https://github.com/ericksonlopes/SearchInExportChat-StreamLit"


repositorio = st.text_input("Digite o repositório: ", value=load_data())

if not st.button("Gerar"):
    st.stop()

github = GitHub()

github.generate_tree(repositorio)

st.markdown("## Arquivos: ")
df_file = pd.DataFrame(github.files)
df_file = df_file.drop(columns=['path', 'type'])
df_file = df_file[['name', 'extension', 'size', 'lines', 'link']]
df_file = df_file.rename(columns={'name': 'Nome', 'extension': 'Extensão', 'size': 'Tamanho (KB)', 'lines': 'Linhas'})

st.table(df_file)

st.markdown("## Gráfico: ")

