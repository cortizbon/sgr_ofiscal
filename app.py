import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# seteo de la configuración de la página

st.set_page_config(layout='wide')

# lectura de datos

sgr_fia = pd.read_csv('datasets/sgr_fia.csv')
sgr_func = pd.read_csv('datasets/sgr_func.csv')
sgr_miner = pd.read_csv('datasets/sgr_miner_2.csv')
sgr_hidroc = pd.read_csv('datasets/sgr_hidroc.csv')
sgr_regal_comp = pd.read_csv('datasets/sgr_regal_tot.csv')

# titulo

st.title("Sistema General de Regalías")

tab1, tab2 = st.tabs(['Recaudo', 'Asignación'])

# varios tabs

with tab1:
    st.header("Composición del recaudo")

    st.dataframe(sgr_regal_comp)


    x=sgr_regal_comp['Periodo']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=sgr_regal_comp['Minería %'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one',
        name = "Minería %" # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=x, y=sgr_regal_comp['Hidrocarburos %'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one',
        name = "Hidrocarburos"
    ))


    fig.update_layout(yaxis_range=(0, 1))
    st.plotly_chart(fig)


# tab de ingreso 

# Subdivisión de hidrocarburos y minerales

# gráfico de área de la composición de ingreso por hidrocarburos y por minerales

# gráfico como porcentaje del PIB
# descarga de datos

# Subdivisión de hidrocarburos
    st.header("Composición de los hidrocarburos")

    st.dataframe(sgr_hidroc)
    x=sgr_hidroc['Periodo'].unique().tolist()

    t = (sgr_hidroc
    .groupby('Periodo')[['RECAUDO POR GAS\n$COP', 
                        'RECAUDO POR CRUDO (ESPECIE Y MONETIZADO) $COP']]
    .sum()
    .assign(total= lambda x: x[['RECAUDO POR GAS\n$COP', 
                        'RECAUDO POR CRUDO (ESPECIE Y MONETIZADO) $COP']].sum(axis=1)))

    t = t[['RECAUDO POR GAS\n$COP','RECAUDO POR CRUDO (ESPECIE Y MONETIZADO) $COP']].div(t['total'], axis=0).rename(columns={'RECAUDO POR GAS\n$COP': "Gas %",
                                                                                                                         'RECAUDO POR CRUDO (ESPECIE Y MONETIZADO) $COP': "Petróleo %"})
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=t['Gas %'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one',
        name="Gas %" # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=x, y=t['Petróleo %'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one',
        name='Petróleo %'
    ))


    fig.update_layout(yaxis_range=(0, 1))
    st.plotly_chart(fig)


# gráfico de área de la composición de hidrocarburos
# gráfico como porcentaje del PIB
# descarga de datos

# Subdivisión de minerales
    st.header("Composición de los minerales")

    st.dataframe(sgr_miner)

    per = st.select_slider("Seleccione un periodo", sgr_miner['Periodo'].unique().tolist())

    sgr_miner_per = sgr_miner[sgr_miner['Periodo'] == per]
    fig = px.treemap(sgr_miner_per,
                     path=[px.Constant("Total regalías mineras"),
                           "Departamento",
                           "Municipio",
                           "clasificacion",
                           "Recurso Natural"],
                    values='Regalías causadas')
    st.plotly_chart(fig)

# gráfico de área de la composición de minerales
# gráfico como porcentaje del PIB
# descarga de datos

# Mapa de extracción de minerales por departamento

# descarga de datos

# tab de gasto

with tab2:

# Subdivisión de funcionamiento
    st.header("Funcionamiento")
    per = st.select_slider("Seleccione un periodo: ", sgr_func['Periodo'].unique().tolist())
    sgr_func_per = sgr_func[sgr_func['Periodo'] == per]
    st.dataframe(sgr_func_per)

    fig = px.treemap(sgr_func_per, 
                     path=[px.Constant("Total funcionamiento"), "Beneficiario", "Beneficiario 2"],
                     values="Apropiación vigente disponible",
                     title="Apropiación vigente disponible")

    st.plotly_chart(fig)
    
    fig = px.treemap(sgr_func_per, 
                     path=[px.Constant("Total funcionamiento"), "Beneficiario", "Beneficiario 2"],
                     values="Caja total",
                     title='Caja total')

    st.plotly_chart(fig)


# Subdivisón de ahorro
    st.header("Ahorro")

    ahorro = sgr_fia[sgr_fia['CONCEPTO 1'] == 'AHORRO']
    st.dataframe(ahorro)
    fig = px.bar(ahorro, x='Periodo', y='Instrucción de abono a cuenta', color='CONCEPTO 2')
    st.plotly_chart(fig)



# Subdivisón de inversión

    st.header("Inversión")

    inv = sgr_fia[sgr_fia['CONCEPTO 1'] == 'INVERSIÓN']
    st.dataframe(inv)
    fig = px.bar(inv, x='Periodo', y='Instrucción de abono a cuenta', color='CONCEPTO 2')
    st.plotly_chart(fig)    
