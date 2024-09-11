# -*- coding: utf-8 -*-
"""
@author: Raul Juan González
"""
from clase_Entorno import datetime,time
from clase_Entorno import Entorno
e = Entorno(headless=False)

#############################################################################
#############################################################################

from clase_Historico import Historico
h = Historico(entorno=e)

#############################################################################
#############################################################################

codigo = """

# ejemplo para proceso de actualizacion
# -----------------------------------------------
e = Entorno(headless=False,act=True)
h = Historico(entorno=e)
H_HISTORICO_FIs = h.construccion_historico(mis_valores=['FIs'],fec_dato=[2023,1,1],ticks=['0P0001LIG8'])


# introducir fecha en input date de yahoo finance
# -----------------------------------------------
driver = e.inicio(url='https://finance.yahoo.com/quote/0P0000XT9O/history/',pag='YF')
input_date = e.busqueda_html(fuente=driver,tag='input',s_atributo=['name','startDate']) 
input_date.send_keys('01')
input_date.send_keys('05')
input_date.send_keys('2023')

"""

#############################################################################
#############################################################################

ini = time()

H_HISTORICO = h.construccion_historico()
H_HISTORICO['FEC_CARGA'] = datetime.now()
tipos_columnas = H_HISTORICO.dtypes  

fin = time()

print('')
print('Tiempo de construcción de H_HISTORICO: ' + str((fin-ini)/60) + ' minutos')

