import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Visão Geral", layout="wide")

# Carregar os dados
df = pd.read_csv("data/dados_consolidados.csv")

st.title("📌 Visão Geral")

# Indicadores principais (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("📈 Média INDE", round(df["inde"].mean(), 2))
col2.metric("🎯 Ponto de Virada (%)", f"{round(df['atingiu_ponto_virada'].mean() * 100, 2)}%")
col3.metric("🏆 Indicados para Bolsa (%)", f"{round(df['indicado_bolsa'].mean() * 100, 2)}%")
col4.metric("🎓 Taxa de Formatura (%)", f"{round(df['formado'].mean() * 100, 2)}%")

# Evolução temporal
fig = px.line(df.groupby("ano").mean().reset_index(), x="ano", y="inde", title="Evolução do Índice INDE")
st.plotly_chart(fig)
