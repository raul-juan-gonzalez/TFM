# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import datetime,time
from clase_Entorno import Entorno
#e = Entorno(headless=False)
e = Entorno(headless=False, act=True)

#############################################################################
#############################################################################

from clase_Estados import Estados
est = Estados(entorno=e)

#############################################################################
#############################################################################

codigo = """

url = 'https://es.investing.com/equities/bbva-income-statement?cid=32289'
e = Entorno(headless=False)
driver = e.inicio(url=url,close_driver=False)

from clase_Estados import Estados
e = Entorno(headless=False)
est = Estados(entorno=e,only_one=True)
H_ESTADOS_CONTABLES = est.construccion_historico()


est = Estados(entorno=e,only_one=True)
H_ESTADOS_CONTABLES_uni = est.construccion_historico()
H_ESTADOS_CONTABLES_uni['FEC_CARGA'] = datetime.now()



"""

##############################################################################
##############################################################################

ini = time()

H_ESTADOS_CONTABLES = est.construccion_historico()
H_ESTADOS_CONTABLES['FEC_CARGA'] = datetime.now()

fin = time()

print('')
print('Tiempo de construcción de H_ESTADOS_CONTABLES: ' + str((fin-ini)/60) + ' minutos')
del ini,fin


