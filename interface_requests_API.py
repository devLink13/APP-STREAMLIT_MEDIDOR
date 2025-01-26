import requests
import pandas as pd
import json
import streamlit as st
from io import StringIO

URL_DATES_AVAILABLES = "http://127.0.0.1:5000/availabledates"
URL_GET_DATAFRAME_BYDATE = "http://127.0.0.1:5000/getDatabaseByDates/"


@st.cache_data
def get_datesAvailables():

    response = requests.get(URL_DATES_AVAILABLES)
    json_str = response.text
    json_io = StringIO(json_str)

    dates = pd.read_json(json_io)

    dates["dates_availables"] = pd.to_datetime(dates['dates_availables']).dt.date

    # pegando a series com as datas
    series_dates = dates['dates_availables']

    return series_dates

@st.cache_data
def get_dataframe_from_selectDate(select_date):
    url = URL_GET_DATAFRAME_BYDATE + select_date
    response = requests.get(url=url)

    # pega o json da requisição, é necessário usar o atributo .text para que a string json
    # formatada pela funcao json.dumps() não seja convertida automaticamente para uma lista pela biblioteca resquests
    # isso causaria um erro e quebraria o código.
    json = response.text

    # apenas retornar o json
    return json


if __name__ == "__main__":
    get_datesAvailables()
