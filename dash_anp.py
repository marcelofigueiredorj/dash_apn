import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "database_anp.xlsx",
        engine= "openpyxl",
        sheet_name="Planilha1",
        usecols="A:Q",
        nrows=21404
    )
    return df
df = gerar_df()
colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

with st.sidebar:
    st.subheader('PRODUTIVIDADE 1000%')
    logo_teste = Image.open ('logo.png')
    st.image(logo_teste, use_column_width=True)
    st.subheader('SELEÇÃO DE FILTROS')
    fProduto = st.selectbox(
        "Selecione o combustivel:",
        options=df['PRODUTO'].unique()
    )

    fEstado = st.selectbox(
        "Selecione o Estado:",
        options= df['ESTADO'].unique()
    )

    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) &
        (df['ESTADO'] == fEstado)
    ]

updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y%b')
dadosUsuario['MÊS'] = updateDatas[0:]

st.header('PREÇOS DOS COMBUTÍVEIS NO BRASIL: 2013 À 2024')
st.markdown('**Combutível selecionado:** ' + fProduto)
st.markdown('**Estado:** ' + fEstado)

grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color='red', size=20)
).encode(
    x = alt.X('MÊS', title='Mês'),
    y = alt.Y('PREÇO MÉDIO REVENDA', title='Preço Médio Revenda'),
    strokeWidth = alt.value(3)
).properties(
    height = 700,
    width = 1400,
)
st.altair_chart(grafCombEstado)
