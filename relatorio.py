import streamlit as st

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
    """)

    st.header("3️⃣ Análises Realizadas")

    st.subheader("📊 Descritiva")
    st.write("""
    - **Média INDE**: {:.2f}
    - **Taxa de Atingimento do Ponto de Virada**: {:.2f}%
    - **Percentual de Alunos Indicados para Bolsa**: {:.2f}%
    - **Taxa de Formatura**: {:.2f}%
    """.format(
        df["inde"].mean(),
        df["atingiu_ponto_virada"].mean() * 100,
        df["indicado_bolsa"].mean() * 100,
        df["formado"].mean() * 100
    ))

    st.subheader("🔍 Identificação de Outliers")
    st.write("Os alunos com melhor desempenho têm um **INDE maior que 8.5**, enquanto os que necessitam de atenção apresentam **INDE abaixo de 5**.")

    st.subheader("🤖 Predição")
    st.write("Utilizamos regressão linear para prever o desempenho futuro dos alunos com base em seus indicadores.")

    st.header("4️⃣ Conclusões e Recomendações")
    st.write("""
    - Alunos com engajamento (IEG) maior tendem a ter melhor desempenho.
    - A recomendação de bolsa está fortemente relacionada ao ponto de virada.
    - A Passos Mágicos pode melhorar os programas de acompanhamento para alunos com INDE abaixo de 5.
    """)

