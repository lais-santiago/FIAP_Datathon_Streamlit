import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Configuração inicial do Streamlit
st.set_page_config(page_title="Passos Mágicos - Dashboard", layout="wide")

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/dados_consolidados.csv")  # Substitua pelo caminho correto
    return df

df = load_data()

# Criar menu de navegação
menu = st.sidebar.radio("Navegação", ["Dashboard", "Relatório"])

if menu == "Dashboard":
    from dashboard import show_dashboard
    show_dashboard(df)
elif menu == "Relatório":
    from relatorio import show_report
    show_report(df)
