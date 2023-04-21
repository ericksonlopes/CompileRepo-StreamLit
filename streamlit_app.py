import streamlit as st
from helpers import GitHub
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CompileRepo").getOrCreate()

st.title("Gerador de árvore de diretórios")

repositorio = st.text_input("Digite o repositório: ")

if not st.button("Gerar"):
    st.stop()

github = GitHub()

github.generate_tree(repositorio)

st.text("Arquivos: ")
spark.createDataFrame(github.files).show()
# st.dataframe(df_files)
#
# st.text("Diretórios: ")
# df_directory = pd.DataFrame(github.directories)
# st.dataframe(df_directory)
