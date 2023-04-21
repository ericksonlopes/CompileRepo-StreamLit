import findspark
import streamlit as st

from helpers import GitHub

findspark.init()
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

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
