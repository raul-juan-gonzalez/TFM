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

with inicio as (
 
    select 
        h.tick,
        min(fec_dato) as fec_inicio
    from ( 
        
        -- fecha minimia de inicio
        select max(fec_dato) as fec_dato_inicio
        from (
        
            select distinct 
                tick,
                min(fec_dato) as fec_dato 
            from mundo_valores_v.hh_historico_cotizacion
            where tick in ('IBEX','BTC','NVDA')
            group by 1
        )
        
    ) aux, mundo_valores_v.hh_historico_cotizacion h
    
    where  h.fec_dato >= aux.fec_dato_inicio and
           h.tick in ('IBEX','BTC','NVDA')
    group by 1
    

), maximos as (

    select 
        h.tick,
        h.fec_dato as fec_cierre_max,
        h.cierre as cierre_maximo_historico
    from (
        select 
            tick,
            max(cierre) as cierre_maximo_historico
        from mundo_valores_v.hh_historico_cotizacion
        where tick in (select tick from inicio)
        group by 1        
    ) aux, mundo_valores_v.hh_historico_cotizacion h
    
    where h.tick = aux.tick and h.cierre = aux.cierre_maximo_historico
    
)
    
    select distinct
    
        i.tick,
        coalesce(acc.empresa,cript.cripto,ind.indice) as valor,
        m.fec_cierre_max,
        m.cierre_maximo_historico,
        i.fec_inicio,
        h.cierre as precio_cierre_inicio,
        CAST( h.cierre/m.cierre_maximo_historico AS NUMERIC(10,5) ) as precio_inicio_normalizado
        
        
    from inicio i
    inner join mundo_valores_v.hh_historico_cotizacion h
    on (h.tick = i.tick and h.fec_dato = i.fec_inicio)
    
    inner join maximos m on m.tick = i.tick
           
    -- para traer los nombres de los valores
    left join mundo_valores_v.dim_acciones acc on acc.tick = i.tick
    left join mundo_valores_v.dim_criptomonedas cript on cript.tick = i.tick
    left join mundo_valores_v.dim_indices ind on ind.tick = i.tick
                  

"""

# 2) RESULTADO QUERY => EN df 
# -------------------------------------
df_parametria = pd.read_sql_query(query, engine)

#############################################################################
#############################################################################

# 1) QUERY 
# -------------------------------------
query = """

with inicio as (
 
    select 
        h.tick,
        min(fec_dato) as fec_inicio
    from ( 
        
        -- fecha minimia de inicio
        select max(fec_dato) as fec_dato_inicio
        from (
        
            select distinct 
                tick,
                min(fec_dato) as fec_dato 
            from mundo_valores_v.hh_historico_cotizacion
            where tick in ('IBEX','BTC','NVDA')
            group by 1
        )
        
    ) aux, mundo_valores_v.hh_historico_cotizacion h
    
    where  h.fec_dato >= aux.fec_dato_inicio and
           h.tick in ('IBEX','BTC','NVDA')
    group by 1
    

), maximos as (

    select 
        tick,
        max(cierre) as cierre_maximo_historico
    from mundo_valores_v.hh_historico_cotizacion 
    where tick in (select tick from inicio)
    group by 1
    
)
    
    select distinct
    
        h.tick,
        coalesce(acc.empresa,cript.cripto,ind.indice) as valor,
        h.fec_dato,
        h.cierre,
        m.cierre_maximo_historico,
        CAST(h.cierre/m.cierre_maximo_historico AS NUMERIC(10,5) ) as precio_cierre_normalizado
        
    from mundo_valores_v.hh_historico_cotizacion h
    inner join maximos m on m.tick = h.tick
        
    -- para traer los nombres de los valores
    left join mundo_valores_v.dim_acciones acc on acc.tick = h.tick
    left join mundo_valores_v.dim_criptomonedas cript on cript.tick = h.tick
    left join mundo_valores_v.dim_indices ind on ind.tick = h.tick
    
    -- inicio del analisis
    where h.fec_dato >= (select min(fec_inicio) from inicio) 
          -- and EXTRACT(YEAR from h.fec_dato) between 2018 and 2023
               

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
    'BITCOIN': 'orange',  
    'IBEX 35': 'blue',  
    'NVIDIA CORPORATION': 'green',  
}  


# Usar seaborn para generar un gráfico de líneas  
sns.lineplot(data=df, 
             x='fec_dato', 
             y='precio_cierre_normalizado', 
             palette=leyenda, 
             hue='valor', 
             marker='o',
             markersize=5)  

# Opciones del grafico   
plt.xlabel('FECHA')  
plt.ylabel('PRECIO DE CIERRE NORMALIZADO')  
plt.legend(title='VALORES')  
plt.xticks(rotation=45)  
plt.ylim(bottom=0)  
plt.grid() 

# Ajustar el gráfico para evitar recortes  
plt.tight_layout()  

# Mostrar la gráfica  
plt.show()  
