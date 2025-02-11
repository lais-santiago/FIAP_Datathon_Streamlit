import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show_report(df):
    st.title("📄 Relatório Analítico")

    st.header("1️⃣ Introdução")
    st.write("""
    A ONG Passos Mágicos atua na transformação social através da educação, atendendo crianças e jovens em situação de vulnerabilidade.
    Este relatório apresenta os impactos do projeto entre os anos de 2022, 2023 e 2024.
    """)

    st.header("2️⃣ Metodologia")
    st.write("""
    Os dados passaram por limpeza, padronização e criação de novas variáveis. Foram feitas análises descritivas e preditivas para entender os fatores que impactam o sucesso dos alunos.
             
    \n\nForam fornecidas 3 bases, sendo uma para cada ano: 2022, 2023 e 2024, mas com divergência nas colunas.
             
    \n\nPara a base do ano de __2022__ foram realizados os seguintes tratamentos:
    \n\n-    Foi removida uma linha do dataframe, que era composta somente de valores inválidos (NaN).
    \n\n-    Foi identificado que faltava a informação de um dos indicadores (IPP), que foi obtido através de outra base de 2022, que foi fornecida no desafio na versão original. Como a base nova tinha mais informações, essa coluna foi criada base nova, sendo preenchida com o valor da antiga, cruzando pelo valor da coluna CG (Classificação Geral).
    \n\n-    Foram renomeadas as colunas seguindo o padrão snake_case
    \n\n-    As colunas fase, ano_nascimento, classificacao_fase, classificacao_turma e quantidade_avaliadores tiveram seu formato adequado para int
    \n\n-    Foi criada uma coluna de ano, com valor fixo de 2022   

    \n\nPara a base do ano de __2023__ foram realizados os seguintes tratamentos:
    \n\n-    Não foram encontradas nem linhas duplicadas, nem linhas com valor 'NaN' em todas as colunas
    \n\n-    As colunas foram renomeadas para o padrão snake_case
    \n\n-    A coluna fase possuía um domínio diferente do dataframe de 2022, portanto os valores foram convertidos conforme abaixo:
             \n\n\tALFA > 0
             \n\n\tFASE 1 > 1
             \n\n\tFASE 2 > 2
             \n\n\tFASE 3 > 3
             \n\n\tFASE 4 > 4
             \n\n\tFASE 5 > 5
             \n\n\tFASE 6 > 6
             \n\n\tFASE 7 > 7
             \n\n\tFASE 8 > 8
    \n\n-    A coluna turma possuía também um domínio diferente do dataframe de 2022, sendo composta pela fase + turma, como por exemplo '1A', de onde foi extraída somente a letra 'A'.
    \n\n-    Como no dataframe de 2022 havia uma coluna de ano_nascimento, enquanto que no de 2023 há uma coluna de data_nascimento, para equiparar os dataframes essa coluna foi convertida em datetime e dela foi extraído o ano de nascimento.
    \n\n-    Como no dataframe de 2022 havia uma coluna de idade, essa coluna foi gerada nesse dataframe subtraindo a data de 01.01.2024 da data de nascimento.
    \n\n-    As colunas inde, inde_2022, iaa, ieg, ips, ipp, ida, nota_matematica, nota_portugues, nota_ingles, ipv e ian estavam com formato object, então foram convertidas para float.
    \n\n-    Foi criada uma coluna de ano, com valor fixo de 2023.

    \n\nPara a base do ano de __2024__ foram realizados os seguintes tratamentos:
    \n\n-    Não foram encontradas nem linhas duplicadas, nem linhas com valor 'NaN' em todas as colunas
    \n\n-    As colunas foram renomeadas para o padrão snake_case.
    \n\n-    Tanto a coluna fase, quanto a coluna turma tinha os valores misturados, como por exemplo '1A'. Dessa forma os valores foram separados em '1'para fase e 'A' para turma, nesse caso.
    \n\n-    Como no dataframe de 2022 havia uma coluna de ano_nascimento, enquanto que no de 2024 há uma coluna de data_nascimento, para equiparar os dataframes essa coluna foi convertida em datetime e dela foi extraído o ano de nascimento.
    \n\n-    As colunas inde, inde_2022, inde_2023, iaa, ieg, ips, ipp, ida, nota_matematica, nota_portugues, nota_ingles, ipv e ian estavam com formato object, então foram convertidas para float.
    \n\n-    As colunas recomendacao_avaliador_3 e recomendacao_avaliador_4 não estavam preenchidas para nenhum aluno. Mas como para os outros anos essa coluna existia, foi atribuído o valor fixo de "não avaliado" para todas as linhas.
    \n\n-    Foi criada uma coluna de ano, com valor fixo de 2024.
             
    \n\nForam então eliminadas colunas que não seriam utilizadas na análise e os dataframes foram concatenados em um único dataframe.
    \n\nCom o novo dataframe gerado, algumas colunas foram normalizadas:
             \n\n-    A coluna genero que possuia 4 tipos de valores (Feminino, Masculino, Menino e Menina) teve seus valores convertidos para somente 2 tipos de valores (Feminino e Masculino). Foi aplicado então one-hot encoding nessa coluna, criando duas novas com valores 0 e 1, com os nomes feminino e masculino.
             \n\n-    A coluna instituicao_ensino tinha diversos valores, dentre eles alguns valores indicavam que o aluno era bolsista. Como já havia uma coluna indicado_bolsa, que não tinha todos os valores preenchidos, essa informação foi extraída e foi alimentada na coluna indicado_bolsa, onde haviam dados faltantes.
             \n\n-    Os valores de instituicao_ensino foram reclassificados para instituicao_publica, instituicao_privada e nao_informado (quando não era possível associar a nenhum dos 2 outros valores). Posteriormente foi aplicado o one-hot encoding nessa coluna.
             \n\n-    Foi identificado que alguns valores de inde não estavam preenchidos, mas com os valores dos outros indicadores foram aplicadas as fórmulas para obter os valores, quando a fase é de 0 a 7 e quando a fase é 8.
             \n\n-    Como alguns valores de pedra não foram preenchidos, eles foram determinados com base no valor de inde.
             \n\n-    Foi aplicado o Ordinal Encoding nas colunas de recomendação dos avaliadores.
             \n\n-    Foi aplicado o Label Enconding na coluna de recomendação psicologia.
             \n\n-    Foi identificado que na coluna atingiu_ponto_virada não havia valores em algumas linhas. Então os valores faltantes foram preenchidos com base no indicador ipv.
             \n\n-    Na coluna fase ideal foi extraído apenas o número da fase, dentre outros textos.
             \n\n-    As colunas destaque_ieg, destaque_ida e destaque_ipv possuiam algumas linhas sem valores, mas como os possíveis valores eram destaque ou melhorar, os valores faltantes foram alimentados de acordo com a nota dos respectivos indicadores.
             \n\n-    A coluna classificacao_geral tinha valores faltantes, que foram preenchidos com base no ano e a nota inde.
             \n\n-    A coluna classificacao_fase tinha valores faltantes, que foram preenchidos com base no ano, fase e a nota inde.
             \n\n-    A coluna classificacao_turma tinha valores faltantes, que foram preenchidos com base no ano, fase, turma e a nota inde.

    \n\n Por fim o dataframe foi convertido em arquivo .csv que foi utilizado na análise realizada neste projeto Stremlit.
    """)

    st.header("3️⃣ Análises Realizadas")

    df_2022 = df[df["ano"] == 2022]
    df_2023 = df[df["ano"] == 2023]
    df_2024 = df[df["ano"] == 2024]

    analise_descritiva(df_2022, 2022)
    analise_descritiva(df_2023, 2023)
    analise_descritiva(df_2024, 2024)

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

    st.write("A média de valores INDE ao longo dos anos de 2022 a 2024 sofreu uma queda gradativa, mas não muito acentuada com o passar dos anos.")

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

    st.write("A pontuação média dos indicadores de dimensão acadêmica IAN (Indicador de Adequação de Nível), IDA (Indicador de Desempenho Acadêmico) e IEG (Indicador de Engajamento), também sofreu alteração ao longo dos anos, mas com comportamento diferente do indicador geral INDE. \n\nA média de pontuação do indicador IAN foi a única que não sofreu nenhuma queda ao longo dos anos analisados. \n\n Já a média de pontuações dos indicadores IDA e IEG, tiveram comportamentos similares entre si, onde tiveram um leve aumento do ano de 2022 a 2023, mas seguido de queda no ano de 2024.")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="iaa", label="IAA", marker="o")
    sns.lineplot(data=df, x="ano", y="ips", label="IPS", marker="o")
    ax.set_xticks(anos)
    plt.legend(loc='best')
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução dos Indicadores de Dimensão Psicossocial")
    st.pyplot(fig)

    st.write("A pontuação média dos indicadores de dimensão psicossocial IAA (Indicador de Autoavaliação) e IPS (Indicador Psicossocial) tiveram comportamentos similares entre si, com uma queda de aproximadamente 2 pontos de 2022 a 2023, mas seguida de recuperação de aproximadamente 1,5 ponto de 2023 a 2024.")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x="ano", y="ipp", label="IPP", marker="o")
    sns.lineplot(data=df, x="ano", y="ipv", label="IPV", marker="o")
    ax.set_xticks(anos)
    plt.legend(loc='best')
    plt.xlabel("Ano")
    plt.ylabel("Pontuação Média")
    plt.title("Evolução dos Indicadores de Dimensão Psicopedagógica")
    st.pyplot(fig)

    st.write("O comportamento da média dos indicadores de dimensão psicopedagógica IPP (Indicador Psicopedagógico) e IPV (Indicador de Ponto de Virada) foi de aumento do ano de 2022 a 2023, seguido de queda de 2023 a 2024, mas com magnitudes diferentes. \n\n Enquanto que o IPV teve um aumento bastante discreto de 2022 a 2023, sua queda de 2023 a 2024 foi mais acentuada, o indicador IPP teve um aumento significativo de 2022 a 2023, mas seguido de uma queda de 2023 a 2024 mais discreta.")

    qtd_alunos_ano(df)

    st.subheader("📊 Perfil dos alunos Topázio")

     # Análise do perfil dos alunos topázio
    st.subheader(f"🔹 Perfil dos Alunos Topázio de 2022 a 2024")

    df_topazio = df[df['pedra'] == 'topazio']

    indicadores = ["inde", "ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv"]

    # Calculando médias
    media_topazio = df_topazio[indicadores].mean()
    media_geral = df[indicadores].mean()

    # Criando um gráfico de radar
    labels = indicadores
    num_vars = len(labels)

    angles = np.linspace(0,2 * np.pi, num_vars, endpoint=False).tolist()
    media_topazio = np.concatenate((media_topazio, [media_topazio[0]]))
    media_geral = np.concatenate((media_geral, [media_geral[0]]))
    angles += angles[:1]

    col1, col2 = st.columns(2)
    
    with col1: 
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.fill(angles, media_topazio, color="blue", alpha=0.4, label="Topázio")
        ax.fill(angles, media_geral, color="yellow", alpha=0.4, label="Média Geral")

        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        plt.title(f"Perfil dos Alunos Topázio vs Média Geral de 2022 a 2024")
        plt.legend(loc='lower left')
        st.pyplot(fig)

    with col2:
        st.write("Os alunos de perfil Topázio tiveram a média de indicadores no geral aumentada em relação aos alunos de outros perfis, mas com deatque para os indicadores IAA, IEG, IDA e IAN, que tiveram valores com diferença maior em relação aos respectivos indicadores nas outras categorias de alunos.")


    st.subheader("📊 Análise de correlação dos indicadores, ponto de virada e bolsa")

    # Definir as colunas de indicadores
    indicadores = ["atingiu_ponto_virada", "inde", "ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv", "indicado_bolsa"]

    # Calcular a matriz de correlação
    correlacao = df[indicadores].corr()

    col1, col2 = st.columns(2)
    
    with col1:
        # Criar o gráfico de calor (heatmap)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlacao, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)

        plt.title("Mapa de Calor das Correlações entre Indicadores e Ponto de Virada")

        st.pyplot(fig)

    with col2: 
        st.write("De acordo com o mapa de calor, nenhum dos indicadores teve correlação relevante com o fato dos alunos atingirem ou não o ponto de virada, assim como ser indicado para bolsa ou não, no período analisado, de 2022 a 2024. \n\nJá os indicadores ida, ieg, ipp e ipv demonstraram forte relação com o indicador de desempenho INDE.")

    st.subheader("🔍 Identificação de Outliers")

    df["instituicao"] = df.apply(
    lambda row: "publica" if row["instituicao_publica"] == 1 else 
                "privada" if row["instituicao_privada"] == 1 else 
                "nao informado", axis=1
    )

    col1, col2 = st.columns(2)

    with col1:
        # Criando um boxplot para visualizar outliers de INDE por gênero
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x="genero", y="inde", ax=ax, palette="rocket")

        plt.xlabel("Gênero")
        plt.ylabel("INDE")
        plt.title("Distribuição de Outliers de INDE por Gênero")

        # Exibir no Streamlit
        st.pyplot(fig)

        # Criando um boxplot para visualizar outliers de INDE nos alunos que atingiram ou não ponto de virada
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x="atingiu_ponto_virada", y="inde", ax=ax, palette="coolwarm")

        # Ajustando os rótulos do eixo x
        ax.set_xticklabels(["Não", "Sim"])
        plt.xlabel("Atingiu Ponto Virada")
        plt.ylabel("INDE")
        plt.title("Distribuição de Outliers de INDE nos alunos que atingiram ou não ponto de virada")

        # Exibir no Streamlit
        st.pyplot(fig)

    with col2:
        # Criando um boxplot para visualizar outliers de INDE por gênero
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x="instituicao", y="inde", ax=ax, palette="viridis")

        plt.xlabel("Tipo instituição")
        plt.ylabel("INDE")
        plt.title("Distribuição de Outliers de INDE por tipo de instituição")

        # Exibir no Streamlit
        st.pyplot(fig)

        st.write("Ao analisar os outliers do indicador INDE por gênero é possível identificar que tanto no público de alunos do gênero feminino, quanto do masculino, a concentração de alunos que tiveram melhor pontuação no indicador INDE, ficaram entre 6,5 e 8. Enquanto que alunos que requerem atenção, são alunos que ficaram abaixo de 4,5.")
        st.write("Ao analisar os outliers do indicador INDE por instituição de ensino, os alunos que frequentam instituições públicas tiveram um comportamento similar ao analisado em relação ao gênero. Porém nos alunos de instituição privada e de instituições não informadas os valores ficaram muito mais distribuídos, variando de 1 a 8.")
        st.write("Considerando os alunos que atingiram o ponto de virada, perante os alunos que não atingiram, identificamos que nos que atingiram a concentração de pontuação INDE mais altas estão concentrados entre 8 e 9, enquanto que os que não atingiram o ponto de virada a pontuação fica mais concentrada entre 6 e 8.")

    st.header("4️⃣ Conclusões e Recomendações")
    st.write("""
    - O percentual de alunos Topázio aumentou de forma consistente de 2022 a 2024, acumulando um aumento de 13,11 pontos percentuais do inicio ao fim do período analisado (2022 a 2024). 
    - Apesar do INDE ser uma ponderação de diversos indicadores, os que mais demonstraram relação com o mesmo foram o IDA, IEG, IPP e IPV. Sugerindo que alunos que tiram notas mais altas em matemática, português e inglês, que tem maior engajamento com a entrega de tarefas, que é promovido de fase e que tem maior desenvolvimento emocional, conseguem maior destaque sendo classificado com INDE maiores.
    - A indicação de bolsa não esteve fortemente vinculada a nenhum indicador. Mesmo assim, o que teve correlação melhor (0,09) foi o IAN, sugerindo que minimamente os alunos que estão na sua fase adequada tem mais chances de obter uma bolsa.
    - O fato de alunos terem ou não atingido o ponto de virada demonstrou-se que está medianamente vinculado a indicadores IDA, IEG e IPP. O que sugere que dedicar-se a notas altas nas disciplinas matemática, português e inglês, estar engajado com a entrega de tarefas e ser promovido de fase, indicam que há mais chances de atingir o ponto de virada.
    - A Passos Mágicos pode melhorar os programas de acompanhamento para alunos com INDE abaixo de 5.
    """)

    st.markdown("<p style='text-align: right;'>by Laís Santiago Ribeiro - RM356012 - Grupo 67</p>", unsafe_allow_html=True)

def analise_descritiva(df, ano):
    # Contagem dos valores únicos na coluna "pedra"
    percentuais_pedra = df["pedra"].value_counts(normalize=True) * 100
    percentual_ponto_virada = df["atingiu_ponto_virada"].value_counts(normalize=True) * 100
    percentual_indicado_bolsa = df["indicado_bolsa"].value_counts(normalize=True) * 100

    st.subheader(f"📊 Descritiva ano {ano}")
    st.write("""
    - __Média INDE__: {:.2f}
    - __Taxa de Atingimento do Ponto de Virada__: {:.2f}%
    - __Percentual de Alunos Indicados para Bolsa__: {:.2f}%
    - __Percentual de Alunos Pedra Quartzo__: {:.2f}%
    - __Percentual de Alunos Pedra Ágata__: {:.2f}%
    - __Percentual de Alunos Pedra Ametista__: {:.2f}%
    - __Percentual de Alunos Pedra Topázio__: {:.2f}%
    """.format(
        df["inde"].mean(),
        percentual_ponto_virada[1],
        percentual_indicado_bolsa[1],
        percentuais_pedra["quartzo"],
        percentuais_pedra["agata"],
        percentuais_pedra["ametista"],
        percentuais_pedra["topazio"]
    ))


def qtd_alunos_ano(df):
    # Contando a quantidade de alunos por ano
    contagem_por_ano = df["ano"].value_counts().sort_index()

    # Criando o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x=contagem_por_ano.index, y=contagem_por_ano.values, ax=ax, palette="viridis")

    plt.xlabel("Ano")
    plt.ylabel("Quantidade de Alunos")
    plt.title("Quantidade de Alunos por Ano")

    ax.set_yticks(np.arange(0, contagem_por_ano.max() + 100, 100))  
    ax.grid(axis='y', linestyle='--', alpha=0.7)  

    # Exibir no Streamlit
    st.pyplot(fig)

