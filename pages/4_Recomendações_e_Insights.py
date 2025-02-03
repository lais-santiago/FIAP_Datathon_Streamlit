import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Recomendações e Insights", layout="wide")

# Carregar os dados
df = pd.read_csv("data/dados_consolidados.csv")

st.title("💡 Recomendações e Insights")

# Exibir principais insights
st.subheader("📌 Principais Descobertas")

st.markdown("""
- Alunos que atingiram **ponto de virada** geralmente possuem um **INDE acima de 8.3**.
- Alunos da **fase 2** possuem maior taxa de abandono.
- O **Indicador de Engajamento (IEG)** é um dos fatores mais correlacionados com o sucesso acadêmico.
- Há uma disparidade entre alunos de **instituições públicas e privadas**, sendo que alunos de escolas privadas apresentam melhores resultados médios.
""")

# Sugestões de Ação
st.subheader("📢 Sugestões para a Passos Mágicos")
st.markdown("""
✅ Implementar programas de mentoria para alunos da Fase 2 para reduzir a evasão.
✅ Focar em estratégias para melhorar o engajamento dos alunos, visto que o **IEG** tem forte correlação com sucesso.
✅ Criar um programa de incentivo para alunos de escolas públicas, reduzindo a desigualdade de desempenho.
""")
