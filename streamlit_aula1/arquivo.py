import streamlit as st
import pandas as pd

st.write("Olá, mundo")


nome = "Davi Augusto"
idade = 18


st.title("Meu primeiro dash")
st.subheader(nome)


st.write("Meu nome é", nome, "e eu tenho", idade, "anos")


df = pd.DataFrame({
    'Matéria': ['Português', 'Matemática', 'Python', 'Frame'],
    'Nota': [5, 9, 7, 10]
})


st.write(df)