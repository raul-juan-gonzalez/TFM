# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import pd,ud,datetime
from clase_Entorno import Entorno
e = Entorno()

#############################################################################
#############################################################################

print('')
print('**************************************************************')
print('DIM_EXCHANGE_CRIPTO')
print('**************************************************************')

url = 'https://javilinares.com/5-mejores-exchanges-de-criptomonedas/'
print(' + '+url)

# CREACION DE LA TABLA DIM_EXCHANGE_CRIPTO
# ---------------------------------

driver = e.inicio(url=url,pag='otra',stop=True)
tabla = e.busqueda_html(fuente=driver,tag='table')
parser = e.inicio(elemento=tabla)
driver.quit()

filas = e.busqueda_html(fuente=parser,tag='tr',n=True)
del driver,parser,tabla

datos = []
for f,fila in enumerate(filas):
    vector = []
    td = e.busqueda_html(fuente=fila,tag='td',n=True)
    for ind,data in enumerate(td):            
        if ind !=0 and data.text not in ['','\n','\n\n']:
            if f == 0:
                # EXCHANGE
                valor = data.text.upper()
                vector.append(ud(valor))
            if f == 1:
                # FUNDACION
                valor = int(data.text)
                vector.append(valor) 
            if f==2:
                # REGULACION
                valor = data.text.upper().replace(', ','/')
                if 'ESPAÑA' in valor:
                    valor = valor.replace('Ñ','NI')
                vector.append(ud(valor))
            if f==3:
                # COMISIONES
                valores = data.text.split(' ')
                aux = []
                for valor in valores:
                    if '%' in valor:
                        aux.append(float(valor.replace('%','')))
                vector.append(round(sum(aux)/len(aux),2))
            if f==4:
                # METODOS DE PAGO
                valor = data.text.upper().replace(', ','/')
                vector.append(ud(valor))
            if f==5:
                # CRIPTOMONEDAS
                if 'AMPLIA' in data.text.upper():
                    vector.append('MEDIA')
                elif 'MAYOR' in data.text.upper():
                    vector.append('ALTA')
                else:
                    vector.append('BAJA')
            if f==6:
                # SEGURIDAD
                if 'ALTA' in data.text.upper():
                    vector.append('ALTA')
                else:
                    vector.append('MEDIA')
            if f==7:
                # SERVICIOS
                valor = data.text.upper().replace(', ','/')
                vector.append(ud(valor))
            if f==8:
                # SERVICIOS
                valor = data.text.upper()
                vector.append(ud(valor))
                
    datos.append(vector)
    # Añadimos el cod_exchange en la segun iteracion
    if len(datos) == 1:
        vector = []
        for valor in datos[0]:
            if valor == 'KRAKEN':
                vector.append('KRK')
            elif valor == 'COINBASE':
                vector.append('CBS')
            elif valor == 'BINANCE':
                vector.append('BNC')
            elif valor == 'BIT2ME':
                vector.append('B2M')
            elif valor == 'KUCOIN':
                vector.append('KCN')
            else:
                None   
        datos.append(vector)
    
# Preparamos
datos = [elemento for elemento in datos if elemento and len(elemento) == 5]
aux = pd.DataFrame(datos) 
# Transponemos y 
DIM_EXCHANGE_CRIPTO = aux.T
# Renombrmaos columans 
columnas = ['EXCHANGE','COD_EXCHANGE','YEAR_FUNDACION','REGULACION','PORCENTAJE_MEDIO_COMISION','METODOS_PAGO','VARIEDAD_CATALOGO','SEGURIDAD','TIPO_SERVICIOS','SOPORTE_CLIENTE']
DIM_EXCHANGE_CRIPTO.columns = columnas

# Adición manual de registros
# ---------------------------
fila = {}
valores = ['INVESTING.COM','INV']
[valores.append(None) for i in range(0,len(columnas)-2)]

for ind,col in enumerate(columnas):
    fila[col] = [valores[ind]]
new_row = pd.DataFrame(fila)

# Concatenar la nueva fila al final del DataFrame
DIM_EXCHANGE_CRIPTO = pd.concat([DIM_EXCHANGE_CRIPTO, new_row], ignore_index=True)

# Añadimos fecha de cargas
DIM_EXCHANGE_CRIPTO['FEC_CARGA'] = datetime.now()

##############################################################################
##############################################################################  
    
for var in dir():
    
    # print([elemento for elemento in dir() if callable(globals()[elemento])==False])
    # print([elemento for elemento in dir() if hasattr(globals()[elemento], '__spec__')==False])
    
    # Solo eliminamos variables del programa => ni modulos ni funcioens
    if hasattr(globals()[var], '__spec__')==False and callable(globals()[var])==False and var[0] != '_':
        if var not in e.mis_variables:
            del globals()[var]
            