# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import pd,ud,datetime
from clase_Entorno import Entorno
# Trabajando con página responsive => si está "minimizada", no aparecen 
# todos los elementos
e = Entorno(resize=True,headless=False)

#############################################################################
#############################################################################

print('')
print('**************************************************************')
print('TDC_SECTOR y TDC_INDUSTRIA' )
print('**************************************************************')

url = 'https://es.investing.com/stock-screener'
print(' + '+url)

# Escraping del cod_sector
# No hay cookies => pag='OTRO'
# ----------------------------
driver = e.inicio(url=url,pag='OTRA')

# MENU **SECTOR**
# <div class="my-4 hidden items-center justify-between md:flex md:gap-6">
# ------------------------------------------------------------------------
selector = 'my-4 hidden items-center justify-between md:flex md:gap-6'
elemento_html = e.busqueda_html(fuente=driver,tag='div',s_class=selector,w=True)
botones = e.busqueda_html(fuente=elemento_html,tag='div',n=True )

for boton in botones:
    if boton.text.upper() in ['CUALQUIER SECTOR','ANY SECTOR']:
        boton.click()
        break
    
# SCRAPING SECTORES
# <div class="z-3 rounded border border-[#B5B8BB] bg-white shadow-secondary 
#  no-contextual-alternatives !z-14 max-h-75 w-64 overflow-y-auto !border-[#BDBFC2] 
# py-1.5 font-sans-v2 !shadow-[0_6px_20px_0_rgba(35,37,38,0.16)]" 
# ----------------------------------------------------------------------------
selector = 'z-3 rounded border bg-white shadow-secondary no-contextual-alternatives overflow-y-auto'
elemento_html = e.busqueda_html(fuente=driver,tag='div',s_class=selector)
valores = e.busqueda_html(fuente=elemento_html,tag='li',n=True,)

datos = []
for ind,valor in enumerate(valores):
    if ind <= 9: 
        cod = 'SEC0'+str(ind+1)
    else:
        cod = 'SEC'+str(ind+1)
    datos.append([cod,ud(valor.text.upper())])
    
TDC_SECTOR = pd.DataFrame(datos,columns=['COD_SECTOR','SECTOR'])
TDC_SECTOR['FEC_CARGA'] = datetime.now()

#############################################################################
#############################################################################

# Escraping del cod_industria
# ---------------------------

for boton in botones:
    if boton.text.upper() in ['CUALQUIER INDUSTRIA','ANY INDUSTRY']:
        boton.click()
        break
    
# <div class="z-3 rounded border border-[#B5B8BB] bg-white shadow-secondary 
#  no-contextual-alternatives !z-14 max-h-75 w-64 overflow-y-auto !border-[#BDBFC2] 
# py-1.5 font-sans-v2 !shadow-[0_6px_20px_0_rgba(35,37,38,0.16)]" 
# ----------------------------------------------------------------------------
# selector = 'z-3 rounded border border-[#B5B8BB] bg-white shadow-secondary no-contextual-alternatives max-h-75 w-64 overflow-y-auto py-1.5 font-sans-v2'
elemento_html = e.busqueda_html(fuente=driver,tag='div',s_class=selector)
valores = e.busqueda_html(fuente=elemento_html,tag='li',n=True)

datos = []
for ind,valor in enumerate(valores):
    if ind <= 9: 
        cod = 'IND0'+str(ind+1)
    else:
        cod = 'IND'+str(ind+1)
    datos.append([cod,ud(valor.text.upper())])
    
driver.quit()
del driver
TDC_INDUSTRIA = pd.DataFrame(datos,columns=['COD_INDUSTRIA','INDUSTRIA'])
TDC_INDUSTRIA['FEC_CARGA'] = datetime.now()

#############################################################################
#############################################################################

for var in dir():
    
    # print([elemento for elemento in dir() if callable(globals()[elemento])==False])
    # print([elemento for elemento in dir() if hasattr(globals()[elemento], '__spec__')==False])
    
    # Solo eliminamos variables del programa => ni modulos ni funcioens
    if hasattr(globals()[var], '__spec__')==False and callable(globals()[var])==False and var[0] != '_':
        if var not in e.mis_variables:
            del globals()[var]
