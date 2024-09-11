# -*- coding: utf-8 -*-
"""
@author: Raul
"""

import psycopg2
from PROC_construccion_tablas import *

#############################################################################
#############################################################################

conn = psycopg2.connect(
    dbname='mundo_valores',
    user="postgres",
    password="cebolla0197",
    host="localhost",
)

# cur = conn.cursor()
# conn.commit()
# conn.close()

#############################################################################
#############################################################################

if inicializacion:
    # carga inicial de la BD
    schema = 'mundo_valores_v'
else:
    # procesos de actualizacion
    schema = 'mundo_valores_act'
    # Borramos antes de cargar lo nuevo
    query = """
        DELETE FROM mundo_valores_act.sdim_valores;
        DELETE FROM mundo_valores_act.sdim_mercados;
        DELETE FROM mundo_valores_act.tdc_pais;
        DELETE FROM mundo_valores_act.dim_bolsa_valores;
        DELETE FROM mundo_valores_act.dim_exchange_cripto;
        DELETE FROM mundo_valores_act.hh_historico_cotizacion;
        DELETE FROM mundo_valores_act.dim_divisas;
        DELETE FROM mundo_valores_act.dim_FIs;
        DELETE FROM mundo_valores_act.dim_criptomonedas;
        DELETE FROM mundo_valores_act.h_cripto_emisiones;
        DELETE FROM mundo_valores_act.tdc_industria;
        DELETE FROM mundo_valores_act.tdc_sector;;
        DELETE FROM mundo_valores_act.tdc_estados;
        DELETE FROM mundo_valores_act.dim_acciones;
        DELETE FROM mundo_valores_act.h_acc_dividendos;
        DELETE FROM mundo_valores_act.h_estados_contables;
        DELETE FROM mundo_valores_act.dim_indices;
        DELETE FROM mundo_valores_act.dim_ETFs;   
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()  
    cursor.close()  

#############################################################################
#############################################################################

def carga(schema,tabla,campos,df):
    
    global conn
    # para interactuar con postgreSQL
    cursor = conn.cursor()
    
    vals = '%s,'*len(campos.split(','))
    values = 'VALUES ('+vals[:-1]+')'

    
    for index, row in df.iterrows():
        query = 'INSERT INTO '+schema+'.'+tabla+' '+campos+' '+values 
        fila = tuple(row)
        cursor.execute(query, fila)
    conn.commit()
    cursor.close()  

#############################################################################
#############################################################################

ini = time()

# -------------------------------------
# CATALGOs
# -------------------------------------
campos = '(tipo_valor,tick,fec_carga)'
carga(schema=schema,tabla='sdim_valores',campos=campos,df=SDIM_VALORES)

campos = '(tipo_mercado,tipo_bolsa,cod_bolsa,fec_carga)'
carga(schema=schema,tabla='sdim_mercados',campos=campos,df=SDIM_MERCADOS)

# -------------------------------------
# TDCs
# -------------------------------------
campos = '(exchange,cod_exchange,year_fundacion,regulacion,comision_media,metodos_pago,variedad_catalogo,seguridad,tipo_servicios,soporte_cliente,fec_carga)'
carga(schema=schema,tabla='dim_exchange_cripto',campos=campos,df=DIM_EXCHANGE_CRIPTO)

campos = '(cod_pais,pais,country,continente,cod_moneda,moneda,cod_region,region,fec_carga)'
carga(schema=schema,tabla='tdc_pais',campos=campos,df=TDC_PAIS)

campos = '(bolsa,bolsa_integrada,cod_bolsa_integrada,cod_region,fec_carga)'
carga(schema=schema,tabla='dim_bolsa_valores',campos=campos,df=DIM_BOLSA_VALORES)

campos = '(cod_industria,industria,fec_carga)'
carga(schema=schema,tabla='tdc_industria',campos=campos,df=TDC_INDUSTRIA)

campos = '(cod_sector,sector,fec_carga)'
carga(schema=schema,tabla='tdc_sector',campos=campos,df=TDC_SECTOR)

campos = '(cod_sector,estado_contable,cod_magnitud,magnitud,fec_carga)'
carga(schema=schema,tabla='tdc_estados',campos=campos,df=TDC_ESTADOS)

# -------------------------------------
# DIMs
# -------------------------------------
campos = '(tick, divisa,fec_carga)'
carga(schema=schema,tabla='dim_divisas',campos=campos,df=DIM_DIVISAS)

campos = '(tick,indice,cod_bolsa,cod_pais_referencia,fec_carga)'
carga(schema=schema,tabla='dim_indices',campos=campos,df=DIM_INDICES)

campos = '(tick,fi,isin,emisor,cod_pais_emisor,tipo_valor_subyacente,categoria,rating_morningstar,fec_carga)'
carga(schema=schema,tabla='dim_fis',campos=campos,df=DIM_FIs)

campos = '(tick,etf,isin,emisor,tipo_valor_subyacente,subyacente,fec_carga)'
carga(schema=schema,tabla='dim_etfs',campos=campos,df=DIM_ETFs)

campos = '(tick,cripto,fec_carga)'
carga(schema=schema,tabla='dim_criptomonedas',campos=campos,df=DIM_CRIPTOMONEDAS)

campos = '(tick,empresa,sede,cod_pais_sede,cod_industria,cod_sector,fec_carga)'
carga(schema=schema,tabla='dim_acciones',campos=campos,df=DIM_ACCIONES)

# -------------------------------------
# HISTORICOS
# -------------------------------------
campos = '(fec_dato,dia_semana,tick,oferta_actual,oferta_maxima,fec_carga)'
carga(schema=schema,tabla='h_cripto_emisiones',campos=campos,df=H_CRIPTO_EMISIONES)

campos = '(tick,fec_dividendo,dividendo,fec_carga)'
carga(schema=schema,tabla='h_acc_dividendos',campos=campos,df=H_ACC_DIVIDENDOS)

campos = '(par,tick,cod_bolsa,fec_dato,dia_semana,cierre,apertura,maximo,minimo,vol_negociado,var_porcentual,fec_carga)'
carga(schema=schema,tabla='hh_historico_cotizacion',campos=campos,df=HH_HISTORICO_COTIZACION)

campos = '(tick,cod_sector,anio,periodo,cod_magnitud,valor_magnitud,fec_carga)'
carga(schema=schema,tabla='h_estados_contables',campos=campos,df=H_ESTADOS_CONTABLES)

fin = time()
# Cerramos la conexión finalmente
conn.close

print('')
print('Tiempo de carga de las tablas: ' + str((fin-ini)/60) + ' minutos')


#############################################################################
#############################################################################

codigo = """

cols = ['TICK','FEC_DIVIDENDO']
duplicados = H_CRIPTO_EMISIONES[H_CRIPTO_EMISIONES.duplicated(subset='TICK', keep='first')]  

cols = ['PAR','COD_BOLSA','FEC_DATO']
groups = [col for col in cols if col != 'FEC_DATO']

fechas_maximas = H_HISTORICO.groupby(by=groups,as_index=False).agg('max')
valor = H_HISTORICO.loc[H_HISTORICO['PAR'] == 'BBVA/EUR']
check = H_HISTORICO.loc[H_HISTORICO['FECHA'] == date(2019,8,2)]

"""

#############################################################################
#############################################################################

del campos,codigo

