# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import pd,datetime,time
from clase_Entorno import Entorno
# HISTORICOS
from clase_Historico import Historico
from clase_Dividendos import Dividendos
from clase_Estados import Estados
# DIM_VALORES
from clase_Valores import Valores

# Construccion de las tablas segun JSONs de PRODUCCION
e = Entorno(headless=False,act=True)

#############################################################################
#############################################################################

import psycopg2
from sqlalchemy import create_engine

conn = psycopg2.connect(
    dbname='mundo_valores',
    user="postgres",
    password="cebolla0197",
    host="localhost",
)

# Para lanzar SELECTs a postgre y convertir resultado a df
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn) 

#############################################################################
# 1) H_ESTADOS_CONTABLES
#############################################################################

# 1) Obtencion de min(fec_dividendo_max) 
# -------------------------------------
query = """
-- fecha minima de las fechas más actuales de cada tick
select  min(anio_max) as anio_min
from (
	select
		TICK,
        COD_SECTOR,
        PERIODO,
		max(anio) as anio_max
	from mundo_valores_v.h_estados_contables
	group by 1,2,3
)
"""

df = pd.read_sql_query(query, engine)
anio_min = str(df.iloc[0, 0]).split('-')
anio_min = [int(v) for v in anio_min]

# 2) Obtencion de los ticks) 
# ----------------------------

query = """
select distinct TICK from mundo_valores_v.h_estados_contables
"""
df = pd.read_sql_query(query, engine)
ticks = df['tick']
ticks = ticks.tolist()

# 3) Lanzamos la construcción del histórico
# -----------------------------------------

ini = time()

est = Estados(entorno=e)
H_ESTADOS_CONTABLES = est.construccion_historico()
H_ESTADOS_CONTABLES['FEC_CARGA'] = datetime.now()

fin = time()

print('')
print('Tiempo de construcción de H_ESTADOS_CONTABLES: ' + str((fin-ini)/60) + ' minutos')
del ini,fin

#############################################################################
# 2) H_ACC_DIVIDENDOS
#############################################################################

# 1) Obtencion de min(fec_dividendo_max) 
# -------------------------------------
query = """
-- fecha minima de las fechas más actuales de cada tick
select  min(fec_dividendo_max) as fec_dividendo_min
from (
	select
		TICK,
		max(fec_dividendo) as fec_dividendo_max
	from mundo_valores_v.h_acc_dividendos
	group by 1
)
"""

df = pd.read_sql_query(query, engine)
fec_dividendo_min = str(df.iloc[0, 0]).split('-')
fec_dividendo_min = [int(v) for v in fec_dividendo_min]

# 2) Obtencion de los ticks) 
# ----------------------------

query = """
select distinct TICK from mundo_valores_v.h_acc_dividendos
-- ****************************************************
"""
df = pd.read_sql_query(query, engine)
ticks = df['tick']
ticks = ticks.tolist()

# 3) Lanzamos la construcción del histórico
# -----------------------------------------

ini = time()

d = Dividendos(entorno=e)
H_ACC_DIVIDENDOS = d.construccion_historico(fec_dato=fec_dividendo_min,ticks=ticks)
H_ACC_DIVIDENDOS['FEC_CARGA'] = datetime.now()

fin = time()

print('')
print('Tiempo de construcción de H_ACC_DIVIDENDOS: ' + str((fin-ini)/60) + ' minutos')

#############################################################################
# 3) H_HISTORICO
#############################################################################

# 1) Obtencion de min(fec_dato_max)) 
# -------------------------------------

query = """
-- fecha minima de las fechas más actuales de cada tick
select  min(fec_dato_max) as fec_dato_min
from (
	select
		TICK,
		max(fec_dato) as fec_dato_max
	from mundo_valores_v.hh_historico_cotizacion
	group by 1
)
"""
df = pd.read_sql_query(query, engine)
fec_dato_min = str(df.iloc[0, 0]).split('-')
fec_dato_min = [int(v) for v in fec_dato_min]

# 2) Obtencion de los ticks) 
# ----------------------------

query = """
select distinct TICK from mundo_valores_v.hh_historico_cotizacion
-- ****************************************************
"""
df = pd.read_sql_query(query, engine)
ticks = df['tick']
ticks = ticks.tolist()

# 3) Lanzamos la construcción del histórico
# -----------------------------------------

ini = time()

h = Historico(entorno=e)
H_HISTORICO = h.construccion_historico(fec_dato=fec_dato_min,ticks=ticks)
H_HISTORICO['FEC_CARGA'] = datetime.now()

fin = time()
# Cerramos la conexión finalmente
conn.close

print('')
print('Tiempo de construcción de H_HISTORICO: ' + str((fin-ini)/60) + ' minutos')

#############################################################################
# 4) DIM_VALORES
#############################################################################

ini = time()

# e.act = True
v = Valores(entorno=e)
for k,valor in enumerate(e.mis_valores):
    
    globals()[e.mis_tablas_dim[k]] = v.dim_info(tipo_valor=valor)
    globals()[e.mis_tablas_dim[k]]['FEC_CARGA'] = datetime.now()

fin = time()

print('')
print('Tiempo de construcción de las tablas DIM_: ' + str((fin-ini)/60) + ' minutos')
del ini,fin,k,v,valor
