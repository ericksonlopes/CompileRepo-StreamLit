import pandas as pd
import streamlit as st

from helpers import GitHub

st.title("Gerador de árvore de diretórios")

repositorio = st.text_input("Digite o repositório: ")

if not st.button("Gerar"):
    st.stop()

github = GitHub()

github.generate_tree(repositorio)

st.text("Arquivos: ")
df_file = pd.DataFrame(github.files)
st.table(df_file)

st.text("Diretórios: ")
df_dir = pd.DataFrame(github.directories)
st.table(df_dir)
