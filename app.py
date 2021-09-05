import streamlit as st
import datetime
import pandas as pd
import psycopg2

# --- INTRODUÇÃO ---
st.title('Interagindo com o Banco de Dados')
st.subheader('Usando o Streamlit para inserir dados para no banco de dados')

texto_intro1 = '''
Uma das etapas fundamentais em um produto de dados é a obtenção dos dados, a qual muitas vezes é feita via coleta dos dados. Este aplicativo web em Streamlit exemplifica uma maneira de se fazer isso.
'''

st.write(texto_intro1)

texto_intro2 ='''
Em resumo, este aplicativo irá (1) acessar o banco de dados que você já criou com suas credenciais, (2) inserir os dados e (3) acessar a tabela no banco.
''' 
st.write(texto_intro2)

st.info('**Fique tranquilo**, suas credenciais do banco de dado _NÃO_ serão coletadas. Você pode checar o código deste aplicativo no arquivo app.py em https://github.com/rknagao/artigo_sql')


# --- PARTE 1 ---
st.header('Parte 1 - Credenciais do banco de dados')

HOST = st.text_input("Insira o 'Host'")
HOST = HOST.replace(" ", "")
DBNAME = st.text_input("Insira o 'Database'")
DBNAME = DBNAME.replace(" ", "")
USER = st.text_input("Insira o 'User'")
USER = USER.replace(" ", "")
PORT = st.text_input("Insira o 'Port'")
PORT = PORT.replace(" ", "")
PASSWORD = st.text_input("Insira o 'Password'")
PASSWORD = PASSWORD.replace(" ", "")


# --- PARTE 2 ---
st.header('Parte 2 - Dados a serem coletados')
st.markdown('_**Sobre o famoso quadro abaixo...**_')

st.image('caravaggio.jpg', caption='Não vale pesquisar no Google!')

resp_opiniao = st.select_slider('O que você achou da obra?', options=['odiei','não gostei','indiferente','gostei', 'amei'], value='indiferente')
resp_preco = st.slider('Quantos milhões de doláres você acha custa a obra original?', min_value=0, max_value=100)


# --- 2 FUNÇÕES SQL: as coisas mais importantes deste script
#documentação https://www.psycopg.org/docs/module.html

def interagir_sql(query):
    #objetivo: criar tabela ou inserir dados 
    conn = psycopg2.connect(dbname=DBNAME,
                            user = USER,
                            password = PASSWORD,
                            host = HOST,
                            port = PORT)   
    cur = conn.cursor()
    cur.execute(query)
    cur.close
    conn.commit()
    conn.close()


def obter_tabela_sql(query):
    #objetivo: criar tabela ou inserir dados 
    conn = psycopg2.connect(dbname=DBNAME,
                            user = USER,
                            password = PASSWORD,
                            host = HOST,
                            port = PORT)   
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns=['data','opiniao','preco'])
    cur.close
    conn.commit()
    conn.close()
    return df


# --- SALVANDO DADOS NO BANCO ---

if st.button('Enviar os dados'):

    #criando a tabela sql
    try:
        query1 = '''CREATE TABLE IF NOT EXISTS tabela_arte(
                    data VARCHAR,
                    opiniao VARCHAR,
                    preco INT
                    );
        '''

        interagir_sql(query1)
        st.write("Sucesso: a tabela 'tabela_arte' foi criada.")
    except:
        st.write('Erro: não foi possível criar a tabela')

    #inserindo os dados na tabela
    try:
        query2 = f'''INSERT INTO tabela_arte (data, opiniao, preco)
                    VALUES ('{datetime.datetime.now().strftime('%d-%m-%Y')}', '{resp_opiniao}', {resp_preco});
        '''

        interagir_sql(query2)

        st.info(f'''**Dados enviados**:\n
            1) O que você achou da obra? {resp_opiniao}\n
            2) Quantos milhões de dólares você acha que é o preço da obra original? {resp_preco}
            ''')
    except:
        st.write('Erro: não foi possível inserir os dados na base.')


    # --- PARTE 3 ---
st.header('Parte 3 - Acessar a tabela SQL')

df = obter_tabela_sql('SELECT * FROM tabela_arte')
st.write(df)
