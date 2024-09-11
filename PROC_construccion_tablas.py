# -*- coding: utf-8 -*-
"""
@author: Raul
"""

# inicializacion = True  => carga inicial
# inicializacion = False => procesos de actualizacion
inicializacion = False

#############################################################################
#############################################################################

from clase_Entorno import time,date,pd
from clase_Entorno import Entorno

# Simplemente para traernos variables globales
e = Entorno()
mis_variables = e.mis_variables
mis_tablas_dim = e.mis_tablas_dim
del e

#############################################################################
#                           TRAEMOS DATAFRAMES
#############################################################################

ini = time()

if inicializacion:
    
    from H_historico_cotizaciones import H_HISTORICO
    from H_estados_contables import H_ESTADOS_CONTABLES
    from H_acc_dividendos import H_ACC_DIVIDENDOS
    from DIM_valores import DIM_ACCIONES,DIM_CRIPTOMONEDAS,DIM_ETFs,DIM_FIs,DIM_DIVISAS,DIM_INDICES
          
else:
    
    from PROC_tablas_act import H_ESTADOS_CONTABLES,H_ACC_DIVIDENDOS,H_HISTORICO
    from PROC_tablas_act import DIM_ACCIONES,DIM_CRIPTOMONEDAS,DIM_ETFs,DIM_FIs,DIM_DIVISAS,DIM_INDICES
    
# resto
from TDC_sector_industria import TDC_INDUSTRIA,TDC_SECTOR
from DIM_exchange_cripto import DIM_EXCHANGE_CRIPTO
from DIM_bolsa_valores import TDC_PAIS,DIM_BOLSA_VALORES

#############################################################################
#                        CODIFICACION TABLAS DIM
#############################################################################

# 1) Codificamos las bolsas
# -------------------------
for tabla in mis_tablas_dim:
    
    # print('CODIFICANDO TABLA ' + tabla + ' ....')
    if tabla in ['DIM_ACCIONES','DIM_INDICES','DIM_ETFs']:
        
        cols = globals()[tabla].columns.tolist()
        cols.append('COD_BOLSA_INTEGRADA')
        # Traemos dos columnas => cruzamos region con cod_bolsa_integrada y bolsa con cod_bolsa_integrada
        aux = pd.merge(globals()[tabla], DIM_BOLSA_VALORES[['COD_BOLSA_INTEGRADA','REGION']].drop_duplicates(), left_on='BOLSA', right_on='REGION', how='left')
        aux = aux[cols]
        aux = pd.merge(aux, DIM_BOLSA_VALORES[['COD_BOLSA_INTEGRADA']].drop_duplicates(), left_on='BOLSA', right_on='COD_BOLSA_INTEGRADA', how='left')
        # Juntamos columnas cod_bolsa_integrada's para contruir cod_bolsa final
        aux['COD_BOLSA'] = aux['COD_BOLSA_INTEGRADA_x'].fillna(aux['COD_BOLSA_INTEGRADA_y'])
        globals()[tabla] = aux[['COD_BOLSA' if col == 'BOLSA' else col for col in globals()[tabla].columns.tolist()]]
        
        if tabla == 'DIM_INDICES':
            aux = pd.merge(globals()[tabla], TDC_PAIS[['COD_PAIS','PAIS']].drop_duplicates(), left_on='PAIS_REFERENCIA', right_on='PAIS', how='left')
            aux['COD_PAIS_REFERENCIA'] = aux['COD_PAIS']
            globals()[tabla] = aux[['COD_PAIS_REFERENCIA' if col == 'PAIS_REFERENCIA' else col for col in globals()[tabla].columns.tolist()]]
            
    elif tabla == 'DIM_FIs':
        
        aux = pd.merge(globals()[tabla], TDC_PAIS[['REGION','COD_PAIS']].drop_duplicates(), left_on='BOLSA', right_on='REGION', how='left')
        aux['COD_PAIS_EMISOR'] = aux['COD_PAIS']
        globals()[tabla] = aux[['COD_PAIS_EMISOR' if col == 'BOLSA' else col for col in globals()[tabla].columns.tolist()]]

    elif tabla == 'DIM_CRIPTOMONEDAS':
        
        aux = pd.merge(globals()[tabla], DIM_EXCHANGE_CRIPTO[['EXCHANGE','COD_EXCHANGE']].drop_duplicates(), left_on='BOLSA', right_on='EXCHANGE', how='left')
        globals()[tabla] = aux[['COD_EXCHANGE' if col == 'BOLSA' else col for col in globals()[tabla].columns.tolist()]]
                
    else:
        
        None
        
# Codificamos dim_acciones
# -------------------------

#   -> correcciones de TDC_SECTOR antes de cruce
cambios = ['FINANCIERAS','FINANCIEROS']
TDC_SECTOR.loc[TDC_SECTOR['SECTOR'].isin(cambios), 'SECTOR'] = 'FINANCIERO'
DIM_ACCIONES.loc[DIM_ACCIONES['SECTOR'].isin(['FINANCIERAS','FINANCIEROS']), 'SECTOR'] = 'FINANCIERO'

cols = DIM_ACCIONES.columns.tolist()
DIM_ACCIONES = pd.merge(DIM_ACCIONES,TDC_SECTOR[['COD_SECTOR','SECTOR']].drop_duplicates(),on='SECTOR',how='left')
DIM_ACCIONES = DIM_ACCIONES[[col if col != 'SECTOR' else 'COD_SECTOR' for col in cols]]

#   -> correcciones de TDC_INDUSTRIA antes de cruce
cambios = ['GAS DE PETROLEO','PETROLEO DE GAS','GAS Y PETROLEO']
TDC_INDUSTRIA.loc[TDC_INDUSTRIA['INDUSTRIA'].isin(cambios), 'INDUSTRIA'] = 'PETROLEO Y GAS'
DIM_ACCIONES.loc[DIM_ACCIONES['INDUSTRIA'].isin(cambios), 'INDUSTRIA'] = 'PETROLEO Y GAS'

cols = DIM_ACCIONES.columns.tolist()
DIM_ACCIONES = pd.merge(DIM_ACCIONES,TDC_INDUSTRIA[['COD_INDUSTRIA','INDUSTRIA']].drop_duplicates(),on='INDUSTRIA',how='left')
DIM_ACCIONES = DIM_ACCIONES[[col if col != 'INDUSTRIA' else 'COD_INDUSTRIA' for col in cols]]

# renombramos PAIS_SEDE para codificacion 
DIM_ACCIONES.loc[DIM_ACCIONES['PAIS_SEDE'] == 'UNITED STATES', 'PAIS_SEDE'] = 'UNITED STATES OF AMERICA'

# aux = DIM_ACCIONES
# DIM_ACCIONES = aux
cols = DIM_ACCIONES.columns.tolist()
DIM_ACCIONES = pd.merge(DIM_ACCIONES,TDC_PAIS[['COUNTRY','COD_PAIS']].drop_duplicates(),left_on='PAIS_SEDE',right_on='COUNTRY')
DIM_ACCIONES.rename(columns={'COD_PAIS': 'COD_PAIS_SEDE'}, inplace=True)  
DIM_ACCIONES = DIM_ACCIONES[[col if col != 'PAIS_SEDE' else 'COD_PAIS_SEDE' for col in cols]]

# Preparamos tablas DIM_* para carga
# ---------------------------------

cols = ['TICK','INDICE','COD_BOLSA','COD_PAIS_REFERENCIA','FEC_CARGA']
DIM_INDICES = DIM_INDICES[cols].drop_duplicates()
cols = ['TICK','FI','ISIN','EMISOR','COD_PAIS_EMISOR','TIPO_VALOR_SUBYACENTE','CATEGORIA','RATING_MORNINGSTAR','FEC_CARGA']
DIM_FIs = DIM_FIs[cols].drop_duplicates()
cols = ['TICK','ETF','ISIN','EMISOR','TIPO_VALOR_SUBYACENTE','SUBYACENTE','FEC_CARGA']
DIM_ETFs = DIM_ETFs[cols].drop_duplicates()
cols = ['TICK','EMPRESA','SEDE','COD_PAIS_SEDE','COD_INDUSTRIA','COD_SECTOR','FEC_CARGA']
DIM_ACCIONES = DIM_ACCIONES[cols]
# DIM_CRIPTOMONEDAS
# DIM_DIVISAS
       
#############################################################################
#                            H_HISTORICO
#############################################################################

# Primero construimos los catalogos antes de adaptar las columnas de 
# H_HISTORICO a la carga de ka base de datos

# 1) CATALOGO_VALORES (super-dimensional)
# ----------------------------------------

cols = ['TIPO_VALOR','TICK','FEC_CARGA']
# -----------------------------------------------------------
SDIM_VALORES = H_HISTORICO[cols].drop_duplicates()

# 2) CATALOGO_BOLSAS (super-dimensional)
# ----------------------------------------

cols = ['TIPO_MERCADO','TIPO_BOLSA','COD_BOLSA','FEC_CARGA']
# -----------------------------------------------------------
bolsa_1 = DIM_BOLSA_VALORES[['COD_BOLSA_INTEGRADA','FEC_CARGA']].drop_duplicates()
bolsa_1['COD_BOLSA'] = bolsa_1['COD_BOLSA_INTEGRADA']
bolsa_1['TIPO_MERCADO'] = 'BURSATIL'
bolsa_1['TIPO_BOLSA'] = 'MERCADO DE VALORES'
bolsa_1 = bolsa_1[cols]

bolsa_2 = DIM_EXCHANGE_CRIPTO[['COD_EXCHANGE','FEC_CARGA']].drop_duplicates()
bolsa_2['COD_BOLSA'] = bolsa_2['COD_EXCHANGE']
bolsa_2['TIPO_MERCADO'] = 'EXTRABURSATIL'
bolsa_2['TIPO_BOLSA'] = 'EXCHANGE DE CRIPTOMONEDAS'
bolsa_2 = bolsa_2[cols]

SDIM_MERCADOS = pd.concat([bolsa_1,bolsa_2], ignore_index=True)
del bolsa_1,bolsa_2

# 3) Codificamos las bolsaS de H_HISTORICO
# ----------------------------------------
codigo = """

# from tablas_ini import H_HISTORICO

from clase_Entorno import time,date,pd
from TDC_exchange import DIM_EXCHANGE_CRIPTO 
from TDC_bolsa import DIM_BOLSA_VALORES
from H_historico_cotizaciones import H_HISTORICO
recuentos = H_HISTORICO.groupby('COD_BOLSA')['FECHA'].count()  

"""

cols = H_HISTORICO.columns.tolist()
cols = [col for col in cols if col != 'TIPO_VALOR']
# bolsa (x) exchange => cod_exchange
aux = pd.merge(H_HISTORICO, DIM_EXCHANGE_CRIPTO[['EXCHANGE','COD_EXCHANGE']].drop_duplicates(), left_on='BOLSA', right_on='EXCHANGE', how='left')
# bolsa (x) region => cod_bolsa_integrada (x)
aux = pd.merge(aux, DIM_BOLSA_VALORES[['COD_BOLSA_INTEGRADA','REGION']].drop_duplicates(), left_on='BOLSA', right_on='REGION', how='left')
# cod_bolsa_integrada (x) cod_bolsa_integrada => cod_bolsa_integrada (y)
aux = pd.merge(aux, DIM_BOLSA_VALORES[['COD_BOLSA_INTEGRADA']].drop_duplicates(), left_on='BOLSA', right_on='COD_BOLSA_INTEGRADA', how='left')
# cod_bolsa = coalesce(COD_BOLSA_INTEGRADA_x,COD_BOLSA_INTEGRADA_y,COD_EXCHANGE)
aux['COD_BOLSA'] = aux['COD_BOLSA_INTEGRADA_x'].fillna(aux['COD_BOLSA_INTEGRADA_y']).fillna(aux['COD_EXCHANGE'])

# Preparamos columnas
H_HISTORICO = aux[['COD_BOLSA' if col == 'BOLSA' else col for col in cols]].drop_duplicates()
H_HISTORICO.loc[H_HISTORICO['COD_BOLSA'].isnull(),'COD_BOLSA'] = 'N/A'
# renombramos
HH_HISTORICO_COTIZACION = H_HISTORICO

#############################################################################
#                            H_ESTADOS_CONTABLES
#############################################################################

# 1) CODIFICACION DE H_ESTADOS_CONTABLES
# aux = H_ESTADOS_CONTABLES
# H_ESTADOS_CONTABLES = aux
# -----------------------------------------------------------

# traemos cod_sector para preparar TDC_ESTADOS
H_ESTADOS_CONTABLES.loc[H_ESTADOS_CONTABLES['TICK'].isin(['VOW3']), 'TICK'] = 'VOWG_P'
H_ESTADOS_CONTABLES = pd.merge(H_ESTADOS_CONTABLES,DIM_ACCIONES[['TICK','COD_SECTOR']].drop_duplicates(),on='TICK',how='left')

#############################################################################
#                               TDC_ESTADOS
#############################################################################

TDC_ESTADOS = H_ESTADOS_CONTABLES[['COD_SECTOR','COD_MAGNITUD','MAGNITUD','FEC_CARGA']].drop_duplicates()
cols_tdc = TDC_ESTADOS.columns.tolist()
cols_tdc.insert(1,'ESTADO_CONTABLE')

# Para evitar warning de *SettingWithCopyWarning: A value is trying to be 
# set on a copy of a slice from a DataFrame*
codigos = pd.DataFrame()
codigos['ESTADO'] = TDC_ESTADOS['COD_MAGNITUD'].str[:2]
codigos['COD_MAGNITUD'] = TDC_ESTADOS['COD_MAGNITUD']
codigos = codigos.drop_duplicates()

def determinar_estado(cod):  
    if cod == 'CR':  
        return 'CUENTA DE RESULTADOS'  
    elif cod == 'BS':  
        return 'BALANCE DE SITUACION'  
    else:  
        return None 
    
codigos['ESTADO_CONTABLE'] = codigos['ESTADO'].apply(determinar_estado) 
TDC_ESTADOS = pd.merge(TDC_ESTADOS,codigos[['COD_MAGNITUD','ESTADO_CONTABLE']],on='COD_MAGNITUD')
TDC_ESTADOS = TDC_ESTADOS[cols_tdc].drop_duplicates()
del codigos

# y preparamos historico
cols = ['TICK','COD_SECTOR','ANIO','PERIODO','COD_MAGNITUD','VALOR_MAGNITUD','FEC_CARGA']
H_ESTADOS_CONTABLES = H_ESTADOS_CONTABLES[cols].drop_duplicates()
H_ESTADOS_CONTABLES.loc[H_ESTADOS_CONTABLES['VALOR_MAGNITUD'] == '','VALOR_MAGNITUD'] = None

#############################################################################
#                          H_ACC_DIVIDENDOS
###############################################s##############################

cols = ['TICK','FEC_DIVIDENDO','DIVIDENDO','FEC_CARGA']
H_ACC_DIVIDENDOS = H_ACC_DIVIDENDOS[cols].drop_duplicates()

#############################################################################
#                          H_CRIPTO_EMISIONES
#############################################################################

cols = ['FEC_DATO','DIA_SEMANA','TICK','OFERTA_ACTUAL','OFERTA_MAXIMA','FEC_CARGA']
H_CRIPTO_EMISIONES = DIM_CRIPTOMONEDAS[cols].drop_duplicates()
H_CRIPTO_EMISIONES.loc[H_CRIPTO_EMISIONES['OFERTA_ACTUAL'] == '', 'OFERTA_ACTUAL'] = None
H_CRIPTO_EMISIONES.loc[H_CRIPTO_EMISIONES['OFERTA_MAXIMA'] == '', 'OFERTA_MAXIMA'] = None

cols = ['TICK','CRIPTOMONEDA','FEC_CARGA']
DIM_CRIPTOMONEDAS = DIM_CRIPTOMONEDAS[cols]

#############################################################################
#                             DIM_BOLSA_VALORES
#############################################################################

# Preparamos tablas DIM_BOLSA_VALORES para carga
# ---------------------------------
cols = ['BOLSA','BOLSA_INTEGRADA','COD_BOLSA_INTEGRADA','COD_REGION','FEC_CARGA']
DIM_BOLSA_VALORES = DIM_BOLSA_VALORES[cols].drop_duplicates()

#############################################################################
#############################################################################

fin = time()

print('')
print('Tiempo de extraccion de los datos: ' + str((fin-ini)/60) + ' minutos')

#############################################################################
#############################################################################

# ELIMINAMOS VARIABLES NO NECESARIAS
# -----------------------------------------------------------

for var in dir():
    
    # print([elemento for elemento in dir() if callable(globals()[elemento])==False])
    # print([elemento for elemento in dir() if hasattr(globals()[elemento], '__spec__')==False])
    
    # Solo eliminamos variables del programa => ni modulos ni funcioens
    if hasattr(globals()[var], '__spec__')==False and callable(globals()[var])==False and var[0] != '_':
        if var not in mis_variables:
            del globals()[var]
            
# del globals()['var'], globals()['mis_variables']
