import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_dashboard(df):
    st.title("📊 Dashboard - Análise dos Alunos da Passos Mágicos")

    # KPIs - Indicadores Chave
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Média INDE", round(df["inde"].mean(), 2))
    col2.metric("🎯 % Ponto de Virada", f"{round(df['atingiu_ponto_virada'].mean() * 100, 2)}%")
    col3.metric("🎓 % Alunos com Bolsa", f"{round(df['indicado_bolsa'].mean() * 100, 2)}%")
    col4.metric("🏆 Taxa de Formatura", f"{round(df['formado'].mean() * 100, 2)}%")

    st.markdown("---")

    # Evolução dos Indicadores ao longo dos anos
    st.subheader("📊 Evolução dos Indicadores (2022-2024)")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="inde", label="INDE", marker="o")
    sns.lineplot(data=df, x="ano", y="ipv", label="Ponto de Virada", marker="o")
    plt.legend()
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução do Desempenho")
    st.pyplot(fig)

    st.markdown("---")

    # Comparação por Fase
    st.subheader("📌 Comparação de Desempenho por Fase")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df, x="fase", y="inde")
    plt.xlabel("Fase")
    plt.ylabel("INDE")
    plt.title("Distribuição do INDE por Fase")
    st.pyplot(fig)

    st.markdown("---")

    # Comparação por Gênero e Instituição
    st.subheader("👨‍🎓👩‍🎓 Desempenho por Gênero e Instituição")
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=df, x=df["feminino"].map({1: "Feminino", 0: "Masculino"}), y="inde")
        plt.xlabel("Gênero")
        plt.ylabel("INDE")
        plt.title("Desempenho por Gênero")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=df, x=df["instituicao_publica"].map({1: "Pública", 0: "Privada"}), y="inde")
        plt.xlabel("Tipo de Escola")
        plt.ylabel("INDE")
        plt.title("Desempenho por Tipo de Escola")
        st.pyplot(fig)

    st.markdown("---")

    # Análise Individual
    st.subheader("🔎 Análise Individual do Aluno")
    aluno = st.selectbox("Selecione um aluno pelo RA:", df["ra"].unique())

    aluno_df = df[df["ra"] == aluno]
    st.write(aluno_df)

    # Predição de Desempenho
    st.subheader("🤖 Predição de Desempenho Futuro")
    X = df[["idade", "ieg", "ida", "ips", "ian", "ipv"]]
    y = df["inde"]
    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict(aluno_df[["idade", "ieg", "ida", "ips", "ian", "ipv"]])
    st.write(f"📊 Previsão do INDE futuro: **{round(pred[0], 2)}**")

