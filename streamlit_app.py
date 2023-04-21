import streamlit as st
from pyspark.sql import SparkSession

from helpers import GitHub

spark = SparkSession.builder.appName("CompileRepo").getOrCreate()

st.title("Gerador de árvore de diretórios")

repositorio = st.text_input("Digite o repositório: ")

if not st.button("Gerar"):
    st.stop()

github = GitHub()

github.generate_tree(repositorio)

st.text("Arquivos: ")
rdd_files = spark.sparkContext.parallelize(github.files)
df_files = rdd_files.toDF()
st.dataframe(df_files)

st.text("Diretórios: ")
rdd_directory = spark.sparkContext.parallelize(github.directories)
df_directory = rdd_directory.toDF()
st.dataframe(df_directory)
