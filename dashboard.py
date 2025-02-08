import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def show_dashboard(df):

    st.sidebar.header("Filtros")
    ano_selecionado = st.sidebar.selectbox("Selecione o ano para análise:", [2022, 2023, 2024])

    # Filtrando os dados pelo ano selecionado
    df_selecionado = df[df["ano"] == ano_selecionado]

    st.title("📊 Dashboard - Análise dos Alunos da Passos Mágicos")

    st.subheader(f"Big Numbers ano {ano_selecionado}")

    inde_medio=df_selecionado['inde'].mean()
    ian_medio=df_selecionado['ian'].mean()
    ida_medio=df_selecionado['ida'].mean()
    ieg_medio=df_selecionado['ieg'].mean()
    iaa_medio=df_selecionado['iaa'].mean()
    ips_medio=df_selecionado['ips'].mean()
    ipp_medio=df_selecionado['ipp'].mean()
    ipv_medio=df_selecionado['ipv'].mean()

    st.metric(label="Média Índice de Desenvolvimento Educacional (INDE)", value=round(inde_medio, 2))

    st.markdown("#### 📚 __Média dos Indicadores que compõem o INDE__")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1: 
        st.metric(label="📖 Adequação de Nível (IAN)", value=round(ian_medio, 2))
        st.metric(label="🧘 Psicossocial (IPS)", value=round(ips_medio, 2))

    with col2:
        st.metric(label="📖 Desempenho Acadêmico (IDA)", value=round(ida_medio, 2))
        st.metric(label="✏️ Psicopedagógico (IPP)", value=round(ipp_medio, 2))


    with col3:
        st.metric(label="📖 Engajamento (IEG)", value=round(ieg_medio, 2))
        st.metric(label="✏️ Ponto de Virada (IPV)", value=round(ipv_medio, 2))

    with col4:
        st.metric(label="🧘 Indicador de Autoavaliação (IAA)", value=round(iaa_medio, 2))

    total = len(df)
    atingiu_ponto_virada = df_selecionado["atingiu_ponto_virada"].sum()
    perc_ponto_virada = (atingiu_ponto_virada / total) * 100
    st.metric(label="🎯 Percentual de alunos que atingiram o ponto de virada", value=f"{perc_ponto_virada:.2f}%")

    # Contagem de alunos por categoria
    contagem = df_selecionado["pedra"].value_counts()
    total_alunos = len(df)
    percentuais = (contagem / total_alunos) * 100

    # Criando os Big Numbers com círculos coloridos
    st.markdown("#### 💎 __Percentual de Alunos por Categoria__")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="🔵 Quartzo", value=f"{percentuais['quartzo']:.2f}%")

    with col2:
        st.metric(label="🔴 Ágata", value=f"{percentuais['agata']:.2f}%")

    with col3:
        st.metric(label="🟣 Ametista", value=f"{percentuais['ametista']:.2f}%")

    with col4:
        st.metric(label="🟠 Topázio", value=f"{percentuais['topazio']:.2f}%")

    anos = np.array([2022, 2023, 2024])
    
    st.subheader("📊 Evolução dos Indicadores  (2022-2024)")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="inde", label="INDE", marker="o")
    ax.set_xticks(anos)
    plt.legend(loc='lower left')
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução do Índice de Desenvolvimento Educacional (INDE)")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="ian", label="IAN", marker="o")
    sns.lineplot(data=df, x="ano", y="ida", label="IDA", marker="o")
    sns.lineplot(data=df, x="ano", y="ieg", label="IEG", marker="o")
    ax.set_xticks(anos)
    plt.legend(loc='best')
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução dos Indicadores de Dimensão Acadêmica")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="iaa", label="IAA", marker="o")
    sns.lineplot(data=df, x="ano", y="ips", label="IPS", marker="o")
    ax.set_xticks(anos)
    plt.legend(loc='best')
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução dos Indicadores de Dimensão Psicossocial")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="ipp", label="IPP", marker="o")
    sns.lineplot(data=df, x="ano", y="ipv", label="IPV", marker="o")
    ax.set_xticks(anos)
    plt.legend(loc='best')
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução dos Indicadores de Dimensão Psicopedagógica")
    st.pyplot(fig)

    st.markdown("---")

    # Comparação por Fase
    st.subheader(f"📌 Comparação de Desempenho por Fase e ano {ano_selecionado}")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df_selecionado, x="fase", y="inde")
    plt.xlabel("Fase")
    plt.ylabel("INDE")
    plt.title("Distribuição do INDE por Fase")
    st.pyplot(fig)

    st.markdown("---")

    # Comparação por Gênero e Instituição
    st.subheader(f"👨‍🎓👩‍🎓 Desempenho por Gênero e Instituição no ano {ano_selecionado}")

    # Criando a coluna 'instituicao' com base nas colunas existentes
    df["instituicao"] = df_selecionado.apply(
        lambda row: "publica" if row["instituicao_publica"] == 1 else 
                    "privada" if row["instituicao_privada"] == 1 else 
                    "nao informado", axis=1
    )

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.swarmplot(data=df_selecionado, x="genero", y="inde", ax=ax, palette="coolwarm_r")
        ax.set_ylim(0, 10)
        plt.xlabel("Gênero")
        plt.ylabel("INDE")
        plt.title("Distribuição de INDE por Gênero")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.swarmplot(data=df_selecionado, x="instituicao", y="inde", ax=ax, palette="viridis", size=4)
        ax.set_ylim(0, 10)
        plt.xlabel("Tipo de Instituição")
        plt.ylabel("INDE")
        plt.title("Distribuição de INDE por Tipo de Instituição")
        st.pyplot(fig)

    st.markdown("---")

    # Análise do perfil dos alunos topázio
    st.subheader(f"🔹 Perfil dos Alunos Topázio do ano {ano_selecionado}")

    df_topazio = df_selecionado[df_selecionado['pedra'] == 'topazio']

    indicadores = ["inde", "ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv"]

    # Calculando médias
    media_topazio = df_topazio[indicadores].mean()
    media_geral = df_selecionado[indicadores].mean()

    # Criando um gráfico de radar
    labels = indicadores
    num_vars = len(labels)

    angles = np.linspace(0,2 * np.pi, num_vars, endpoint=False).tolist()
    media_topazio = np.concatenate((media_topazio, [media_topazio[0]]))
    media_geral = np.concatenate((media_geral, [media_geral[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, media_topazio, color="blue", alpha=0.4, label="Topázio")
    ax.fill(angles, media_geral, color="yellow", alpha=0.4, label="Média Geral")

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title(f"Perfil dos Alunos Topázio vs Média Geral no ano {ano_selecionado}")
    plt.legend(loc='lower left')
    st.pyplot(fig)

    st.markdown("---")

    # Análise de alunos que atingiram o ponto de virada
    st.subheader("🚀 Análise de alunos que atingiram o ponto de virada vs os que não atingiram")

    # Filtrando os alunos
    df_virada = df_selecionado[df_selecionado["atingiu_ponto_virada"] == 1]
    df_sem_virada = df_selecionado[df_selecionado["atingiu_ponto_virada"] == 0]

    # Criando um DataFrame com as médias para visualização
    df_comparacao = pd.DataFrame({
        "Indicador": indicadores,
        "Com Ponto de Virada": df_virada[indicadores].mean(),
        "Sem Ponto de Virada": df_sem_virada[indicadores].mean()
    }).melt(id_vars="Indicador", var_name="Grupo", value_name="Valor")

    # Criando gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_ylim(0, 10)
    sns.barplot(data=df_comparacao, x="Indicador", y="Valor", hue="Grupo", ax=ax)

    plt.xticks(rotation=45)
    plt.title("Comparação dos Indicadores: Com vs Sem Ponto de Virada")
    st.pyplot(fig)


    st.markdown("---")

    st.subheader("🎓 Listagem de alunos por fase")

    # Filtros
    fase_selecionada = st.selectbox("Selecione a Fase: ", sorted(df["fase"].unique()))

    # Filtrando os dados
    df_filtrado = df_selecionado[df_selecionado["fase"] == fase_selecionada]

    # Reduzindo as colunas
    colunas_desejadas = ["ra", "idade", "genero", "turma", "fase",  "fase_ideal",  "instituicao", "pedra", "inde", "iaa", "ieg", "ips", "ida", "ipv", "ian", "ipp", "nota_matematica", "nota_portugues", "nota_ingles", "indicado_bolsa", "atingiu_ponto_virada"]
    df_reduzido = df_filtrado[colunas_desejadas]

    # Exibir tabela interativa
    st.dataframe(df_reduzido)

    st.markdown("---")

    # Predição de Desempenho
    st.subheader("📊 Previsão de Indicação para Bolsa")

    st.write("Insira os valores dos indicadores para prever se o aluno poderá ser indicado para bolsa:")

    indicadores_previsao = ["idade", "fase", "iaa", "ieg", "ips", "ida", "ipv", "ian", "ipp"]

    modelo=cria_modelo(df, indicadores_previsao)

    # Criando campos para o usuário inserir valores dos indicadores
    valores = {}
    for indicador in indicadores_previsao:
        if indicador == "idade":
            valores[indicador] = st.slider(f"{indicador.upper()} (7-18 anos)", min_value=7, max_value=18, value=10)
        elif indicador == "fase":
            valores[indicador] = st.slider(f"{indicador.upper()} (0-7)", min_value=0, max_value=7, value=2)
        else:
            valores[indicador] = st.slider(f"{indicador.upper()} (0-10)", min_value=0.0, max_value=10.0, value=5.0)

    # Botão para realizar a previsão
    if st.button("📊 Prever Indicação para Bolsa"):
        entrada = np.array([list(valores.values())])
        probabilidade = modelo.predict_proba(entrada)[0][1] * 100

        # Exibir o resultado da previsão
        st.success(f"✨ Probabilidade de indicação para bolsa: **{probabilidade:.2f}%**")

        # Classificação baseada na probabilidade
        if probabilidade > 80:
            st.write("💰 O aluno tem **alta probabilidade** de ser indicado para bolsa.")
        elif probabilidade > 50:
            st.write("🟡 O aluno tem **média probabilidade** de receber bolsa.")
        else:
            st.write("🔻 O aluno tem **baixa probabilidade** de ser indicado para bolsa.")


def cria_modelo(df, indicadores):
    # Definição de variáveis
    X = df[indicadores]
    y = df["indicado_bolsa"]

    # Separando os dados para treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinando o modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Avaliação do modelo
    y_pred = modelo.predict(X_test)
    print(f"Acurácia do Modelo: {accuracy_score(y_test, y_pred):.2f}")

    return modelo