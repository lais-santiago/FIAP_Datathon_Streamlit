import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise Comparativa", layout="wide")

# Carregar os dados
df = pd.read_csv("data/dados_consolidados.csv")

st.title("📊 Análise Comparativa")

# Comparação por ano
fig = px.box(df, x="ano", y="inde", color="ano", title="Distribuição do INDE por Ano")
st.plotly_chart(fig)

# Comparação por fase
fig_fase = px.box(df, x="fase", y="inde", color="fase", title="Desempenho por Fase de Aprendizado")
st.plotly_chart(fig_fase)

# Comparação por gênero
fig_genero = px.box(df, x="feminino", y="inde", color="feminino", title="Desempenho por Gênero (1=Feminino, 0=Masculino)")
st.plotly_chart(fig_genero)
