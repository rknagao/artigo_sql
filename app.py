import streamlit as st
import datetime
import pandas as pd


#PARTE 1 - INTRODUÇÃO
st.title('Interagindo com o Banco de Dados')
st.subheader('Usando o Streamlit para inserir dados para no banco de dados')

texto_intro1 = '''
Uma das etapas fundamentais em um produto de dados é a obtenção dos dados, a qual muitas vezes é feita via coleta dos dados. Este aplicativo web em Streamlit exemplifica uma maneira de se fazer isso.
'''

st.write(texto_intro1)

texto_intro2 ='''
Em resumo, este aplicativo irá (1) acessar o banco de dados que você já criou com suas credenciais e (2) inserir os dados.
''' 
st.write(texto_intro2)


path = st.text_input('Insira seu nome aqui')

df = pd.DataFrame()
if path:
    st.write(datetime.datetime.now())
    st.write(path)