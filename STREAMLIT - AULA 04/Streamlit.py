import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Funcionários",
    layout="wide",
    page_icon="")

@st.cache_data
def carregar_dados():
    dados = {
        "nome": ["Beyoncé", "Preta Gil", "Lucas", "Jay-Z", "Aline", "Nivia", "Deyse"],
        "idade": [23, 35, 29, np.nan, 40, 31, 28],
        "cidade": ["SP", "RJ", "SP", "MG", "RJ", "MG", "SP"],
        "salario": [3000, 5000, 4000, 3500, np.nan, 4800, 5200],
        "data_contratacao": pd.to_datetime(["2020-01-10", "2019-05-20", "2021-03-15", "2022-07-01", "2018-11-12", "2020-06-15", "2023-01-20"])
    }
    df = pd.DataFrame(dados)
    
    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())
    
    df["salario_anual"] = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year
    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo")
    return df

df = carregar_dados()

st.sidebar.header("Filtros")

cidades = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df["cidade"].unique(),
    default=df["cidade"].unique())

min_salario = float(df["salario"].min())
max_salario = float(df["salario"].max())
faixa_salario = st.sidebar.slider(
    "Faixa salarial",
    min_salario, max_salario, (min_salario, max_salario))

df_filtrado = df[
    (df["cidade"].isin(cidades)) & 
    (df["salario"].between(faixa_salario[0], faixa_salario[1]))
]

st.title("Análise de Funcionários")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Salário Médio", f"R$ {df_filtrado['salario'].mean():.2f}")
col2.metric("👥 Total Funcionários", len(df_filtrado))
col3.metric("📈 Salário Máximo", f"R$ {df_filtrado['salario'].max():.2f}")

st.divider()

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Média Salarial por Cidade")
    media_cidade = df_filtrado.groupby("cidade")["salario"].mean().reset_index()
    fig1 = px.bar(media_cidade, x="cidade", y="salario", color="cidade")
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    st.subheader("Distribuição por Categoria")
    cat_counts = df_filtrado["categoria_salario"].value_counts().reset_index()
    fig2 = px.pie(cat_counts, names="categoria_salario", values="count", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar CSV Filtrado", data=csv, file_name="dados.csv", mime="text/csv")