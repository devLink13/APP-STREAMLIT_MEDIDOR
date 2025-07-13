import streamlit as st
import pandas as pd
import plotly.express as px


from interface_requests_API import get_datesAvailables, get_dataframe_from_selectDate
from utils.gerenciamento_dataframes import json2dataframe, seriesTensoes

st.set_page_config(page_title='DASH BOARD',
                   layout="wide",
                   initial_sidebar_state='collapsed',
                   )


# configurando a sidebar
with st.sidebar:
    st.sidebar.title('MENU DE NAVEGAÇÃO')

    if st.button("LOGIN"):
        st.switch_page("login.py")

    if st.button("PRINCIPAL"):
        st.switch_page("main.py")

    st.sidebar.button('TENSOES')
    st.sidebar.button('CORRENTES')

# TITULO DA PÁGINA
st.header('ANÁLISE DE TENSÕES')
st.markdown('<hr style="margin: 1px 0;">', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

container = st.container(border=True)
with container:
    st.markdown('### Gerenciamento de datas')

    # pegando as datas do banco de dados ---> falta implementar ainda
    option_dates = get_datesAvailables()

    # selecionar a data de análise
    dia_selecionado = st.selectbox(
        'Selecione uma data para análise:', options=option_dates)

    # converter dia selecionado de hora.date para str para passar para a funcao
    # get_dataframe_from_selectDate
    dia_selecionado = str(dia_selecionado)

    # pega o json contendo todo o datafram do dia selecionado
    json = get_dataframe_from_selectDate(dia_selecionado)

    # converte o json string em um objeto dataframe
    dataframe = json2dataframe(json)

    # horas disponíveis
    horas_disponiveis = dataframe['datetime'].dt.time

    # slider para selecao do período
    periodo_selecionado = st.slider('Selecione o Período de Análise:',
                                    min_value=horas_disponiveis.min(),
                                    max_value=horas_disponiveis.max(),
                                    value=(horas_disponiveis.min(),
                                           horas_disponiveis.max()),
                                    step=pd.Timedelta(minutes=1))

st.markdown('<hr style="margin: 1px 0;">', unsafe_allow_html=True)

periodo_selecionado_minimo = min(periodo_selecionado)
periodo_selecionado_maximo = max(periodo_selecionado)

#####################################################################################################################
series_tensoes = seriesTensoes(dataframe)

# Filtrar os dados com base no período selecionado
filtro_periodos = series_tensoes[(series_tensoes['hora'] >= periodo_selecionado_minimo) & (
    series_tensoes['hora'] <= periodo_selecionado_maximo)]
tensoes_filtrado = filtro_periodos


# filtrando as médias das tensões
v_media = (tensoes_filtrado['tensao_A'].mean(
) + tensoes_filtrado['tensao_B'].mean() + tensoes_filtrado['tensao_C'].mean()) / 3
va_med = tensoes_filtrado['tensao_A'].mean()
vb_med = tensoes_filtrado['tensao_B'].mean()
vc_med = tensoes_filtrado['tensao_C'].mean()

# definindo layout
col1, col2, col3 = st.columns(3)

# plotando a tensao A
with col1:
    state_vmedA = st.toggle('Habilitar valor médio',
                            label_visibility='visible', key='v_medA')

fig_tensaoA = px.line(tensoes_filtrado, x="hora",
                      y="tensao_A", title="TENSAO A x HORAS")
fig_tensaoA.update_xaxes(nticks=5)
if state_vmedA:
    fig_tensaoA.add_scatter(x=tensoes_filtrado['hora'], y=([va_med]*len(tensoes_filtrado)), mode='lines',
                            name='TENSAO MÉDIA VA', showlegend=False, line={'color': 'red'})
col1.plotly_chart(fig_tensaoA, use_container_width=True,
                  config={'displayModeBar': False})

with col2:
    state_vmedB = st.toggle('Habilitar valor médio',
                            label_visibility='visible', key='v_medB')
# plotando a tensao B
fig_tensaoB = px.line(tensoes_filtrado, x="hora",
                      y="tensao_B", title="TENSAO B x HORAS")
fig_tensaoB.update_xaxes(nticks=5)
if state_vmedB:
    fig_tensaoB.add_scatter(x=tensoes_filtrado['hora'], y=([vb_med]*len(tensoes_filtrado)), mode='lines',
                            name='TENSAO MÉDIA VB', showlegend=False, line={'color': 'red'})
col2.plotly_chart(fig_tensaoB, use_container_width=True,
                  config={'displayModeBar': False})

with col3:
    state_vmedC = st.toggle('Habilitar valor médio',
                            label_visibility='visible', key='v_medC')
# plotando a tensao C
fig_tensaoC = px.line(tensoes_filtrado, x="hora",
                      y="tensao_C", title="TENSAO C x HORAS")
fig_tensaoC.update_xaxes(nticks=5)
if state_vmedC:
    fig_tensaoC.add_scatter(x=tensoes_filtrado['hora'], y=([vc_med]*len(tensoes_filtrado)), mode='lines',
                            name='TENSAO MÉDIA VC', showlegend=False, line={'color': 'red'})
col3.plotly_chart(fig_tensaoC, use_container_width=True,
                  config={'displayModeBar': False})


# plotando as tres tensoes e adicionando filtros

# filtrando os valores de pico e mínimo de tensão na FASE A
pico_tensaoA = max(tensoes_filtrado['tensao_A'])
min_tensaoA = min(tensoes_filtrado['tensao_A'])


hora_picoTensaoA = tensoes_filtrado['hora'][tensoes_filtrado['tensao_A']
                                            == pico_tensaoA].unique()
hora_picoTensaoA_inicio = hora_picoTensaoA[0]
hora_picoTensaoA_fim = hora_picoTensaoA[-1]

hora_valeTensaoA = tensoes_filtrado['hora'][tensoes_filtrado['tensao_A']
                                            == min_tensaoA].unique()
hora_valeTensaoA_inicio = hora_valeTensaoA[0]
hora_valeTensaoA_fim = hora_valeTensaoA[-1]

# filtrando os valores de pico e minimo de tensão na FASE B
pico_tensaoB = max(tensoes_filtrado['tensao_B'])
min_tensaoB = min(tensoes_filtrado['tensao_B'])

hora_picoTensaoB = tensoes_filtrado['hora'][tensoes_filtrado['tensao_B']
                                            == pico_tensaoB].unique()
hora_picoTensaoB_inicio = hora_picoTensaoB[0]
hora_picoTensaoB_fim = hora_picoTensaoB[-1]

hora_valeTensaoB = tensoes_filtrado['hora'][tensoes_filtrado['tensao_B']
                                            == min_tensaoB].unique()
hora_valeTensaoB_inicio = hora_valeTensaoB[0]
hora_valeTensaoB_fim = hora_valeTensaoB[-1]

# filtrando os valores de pico e minimo de tensão na FASE C
pico_tensaoC = max(tensoes_filtrado['tensao_C'])
min_tensaoC = min(tensoes_filtrado['tensao_C'])

hora_picoTensaoC = tensoes_filtrado['hora'][tensoes_filtrado['tensao_C']
                                            == pico_tensaoC].unique()
hora_picoTensaoC_inicio = hora_picoTensaoC[0]
hora_picoTensaoC_fim = hora_picoTensaoC[-1]

hora_valeTensaoC = tensoes_filtrado['hora'][tensoes_filtrado['tensao_C']
                                            == min_tensaoC].unique()
hora_valeTensaoC_inicio = hora_valeTensaoC[0]
hora_valeTensaoC_fim = hora_valeTensaoC[-1]

# iniciando os plots
fig_tensoes = px.line(tensoes_filtrado, x="hora",
                      y=["tensao_A", "tensao_B", "tensao_C"],
                      title="TENSOES x HORAS")
fig_tensoes.update_yaxes(title='TENSOES (V)')
fig_tensoes.update_xaxes(nticks=13, ticks='inside', showspikes=True)
fig_tensoes.add_scatter(mode='markers', x=[hora_picoTensaoA_inicio, hora_picoTensaoB_inicio, hora_picoTensaoC_inicio],
                        y=[pico_tensaoA, pico_tensaoB, pico_tensaoC], text=[
                            'Maior pico de tensão Va', 'Maior pico de tensão Vb', 'Maior pico de tensão Vc'],
                        marker={'color': 'red', 'size': 11}, showlegend=False)
fig_tensoes.add_scatter(mode='markers', x=[hora_valeTensaoA_inicio, hora_valeTensaoB_inicio, hora_valeTensaoC_inicio],
                        y=[min_tensaoA, min_tensaoB, min_tensaoC], text=[
                            'Maior pico de tensão Va', 'Maior pico de tensão Vb', 'Maior pico de tensão Vc'],
                        marker={'color': 'yellow', 'size': 11}, showlegend=False)

# criar uma lista com o comprimento de df_filtrado para criar uma linha horizontal que será a média
lista_medias_tensoes = [v_media]*len(tensoes_filtrado)
fig_tensoes.add_scatter(
    x=tensoes_filtrado['hora'], y=lista_medias_tensoes, mode='lines', name='TENSAO MÉDIA DAS 3 FASES')
tab1, tab2 = st.tabs(['Gráfico (Tensão x Tempo)', 'Tabela de Dados'])

with tab1:
    st.plotly_chart(fig_tensoes, use_container_width=True,
                    config={'displayModeBar': False})

with tab2:

    st.dataframe(tensoes_filtrado, use_container_width=True, hide_index=True)


# check box para ver imagens detalhadas
state_toggle = st.toggle('Ver analises gráficas detalhadas?')

if state_toggle:
    str_help = ('Você deve selecionar uma fase por vez para obter as análises gráficas da tensão em funcão'
                'do tempo.')

    select = st.selectbox('Selecione uma fase para obter as análises gráficas', [
                          'FASE A', 'FASE B', 'FASE C'], index=0, help=str_help)

    if select == 'FASE A':
        # :cor[texto]
        st.info(f'O pico de tensao de :red[{pico_tensaoA}V] ocorreu em {
                hora_picoTensaoA_inicio} e manteve até {hora_picoTensaoA_fim}.')
        st.info(f'O menor valor de tensao foi :orange[{min_tensaoA}V] ocorreu em {
                hora_valeTensaoA_inicio} e manteve até {hora_valeTensaoA_fim}.')

    if select == 'FASE B':
        st.info(f'O pico de tensao de :red[{pico_tensaoB}V] ocorreu em {
                hora_picoTensaoB_inicio} e manteve até {hora_picoTensaoB_fim}.')
        st.info(f'O menor valor de tensao foi :orange[{min_tensaoB}V] ocorreu em {
                hora_valeTensaoB_inicio} e manteve até {hora_valeTensaoB_fim}.')

    if select == 'FASE C':
        st.info(f'O pico de tensao de :red[{pico_tensaoC}V]  ocorreu em {
                hora_picoTensaoC_inicio} e manteve até {hora_picoTensaoC_fim}.')
        st.info(f'O menor valor de tensao foi :orange[{min_tensaoC}V] ocorreu em {
                hora_valeTensaoC_inicio} e manteve até {hora_valeTensaoC_fim}.')


st.markdown('<br><br>', unsafe_allow_html=True)


st.write(f"### RESUMO DOS DADOS NO PERÍODO DE {
         periodo_selecionado_minimo} a {periodo_selecionado_maximo}")
st.markdown('<hr style="margin: 1px 0;">', unsafe_allow_html=True)


container2 = st.container(border=True)
with container2:
    col4, col5 = st.columns(2)
    with col4:
        st.markdown(f'- MÉDIA DA TENSAO A: {va_med:.2f}V')
        st.write(f'* MÉDIA DA TENSAO B: {vb_med:.2f}V')
        st.write(f'* MÉDIA DA TENSAO C: {vc_med:.2f}V')

    with col5:
        st.write(f'* MÉDIA DAS TENSÕES: {v_media:.2f}V')
