import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def show_previsao(df):

    st.title("📊 Previsão de Indicação para Bolsa")

    st.write("Insira os valores dos indicadores para prever se o aluno poderá ser indicado para bolsa:")

    indicadores_previsao = ["idade", "fase", "iaa", "ieg", "ips", "ida", "ipv", "ian", "ipp"]

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
        modelo=cria_modelo(df, indicadores_previsao)

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

    st.markdown("<p style='text-align: right;'>by Laís Santiago Ribeiro - RM356012 - Grupo 67</p>", unsafe_allow_html=True)


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
    acuracia = accuracy_score(y_test, y_pred) * 100
    st.write(f"Acurácia do modelo é de: {acuracia:.2f}%")

    return modelo