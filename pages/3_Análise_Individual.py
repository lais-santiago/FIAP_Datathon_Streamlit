import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Análise Individual", layout="wide")

# Carregar os dados
df = pd.read_csv("data/dados_consolidados.csv")

st.title("🔍 Análise Individual do Aluno")

# Seleção do aluno
aluno_selecionado = st.selectbox("Selecione um aluno pelo RA:", df["ra"].unique())

# Dados do aluno
aluno_df = df[df["ra"] == aluno_selecionado]
st.write("📌 Informações do aluno:", aluno_df)

# Evolução dos indicadores do aluno ao longo dos anos
st.line_chart(aluno_df.set_index("ano")[["inde", "ieg", "ida", "ipv"]])
