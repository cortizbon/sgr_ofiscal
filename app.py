import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# seteo de la configuración de la página

st.set_page_config(layout='wide')

# lectura de datos

sgr_fia = pd.read_csv('datasets/sgr_fia.csv')
sgr_func = pd.read_csv('datasets/sgr_func.csv')
sgr_miner = pd.read_csv('datasets/sgr_miner_opt.csv')
sgr_hidroc = pd.read_csv('datasets/sgr_hidroc_opt.csv')
sgr_regal_comp = pd.read_csv('datasets/comp_rec.csv')
sgr_proy = pd.read_csv('datasets/proyectos.csv')
sgr_cont = pd.read_csv('datasets/contratos.csv')

# titulo

st.title("Sistema General de Regalías")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Recaudo', 'Asignación', 'Proyectos', 'Contratos', 'Proyectos sectorizados', 'Scatters'])

# varios tabs

with tab1:
    st.header("Composición del recaudo")

    st.dataframe(sgr_regal_comp)


    x=sgr_regal_comp['Periodo']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=sgr_regal_comp['% miner'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one',
        name = "Minería %" # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=x, y=sgr_regal_comp['% hidroc'],
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
    x = sgr_hidroc['Periodo'].unique().tolist()

    t = (sgr_hidroc
    .groupby('Periodo')[['recaudo_gas_pc', 
                        'recaud_crudo_em_pc']]
    .sum()
    .assign(total= lambda x: x[['recaudo_gas_pc', 
                        'recaud_crudo_em_pc']].sum(axis=1)))

    t = t[['recaudo_gas_pc','recaud_crudo_em_pc']].div(t['total'], axis=0).rename(columns={'recaudo_gas_pc': "Gas %",
                                                                                                                         'recaud_crudo_em_pc': "Petróleo %"})
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

    sgr_miner_per = sgr_miner[sgr_miner['Periodo'] == per].groupby('clasificacion')['regalias_causadas_pc'].sum().reset_index()
    fig = px.treemap(sgr_miner_per,
                     path=[px.Constant("Total recaudo minero"),
                           "clasificacion"],
                    values='regalias_causadas_pc')
    st.plotly_chart(fig)

    prov_piv = sgr_miner.pivot_table(index='clasificacion',
                          columns='Periodo',
                          values='regalias_causadas_pc',
                          aggfunc='sum')
    
   
    sol = prov_piv.div(prov_piv.sum(axis=0), axis=1).unstack().reset_index().rename(columns={0:'%'})
    fig = px.area(sol, x='Periodo', y='%', color='clasificacion')

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

    ahorro = sgr_fia[sgr_fia['CONCEPTO 1'] == 'AHORRO'].pivot_table(index=['Periodo', 'CONCEPTO 2'],
                                                                    values='Instrucción de abono a cuenta',
                                                                    aggfunc='sum').reset_index()
    st.dataframe(ahorro)
    fig = px.bar(ahorro, x='Periodo', y='Instrucción de abono a cuenta', color='CONCEPTO 2')
    st.plotly_chart(fig)



# Subdivisón de inversión

    st.header("Inversión")

    inv = sgr_fia[sgr_fia['CONCEPTO 1'] == 'INVERSIÓN'].pivot_table(index=['Periodo', 'CONCEPTO 2'],
                                                                    values='Instrucción de abono a cuenta',
                                                                    aggfunc='sum').reset_index()
    st.dataframe(inv)
    fig = px.bar(inv, x='Periodo', y='Instrucción de abono a cuenta', color='CONCEPTO 2')
    st.plotly_chart(fig)    

with tab3:

    st.header("Por año")

    piv_sum_tot_an = sgr_proy.groupby(['AÑO APROBACIÓN'])['total_proyecto_pc'].sum().reset_index()
    piv_sum_tot_per = sgr_proy.groupby(['Periodo'])['total_proyecto_pc'].sum().reset_index()
    st.dataframe(piv_sum_tot_an)
    st.dataframe(piv_sum_tot_per)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Por año", "Por bienio"))

    # Add the first line plot to the first subplot
    fig.add_trace(go.Scatter(x=piv_sum_tot_an['AÑO APROBACIÓN'], 
                             y=piv_sum_tot_an['total_proyecto_pc'], 
                             mode='lines', 
                             name='Por año'), row=1, col=1)

    # Add the second line plot to the second subplot
    fig.add_trace(go.Scatter(x=piv_sum_tot_per['Periodo'], 
                             y=piv_sum_tot_per['total_proyecto_pc'], 
                             mode='lines', 
                             name='Por bienio'), row=1, col=2)

    # Customize the layout
    fig.update_layout(
        title="Valor total de los proyectos por año y bienio",
        template="plotly_white" # Hide legend if not needed
    )

    # Show the figure
    st.plotly_chart(fig)

    piv_count_tot_an = sgr_proy.groupby(['AÑO APROBACIÓN'])['total_proyecto_pc'].count().reset_index()
    piv_count_tot_per = sgr_proy.groupby(['Periodo'])['total_proyecto_pc'].count().reset_index()
    st.dataframe(piv_count_tot_an)
    st.dataframe(piv_count_tot_per)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Por año", "Por bienio"))

    # Add the first line plot to the first subplot
    fig.add_trace(go.Scatter(x=piv_count_tot_an['AÑO APROBACIÓN'], 
                             y=piv_count_tot_an['total_proyecto_pc'], 
                             mode='lines', 
                             name='Por año'), row=1, col=1)

    # Add the second line plot to the second subplot
    fig.add_trace(go.Scatter(x=piv_count_tot_per['Periodo'], 
                             y=piv_count_tot_per['total_proyecto_pc'], 
                             mode='lines', 
                             name='Por bienio'), row=1, col=2)

    # Customize the layout
    fig.update_layout(
        title="Número de proyectos por año y bienio",
        template="plotly_white" # Hide legend if not needed
    )

    # Show the figure
    st.plotly_chart(fig)

    piv_mean_tot_an = sgr_proy.groupby(['AÑO APROBACIÓN'])['total_proyecto_pc'].mean().reset_index()
    piv_mean_tot_per = sgr_proy.groupby(['Periodo'])['total_proyecto_pc'].mean().reset_index()
    st.dataframe(piv_mean_tot_an)
    st.dataframe(piv_mean_tot_per)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Por año", "Por bienio"))

    # Add the first line plot to the first subplot
    fig.add_trace(go.Scatter(x=piv_mean_tot_an['AÑO APROBACIÓN'], 
                             y=piv_mean_tot_an['total_proyecto_pc'], 
                             mode='lines', 
                             name='Por año'), row=1, col=1)

    # Add the second line plot to the second subplot
    fig.add_trace(go.Scatter(x=piv_mean_tot_per['Periodo'], 
                             y=piv_mean_tot_per['total_proyecto_pc'], 
                             mode='lines', 
                             name='Por bienio'), row=1, col=2)

    # Customize the layout
    fig.update_layout(
        title="Valor promedio de los proyectos por año y bienio",
        template="plotly_white" # Hide legend if not needed
    )

    # Show the figure
    st.plotly_chart(fig)

    st.header("Por año y por departamento")

    st.subheader("Cantidad de proyectos")



    # heatmap de número de proyectos por departamento y por año

    piv_dc_an = sgr_proy.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='AÑO APROBACIÓN',
                        values='total_proyecto_pc',
                        aggfunc='count')
    
    piv_dc_per = sgr_proy.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='Periodo',
                        values='total_proyecto_pc',
                        aggfunc='count')
    
    st.dataframe(piv_dc_an)
    fig = px.imshow(piv_dc_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_dc_per)

    fig = px.imshow(piv_dc_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    
    st.subheader("Valor total de los proyectos")
    piv_ds_an = sgr_proy.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='AÑO APROBACIÓN',
                        values='total_proyecto_pc',
                        aggfunc='sum')
    
    piv_ds_per = sgr_proy.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='Periodo',
                        values='total_proyecto_pc',
                        aggfunc='sum')
    
    st.dataframe(piv_ds_an)
    fig = px.imshow(piv_ds_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_ds_per)
    fig = px.imshow(piv_ds_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

    st.subheader("Valor promedio de cada proyecto")
    
    piv_dm_an = sgr_proy.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='AÑO APROBACIÓN',
                        values='total_proyecto_pc',
                        aggfunc='mean')
    
    piv_dm_per = sgr_proy.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='Periodo',
                        values='total_proyecto_pc',
                        aggfunc='mean')

    st.dataframe(piv_dm_an)
    fig = px.imshow(piv_dm_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_dm_per)
    fig = px.imshow(piv_dm_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

    # métricas con desfases

    # descarga de datos

    for col in ['FECHA INICIO PROGRAMACIÓN INICIAL', 'FECHA FINAL PROGRAMACIÓN INICIAL',
           'FECHA INICIO PROGRAMACIÓN ACTUAL', 'FECHA FINAL PROGRAMACIÓN ACTUAL']:
        sgr_proy[col] = pd.to_datetime(sgr_proy[col])
    

    fechas = sgr_proy[['DEPARTAMENTO EJECUTOR','AÑO APROBACIÓN', 'Periodo','FECHA INICIO PROGRAMACIÓN INICIAL', 'FECHA FINAL PROGRAMACIÓN INICIAL',
           'FECHA INICIO PROGRAMACIÓN ACTUAL', 'FECHA FINAL PROGRAMACIÓN ACTUAL']]
    
    st.subheader("Desfase en fechas de inicio")
    
    fechas['DESFASE FECHA INICIO'] = fechas['FECHA INICIO PROGRAMACIÓN ACTUAL'] - fechas['FECHA INICIO PROGRAMACIÓN INICIAL']
    a = fechas[fechas['DESFASE FECHA INICIO'] == pd.to_timedelta(0)].groupby('AÑO APROBACIÓN')['DESFASE FECHA INICIO'].count()
    b = fechas[fechas['DESFASE FECHA INICIO'] > pd.to_timedelta(0)].groupby('AÑO APROBACIÓN')['DESFASE FECHA INICIO'].count()
    c = fechas[fechas['DESFASE FECHA INICIO'] < pd.to_timedelta(0)].groupby('AÑO APROBACIÓN')['DESFASE FECHA INICIO'].count()

    tab = pd.concat([a, b, c], axis=1)
    tab.columns = ['A TIEMPO', 'APLAZADO', 'ADELANTADO']
    tab = tab.div(tab.sum(axis=1), axis=0)
    tab = tab.unstack().reset_index(name='num_proyectos')
    tab.columns = ['cat', 'año', 'num_proyectos']

    fig = px.area(tab, x='año', y='num_proyectos', color='cat')

    st.plotly_chart(fig)

    st.subheader("Número de proyectos con fecha de inicio aplazada por departamento")

    fechas['APLAZADA'] = fechas['DESFASE FECHA INICIO'] > pd.to_timedelta(0)

    piv_fi = fechas.pivot_table(index='DEPARTAMENTO EJECUTOR',
                                columns='AÑO APROBACIÓN',
                                values='APLAZADA',
                                aggfunc='mean')

    fig = px.imshow(piv_fi, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

    fechas['DESFASE FECHA FINAL'] = fechas['FECHA FINAL PROGRAMACIÓN ACTUAL'] - fechas['FECHA FINAL PROGRAMACIÓN INICIAL']
    a = fechas[fechas['DESFASE FECHA FINAL'] == pd.to_timedelta(0)].groupby('AÑO APROBACIÓN')['DESFASE FECHA FINAL'].count()
    b = fechas[fechas['DESFASE FECHA FINAL'] > pd.to_timedelta(0)].groupby('AÑO APROBACIÓN')['DESFASE FECHA FINAL'].count()
    c = fechas[fechas['DESFASE FECHA FINAL'] < pd.to_timedelta(0)].groupby('AÑO APROBACIÓN')['DESFASE FECHA FINAL'].count()

    st.subheader("Desfase en fechas de finalización")

    tab = pd.concat([a, b, c], axis=1)
    tab.columns = ['A TIEMPO', 'APLAZADO', 'ADELANTADO']
    tab = tab.div(tab.sum(axis=1), axis=0)
    tab = tab.unstack().reset_index(name='num_proyectos')
    tab.columns = ['cat', 'año', 'num_proyectos']

    fig = px.area(tab, x='año', y='num_proyectos', color='cat')

    st.plotly_chart(fig)


    st.subheader("Número de proyectos con fecha de finalización aplazada por departamento")

    fechas['APLAZADA'] = fechas['DESFASE FECHA FINAL'] > pd.to_timedelta(0)

    piv_fi = fechas.pivot_table(index='DEPARTAMENTO EJECUTOR',
                                columns='AÑO APROBACIÓN',
                                values='APLAZADA',
                                aggfunc='mean')

    fig = px.imshow(piv_fi, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

with tab4:
    st.header("Por año")

    piv_sum_tot_an = sgr_cont.groupby(['AÑO APROBACIÓN'])['total_contrato_pc'].sum().reset_index()
    piv_sum_tot_per = sgr_cont.groupby(['Periodo'])['total_contrato_pc'].sum().reset_index()
    st.dataframe(piv_sum_tot_an)
    st.dataframe(piv_sum_tot_per)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Por año", "Por bienio"))

    # Add the first line plot to the first subplot
    fig.add_trace(go.Scatter(x=piv_sum_tot_an['AÑO APROBACIÓN'], 
                             y=piv_sum_tot_an['total_contrato_pc'], 
                             mode='lines', 
                             name='Por año'), row=1, col=1)

    # Add the second line plot to the second subplot
    fig.add_trace(go.Scatter(x=piv_sum_tot_per['Periodo'], 
                             y=piv_sum_tot_per['total_contrato_pc'], 
                             mode='lines', 
                             name='Por bienio'), row=1, col=2)

    # Customize the layout
    fig.update_layout(
        title="Valor total de los contratos por año y bienio",
        template="plotly_white" # Hide legend if not needed
    )

    # Show the figure
    st.plotly_chart(fig)

    piv_count_tot_an = sgr_cont.groupby(['AÑO APROBACIÓN'])['total_contrato_pc'].count().reset_index()
    piv_count_tot_per = sgr_cont.groupby(['Periodo'])['total_contrato_pc'].count().reset_index()
    st.dataframe(piv_count_tot_an)
    st.dataframe(piv_count_tot_per)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Por año", "Por bienio"))

    # Add the first line plot to the first subplot
    fig.add_trace(go.Scatter(x=piv_count_tot_an['AÑO APROBACIÓN'], 
                             y=piv_count_tot_an['total_contrato_pc'], 
                             mode='lines', 
                             name='Por año'), row=1, col=1)

    # Add the second line plot to the second subplot
    fig.add_trace(go.Scatter(x=piv_count_tot_per['Periodo'], 
                             y=piv_count_tot_per['total_contrato_pc'], 
                             mode='lines', 
                             name='Por bienio'), row=1, col=2)

    # Customize the layout
    fig.update_layout(
        title="Número de contratos por año y bienio",
        template="plotly_white" # Hide legend if not needed
    )

    # Show the figure
    st.plotly_chart(fig)

    piv_mean_tot_an = sgr_cont.groupby(['AÑO APROBACIÓN'])['total_contrato_pc'].mean().reset_index()
    piv_mean_tot_per = sgr_cont.groupby(['Periodo'])['total_contrato_pc'].mean().reset_index()
    st.dataframe(piv_mean_tot_an)
    st.dataframe(piv_mean_tot_per)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Por año", "Por bienio"))

    # Add the first line plot to the first subplot
    fig.add_trace(go.Scatter(x=piv_mean_tot_an['AÑO APROBACIÓN'], 
                             y=piv_mean_tot_an['total_contrato_pc'], 
                             mode='lines', 
                             name='Por año'), row=1, col=1)

    # Add the second line plot to the second subplot
    fig.add_trace(go.Scatter(x=piv_mean_tot_per['Periodo'], 
                             y=piv_mean_tot_per['total_contrato_pc'], 
                             mode='lines', 
                             name='Por bienio'), row=1, col=2)

    # Customize the layout
    fig.update_layout(
        title="Valor promedio de los contrato por año y bienio",
        template="plotly_white" # Hide legend if not needed
    )

    # Show the figure
    st.plotly_chart(fig)

    st.header("Por año y por departamento")

    st.subheader("Cantidad de contratos")



    # heatmap de número de proyectos por departamento y por año

    piv_dc_an = sgr_cont.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='AÑO APROBACIÓN',
                        values='total_contrato_pc',
                        aggfunc='count')
    
    piv_dc_per = sgr_cont.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='Periodo',
                        values='total_contrato_pc',
                        aggfunc='count')
    
    st.dataframe(piv_dc_an)
    fig = px.imshow(piv_dc_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_dc_per)

    fig = px.imshow(piv_dc_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    
    st.subheader("Valor total de los proyectos")
    piv_ds_an = sgr_cont.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='AÑO APROBACIÓN',
                        values='total_contrato_pc',
                        aggfunc='sum')
    
    piv_ds_per = sgr_cont.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='Periodo',
                        values='total_contrato_pc',
                        aggfunc='sum')
    
    st.dataframe(piv_ds_an)
    fig = px.imshow(piv_ds_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_ds_per)
    fig = px.imshow(piv_ds_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

    st.subheader("Valor promedio de cada contrato")
    
    piv_dm_an = sgr_cont.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='AÑO APROBACIÓN',
                        values='total_contrato_pc',
                        aggfunc='mean')
    
    piv_dm_per = sgr_cont.pivot_table(index='DEPARTAMENTO EJECUTOR',
                        columns='Periodo',
                        values='total_contrato_pc',
                        aggfunc='mean')

    st.dataframe(piv_dm_an)
    fig = px.imshow(piv_dm_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_dm_per)
    fig = px.imshow(piv_dm_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

    depto = st.selectbox("Seleccione un departamento: ", sgr_cont['DEPARTAMENTO EJECUTOR'].unique().tolist())
    fil_depto = sgr_cont[sgr_cont['DEPARTAMENTO EJECUTOR'] == depto]
    piv_depto = fil_depto.groupby('NOMBRE CONTRATISTA')['total_contrato_pc'].sum().sort_values(ascending=False).reset_index().head(10)

    fig = px.bar(piv_depto, x='NOMBRE CONTRATISTA',y='total_contrato_pc')
    st.plotly_chart(fig)

    piv_depto = fil_depto.groupby('NOMBRE CONTRATISTA')['total_contrato_pc'].count().sort_values(ascending=False).reset_index().head(10)

    fig = px.bar(piv_depto, x='NOMBRE CONTRATISTA',y='total_contrato_pc')
    st.plotly_chart(fig)

with tab5:
    st.header("Por año y por sector")

    st.subheader("Cantidad de proyectos")



    # heatmap de número de proyectos por departamento y por año

    piv_dc_an = sgr_proy.pivot_table(index='SECTOR SUIFP',
                        columns='AÑO APROBACIÓN',
                        values='total_proyecto_pc',
                        aggfunc='count')
    
    piv_dc_per = sgr_proy.pivot_table(index='SECTOR SUIFP',
                        columns='Periodo',
                        values='total_proyecto_pc',
                        aggfunc='count')
    
    st.dataframe(piv_dc_an)
    fig = px.imshow(piv_dc_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_dc_per)

    fig = px.imshow(piv_dc_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    
    st.subheader("Valor total de los proyectos")
    piv_ds_an = sgr_proy.pivot_table(index='SECTOR SUIFP',
                        columns='AÑO APROBACIÓN',
                        values='total_proyecto_pc',
                        aggfunc='sum')
    
    piv_ds_per = sgr_proy.pivot_table(index='SECTOR SUIFP',
                        columns='Periodo',
                        values='total_proyecto_pc',
                        aggfunc='sum')
    
    st.dataframe(piv_ds_an)
    fig = px.imshow(piv_ds_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_ds_per)
    fig = px.imshow(piv_ds_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

    st.subheader("Valor promedio de cada proyecto")
    
    piv_dm_an = sgr_proy.pivot_table(index='SECTOR SUIFP',
                        columns='AÑO APROBACIÓN',
                        values='total_proyecto_pc',
                        aggfunc='mean')
    
    piv_dm_per = sgr_proy.pivot_table(index='SECTOR SUIFP',
                        columns='Periodo',
                        values='total_proyecto_pc',
                        aggfunc='mean')

    st.dataframe(piv_dm_an)
    fig = px.imshow(piv_dm_an, text_auto=True, aspect="auto")

    st.plotly_chart(fig)
    st.dataframe(piv_dm_per)
    fig = px.imshow(piv_dm_per, text_auto=True, aspect="auto")

    st.plotly_chart(fig)

with tab6:

    # numero de proyectos vs. valor medio departamento
    piv_1 = (sgr_proy
             .groupby(['Periodo', 'SECTOR SUIFP'])
             .agg({'total_proyecto_pc':['count','mean']})
             .reset_index())
    piv_1.columns = ['Periodo', 'SECTOR', 'num_proyectos', 'valor_promedio_proy']
    st.dataframe(piv_1)
    fig = px.scatter(piv_1,
                     x='num_proyectos',
                     y='valor_promedio_proy', hover_data=['Periodo', 'SECTOR', 'num_proyectos', 'valor_promedio_proy'])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)
    piv_2 = (sgr_proy
             .groupby(['Periodo', 'DEPARTAMENTO EJECUTOR'])
             .agg({'total_proyecto_pc':['count','mean']})
             .reset_index())
    piv_2.columns = ['Periodo', 'Departamento', 'num_proyectos', 'valor_promedio_proy']
    st.dataframe(piv_2)
    fig = px.scatter(piv_2,
                     x='num_proyectos',
                     y='valor_promedio_proy',
                     hover_data=['Periodo', 'Departamento', 'num_proyectos', 'valor_promedio_proy'])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

    
    
    



    # numero de proyectos vs. valor medio sector

