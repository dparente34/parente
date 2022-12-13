# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title = 'Reporte de Ventas', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = 'moneybag:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

# Banner de la pagina
from PIL import Image
image = Image.open('banner.jpg')

st.image(image, caption='Reporte Empresarial')

#Streamlit run Ventas.py

tab1, tab2,tab3 = st.tabs(['***ENUNCIADO***','***ANALISIS***','***DATOS & GRAFICAS:bar_chart:***'])

with st.sidebar:

    archivo = st.file_uploader('Seleccionar Archivo',
                                type='xlsx', accept_multiple_files=False)
    if archivo is not None:
        df = pd.read_excel(archivo, usecols='A:F', # Solo cargamos las columnas a Analizar.
                                header=0)
        
    else:
        st.warning('Es Nesesario la Carga del Archivo')
if archivo is None:
        st.warning('')
else:
    with tab1:
        with open('Descripcion.md', 'r') as archivo:
            texto = archivo.read()
        
            st.write(texto)
            st.table(df)

if archivo is None:
        st.warning('')
else:
       
        st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
        vendedor = st.sidebar.multiselect(
        "**Seleccione el Vendedor :man::woman::**",
            options = df['Vendedor'].unique(),
            default = df['Vendedor'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
        )

        status_factura = st.sidebar.multiselect(
            "**Factura Pagada (?):dollar::**",
            options = df['Pagada'].unique(),
            default = df['Pagada'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
        )

        

        cliente = st.sidebar.multiselect(
            "**Seleccione La Empresa:office::**",
            options = df['Cliente'].unique(),
            default = df['Cliente'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
        )

        industria = st.sidebar.multiselect(
            "Seleccione Industria:",
            options = df['Industria'].unique(),
            default = df['Industria'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
        )


with tab2:

    if archivo is None:
        st.warning('') 

    else:
    

    #Conectar los selectores con la base de datos
        df_seleccion = df.query("Vendedor == @vendedor  & Pagada ==@status_factura & Cliente ==@cliente & Industria ==@industria " ) #el primer city es la columna y el segundo es el selector
    

        st.title(':clipboard: Reporte de Ventas') #Titulo
        st.subheader('Compañía PARENTE')
        #st.markdown('##') #Para separar el titulo
        st.markdown("---")

        total_ventas = int(df_seleccion['Valor'].sum())

        total_facturas = int(df_seleccion['Valor'].count())

        left_column, right_column = st.columns(2)

        with left_column:
                st.subheader("Ventas Totales:")
                st.subheader(f"US $ {total_ventas:,}")

        with right_column:
                st.subheader('Facturas:')
                st.subheader(f" {total_facturas}")
            
        st.dataframe(df_seleccion)

        nuevo_archivo = io.BytesIO()
        df_seleccion.to_excel(nuevo_archivo)
        st.download_button('Descargar Planilla', data=nuevo_archivo, file_name= 'NuevoReporte.xlsx')


    
        ventas_por_cliente = (df_seleccion.groupby(by=['Cliente'])[['Valor']].sum('Valor')
    )
        ventas_por_vendedor = (df_seleccion.groupby(by=['Vendedor'])[['Valor']].sum('Valor')
    )

st.markdown("---") 
  
#FORMA COLUMNAS PARA LOS GRAFICOS
if archivo is None:
        st.warning('') 

else:
    with tab3:
        st.markdown('##')
        col1, col2 = st.columns(2)

        with col1:
            st.write('**VENTAS POR EMPRESA (DATOS)**',ventas_por_cliente)

        with col2:
            st.write('**VENTAS POR EMPRESA (GRAFICO)**')
            st.line_chart(ventas_por_cliente)

        st.markdown('##')
        st.markdown('##')


        col1, col2 = st.columns(2)
        with col1:
            st.write('**VENTAS POR VENDEDOR (DATOS)**',ventas_por_vendedor)

        with col2:
            st.write('**VENTAS POR VENDEDOR (GRAFICO)**')
            st.line_chart(ventas_por_vendedor)
        st.markdown("---")
        st.markdown('##')
        st.write('**RELACION COMERCIAL VENDEDORES-EMPRESAS**')
        st.markdown('##')
        st.bar_chart(data=df_seleccion, x='Cliente', y='Vendedor')
    