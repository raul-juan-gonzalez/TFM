# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import pd
import psycopg2
from sqlalchemy import create_engine

#############################################################################
#############################################################################


db = 'mundo_valores'
schema = 'mundo_valores_v'

conn = psycopg2.connect(
    dbname=db,
    user="readuser1",
    password="cebolla0197",
    host="localhost",

)

# Para lanzar SELECTs a postgre y convertir resultado a df
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn) 

#############################################################################
#############################################################################

# 1) QUERY 
# -------------------------------------
query = """

select 

	h.tick,
    acc.empresa as banco,
	extract(YEAR from h.fec_dato) as anio,
    extract(MONTH from h.fec_dato) as mes,
    CAST( extract(YEAR from h.fec_dato) AS TEXT )||'-'||LPAD(CAST( extract(MONTH from h.fec_dato) AS TEXT ),2,'0') as fec_mes,
    
	CAST(sum((h.cierre+h.apertura)/2)/count(*) as NUMERIC(10,2)) as cot_media_anual
    
from mundo_valores_v.hh_historico_cotizacion h

left join mundo_valores_v.dim_acciones acc on acc.tick = h.tick

where h.tick in ('BBVA','CABK','UNI','SABE','BKT','SAN')
      and extract(MONTH from h.fec_dato) in (6,12)
      and extract(YEAR from h.fec_dato) between 2010 and 2023

group by 1,2,3,3,4,5              

"""

# 2) RESULTADO QUERY => EN df 
# -------------------------------------
df = pd.read_sql_query(query, engine)

import matplotlib.pyplot as plt  
import seaborn as sns  

# Crear la gráfica  
plt.figure(figsize=(10, 6))  

# Paleta de colores  
leyenda = {  
    'BBVA': 'blue',  
    'BKT': 'orange',  
    'CABK': 'magenta',  
    'SABE': 'black',
    'SAN': 'red',
    'UNI': 'green' 
}  


# seaborn para generar el gráfico de líneas  
sns.lineplot(data=df, 
             x='fec_mes', 
             y='cot_media_anual', 
             palette=leyenda, 
             hue='tick', 
             marker='.', 
             markersize=15, 
             linestyle='--') 
  
# Opciones del grafico 
plt.xlabel('AÑO')  
plt.ylabel('COTIIZACION MEDIA ANUAL (€)')  
plt.legend(title='BANCA DEL IBEX')  
plt.xticks(rotation=45)
plt.ylim(bottom=0)  
plt.grid()

# Ajustar el gráfico para evitar recortes 
plt.tight_layout()   

# Mostrar la gráfica  
plt.show()  
