# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import csv,pd,re,ud,datetime,time
from clase_Entorno import Entorno
e = Entorno(headless=False)
# e = Entorno(headless=False,act=True)

#############################################################################
#############################################################################

from clase_Valores import Valores
v = Valores(entorno=e)

#############################################################################
#############################################################################

codigo = """

url = ''
driver = e.inicio(url=url,close_driver=False)

e = Entorno()
v = Valores(entorno=e,mis_valores=['ACCIONES'],only_one=True)
info = v.dim_info(tipo_valor='ACCIONES')




"""

#############################################################################
#############################################################################

ini = time()

for k,valor in enumerate(e.mis_valores):
# for k,valor in enumerate(['ACCIONES']):
    
    globals()[e.mis_tablas_dim[k]] = v.dim_info(tipo_valor=valor)
    globals()[e.mis_tablas_dim[k]]['FEC_CARGA'] = datetime.now()

fin = time()

print('')
print('Tiempo de construcción de las tablas DIM_: ' + str((fin-ini)/60) + ' minutos')
del ini,fin,k,v,valor
