# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import datetime,time
from clase_Entorno import Entorno
e = Entorno()
# e = Entorno(act=True)

##############################################################################
##############################################################################

from clase_Dividendos import Dividendos

d = Dividendos(entorno=e)

##############################################################################
##############################################################################

codigo = """

from clase_Entorno import csv,pd,re,ud,datetime,time
from clase_Entorno import Entorno
from clase_Dividendos import Dividendos

e = Entorno(headless=False)
d = Dividendos(entorno=e,only_one=True)
# d.extraer_par(url='https://es.investing.com/equities/bbva-dividends?cid=32289')

url = 'https://es.finance.yahoo.com/quote/REP.MC/history/'
driver = e.inicio(url=url,pag='YF',close_driver=False)

# 2) La opcion "solo dividendos" ya se ha seleccionado => introducimos
# las fechas
# --------------------------------------------------------------------

# Nos ubicamos en la seccion para acotar busqueda de elementos
# <section .... data-test="qsp-historical">
section = e.busqueda_html(fuente=driver,tag='section',s_atributo=['data-test','qsp-historical'],w=True)
# print(section.text[:50])

"""

##############################################################################
##############################################################################
    
ini = time()

H_ACC_DIVIDENDOS = d.construccion_historico()
H_ACC_DIVIDENDOS['FEC_CARGA'] = datetime.now()

fin = time()

print('')
print('Tiempo de construcción de H_ACC_DIVIDENDOS: ' + str((fin-ini)/60) + ' minutos')