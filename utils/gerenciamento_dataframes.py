from io import StringIO
import pandas as pd
import streamlit as st

@st.cache_data
def json2dataframe(json):
    json_io = StringIO(json)
    dataframe = pd.read_json(json_io)

    # criar uma coluna padrão datetime (isso facilitará a manipulação dos dados temporais)
    # concatenar as colunas de data e horarios
    dataframe['datetime'] = dataframe['data'] + ' ' + dataframe['horario']
    # converter a coluna para um objeto datetime formatado
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'], format='%d/%m/%Y %H:%M:%S')

    return dataframe

def seriesTensoes(dataframe):
    series = dataframe[['tensao_A', 'tensao_B', 'tensao_C', 'datetime']].copy()
    
    # manipular os valores de tensao
    series['tensao_A'] = series['tensao_A'] / 10
    series['tensao_B'] = series['tensao_B'] / 10
    series['tensao_C'] = series['tensao_C'] / 10

    # criar uma nova coluna para hora e uma nova coluna para data
    horas = series['datetime'].dt.time
    datas = series['datetime'].dt.date

    series['hora'] = horas
    series['data'] = datas

    return series


if __name__ == '__main__':
    pass



