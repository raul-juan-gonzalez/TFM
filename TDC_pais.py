# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import csv,pd,re,ud,datetime
from clase_Entorno import Entorno
e = Entorno()

#############################################################################
#############################################################################

print('')
print('**************************************************************')
print('TDC_PAIS')
print('**************************************************************')

archivo = 'paises.csv'
url_1 = 'https://es.iban.com/currency-codes'
url_2 = 'http://www.transportando.net/ciudades.htm'

print(' + '+archivo)
print(' + '+url_1)
print(' + '+url_2)


# 1) TABLA CON LOS COD PAIS
# -----------------------------------------------------------

with open(e.ruta_fuentes_externas+archivo, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    datos = [row for row in reader]

# Seleccionamos las columnas necesarias
datos = datos[1:len(datos)]
datos = [arr[2:4] + [arr[6]] + [arr[len(datos[0])-2]] + [arr[len(datos[0])-1]] for arr in datos]
 
# Procesamos los registros seleccionados
for ind,array in enumerate(datos):
    array[0] = ud(array[0].upper())
    array[1] = ud(array[1].upper())
    array[2] = ud(array[2].upper())
    array[3] = re.sub(r'[^A-Z0-9, ]', '', ud(array[3].upper()).split(' (')[0].split('.')[0])
    array[4] = re.sub(r'[^A-Z0-9, ]', '', ud(array[4].upper()).split(' (')[0].split('.')[0])
    
# construimos df
columnas = ['COD_PAIS','COD_MONEDA','CONTINENTE','COUNTRY','PAIS']
pais_aux = pd.DataFrame(datos,columns=columnas)
    
#############################################################################
#############################################################################

# 1) scrapeamos tabla con el nombre de la divisa de cada pais
# -----------------------------------------------------------
driver = e.inicio(url=url_1,pag='otra',stop=True)

# <table class="table table-bordered downloads tablesorter">
# ----------------------------------------------------------
selector = 'table table-bordered downloads tablesorter'
tabla = e.busqueda_html(fuente=driver,tag='table',s_class=selector,w=True)
parser = e.inicio(elemento=tabla)
driver.quit()

filas = e.busqueda_html(fuente=parser,tag='tr',n=True)
del driver,parser,tabla

datos = []
for fila in filas:
    vector = []
    td = e.busqueda_html(fuente=fila,tag='td',n=True)
    for ind,data in enumerate(td):
        if data.text not in ['\n','\n\n'] and ind in [1,2]:
            vector.append(ud(data.text.upper()))
    datos.append(vector)
    
# construimos df
columnas = ['MONEDA','COD_MONEDA']    
divisa_aux = pd.DataFrame(datos,columns=columnas)
divisa_aux = divisa_aux.drop_duplicates()

# Cruzamos y reordenamos columnas
TDC_PAIS = pd.merge(pais_aux, divisa_aux, on='COD_MONEDA', how='left')
columnas = ['COD_PAIS','PAIS','COUNTRY','CONTINENTE','COD_MONEDA','MONEDA']
TDC_PAIS = TDC_PAIS[columnas]
del pais_aux,divisa_aux

# 2) Aplicamos correcciones antes de cargar
TDC_PAIS.loc[TDC_PAIS['CONTINENTE'] == 'ANTARTIDA I TERRITORIS PROPERS', 'CONTINENTE'] = 'ANTARTIDA'

TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ESPANA', 'PAIS'] = 'ESPANIA'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'SYDNEY', 'PAIS'] = 'SIDNEY'


TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'BELARUS', 'COD_MONEDA'] = 'RB'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'BELARUS', 'MONEDA'] = 'RUBLO BIELORRUSO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'BELARUS', 'PAIS'] = 'BIELORRUSIA'

TDC_PAIS.loc[TDC_PAIS['MONEDA'].isnull(), 'MONEDA'] = None
TDC_PAIS.loc[TDC_PAIS['MONEDA'].isnull(), 'COD_MONEDA'] = None

duplicates = TDC_PAIS['PAIS'].duplicated()
paises_duplicados = TDC_PAIS[duplicates]
# TDC_PAIS[TDC_PAIS['PAIS'] == 'UE']

TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'AUSTRALIA','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'CURAZAO','MONEDA'] = 'FLORIN ANTILLANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ISLA DE NAVIDAD','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ISLA NORFOLK','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ISLAS COCOS (KEELING)','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ISLAS COOK','MONEDA'] = 'DOLAR NEOZELANDES'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ISLAS HEARD Y MCDONALD','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'KIRIBATI','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'NAURU','MONEDA'] = 'DOLAR AUSTRALIANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'NIUE','MONEDA'] = 'DOLAR NEOZELANDES'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'NUEVA ZELANDA','MONEDA'] = 'DOLAR NEOZELANDES'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ISLAS PITCAIRN','MONEDA'] = 'DOLAR NEOZELANDES'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'TOKELAU','MONEDA'] = 'DOLAR NEOZELANDES'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'SAN MARTIN (PARTE NEERLANDESA)','MONEDA'] = 'FLORIN ANTILLANO NEERLANDES'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'TUVALU','MONEDA'] = 'DOLAR AUSTRALIANO'

TDC_PAIS.loc[TDC_PAIS['COD_PAIS'] == 'GBR','PAIS'] = 'REINO UNIDO'
TDC_PAIS.loc[TDC_PAIS['COD_PAIS'] == 'GBR','COUNTRY'] = 'UNITED KINGDOM'

TDC_PAIS.loc[TDC_PAIS['MONEDA'] == 'DOLAR NEOZELANDES', 'COD_MONEDA'] = 'NZD'
TDC_PAIS.loc[TDC_PAIS['MONEDA'] == 'DOLAR AUSTRALIANO', 'COD_MONEDA'] = 'AUD'
TDC_PAIS.loc[TDC_PAIS['MONEDA'] == 'FLORIN ANTILLANO NEERLANDES', 'COD_MONEDA'] = 'ANG'

TDC_PAIS = TDC_PAIS.dropna()
# null_values = TDC_PAIS.isnull().sum()
# print(null_values)
TDC_PAIS = TDC_PAIS.drop_duplicates()
# duplicates = TDC_PAIS.duplicated()
# print(TDC_PAIS[duplicates])

TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'COREA','MONEDA'] = 'WON SURCOREANO'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'COREA','PAIS'] = 'COREA DEL SUR'
TDC_PAIS.loc[TDC_PAIS['PAIS'] == 'ESTADOS UNIDOS DE AMERICA','PAIS'] = 'ESTADOS UNIDOS'

#############################################################################
#############################################################################

codigo = """
# Añadimos divisa para EURONEXT
# -----------------------------------------------------------
fila = {}
valores = ['UE','ESPACIO ECONOMICO EUROPEO','EUROPEAN ECONOMIC AREA','EUROPA','EUR','EURO']
for ind,col in enumerate(columnas):
    fila[col] = [valores[ind]]
new_row = pd.DataFrame(fila)

# Concatenar la nueva fila al final del DataFrame
TDC_PAIS = pd.concat([TDC_PAIS, new_row], ignore_index=True)
"""

#############################################################################
#############################################################################

# 3) scrapeamos tabla con los cod_region de cada pais
# -----------------------------------------------------------
driver = e.inicio(url=url_2,pag='otra',stop=True)
tabla = e.busqueda_html(fuente=driver,tag='table',w=True)
parser = e.inicio(elemento=tabla)
driver.quit()

filas = e.busqueda_html(fuente=parser,tag='tr',n=True)
del driver,parser,tabla

datos = []
for fila in filas:  
    vector = []
    td = e.busqueda_html(fuente=fila,tag='td',n=True)
    for ind,data in enumerate(td):
        if ind in[0,1,2]:
            valor = ud(data.text.upper())
            valor = valor.split('/')[0]
            valor = valor.split('(')[0]
            valor = valor.split(',')[0]
            valor = valor.replace('REP.','REPUBLICA')
            valor = valor.replace('\n','')
            valor = valor.replace('\n\n','')
            vector.append(valor.lstrip().rstrip())
    datos.append(vector)
   
# Seleccionamos las filas y columnas necesarias
datos = datos[2:len(datos)]
datos = [elemento for elemento in datos if elemento and len(elemento) == 3]

columnas = ['REGION','COD_REGION','PAIS']
aux_region = pd.DataFrame(datos,columns=columnas)

# Limipieza
aux_region = aux_region.drop_duplicates()
aux_region.replace('', None, inplace=True)
aux_region = aux_region.dropna()

aux_region.loc[aux_region['PAIS'] == 'HOLANDA','PAIS'] = 'PAISES BAJOS'
aux_region.loc[aux_region['PAIS'] == 'ESPANA','PAIS'] = 'ESPANIA'
aux_region.loc[aux_region['PAIS'] == 'USA','PAIS'] = 'ESTADOS UNIDOS'
aux_region.loc[aux_region['PAIS'] == 'MARUECOS','PAIS'] = 'MARRUECOS'
aux_region.loc[aux_region['PAIS'] == 'GRAN BRETANA','PAIS'] = 'REINO UNIDO'
aux_region.loc[aux_region['PAIS'] == 'COREA','PAIS'] = 'COREA DEL SUR'
aux_region.loc[aux_region['PAIS'] == 'EMIRATOS ARABES','PAIS'] = 'EMIRATOS ARABES UNIDOS'
aux_region.loc[aux_region['PAIS'] == 'ARABIA SAUDITA','PAIS'] = 'ARABIA SAUDI'

aux_region.loc[aux_region['REGION'] == 'NEW YORK','REGION'] = 'NUEVA YORK'
aux_region.loc[aux_region['REGION'] == 'NEW ORLEANS','REGION'] = 'NUEVA ORLEANS'
aux_region.loc[aux_region['REGION'] == 'FRANKFURT','REGION'] = 'FRANCFORT'
aux_region.loc[aux_region['REGION'] == 'MEXICO','REGION'] = 'CIUDAD DE MEXICO'

aux_region.loc[aux_region['REGION'] == 'BERLIN','COD_REGION'] = 'BER'

TDC_PAIS = pd.merge(TDC_PAIS, aux_region, on='PAIS', how='left')
TDC_PAIS = TDC_PAIS.explode('REGION')
del aux_region

columnas = ['COD_PAIS','PAIS','COUNTRY','CONTINENTE','COD_MONEDA','MONEDA','COD_REGION','REGION']
TDC_PAIS = TDC_PAIS[columnas]

#############################################################################
#############################################################################

# Funcion para mantener *COD_REGION* como clave unica:
def add_region(pais,region,cod_region):

    # Seleccionamos una bolsa del pais en cuestion => divisa
    fila = TDC_PAIS.loc[TDC_PAIS['PAIS'] == pais].head(1)
    # Añadimos region
    fila.loc[:, ['REGION','COD_REGION']] = [region,cod_region]
    
    # Imprimos fila a añadir en el df
    # print('')
    # [print(elemento) for elemento in fila.values]
    
    # Control del estado de la adicion de la fila
    if fila.empty:
        print('      -> PAIS NO ENCONTRADO EN TDC_PAIS')
        return TDC_PAIS
    else:
        if TDC_PAIS.loc[TDC_PAIS['COD_REGION'] == cod_region].empty:
            return pd.concat([TDC_PAIS, fila], ignore_index=True)
        else:
            print('      -> ¡YA EXISTE UN *COD_REGION* (' + cod_region + ') EN EL DATAFRAME! La fila no se añadirá ')
            return TDC_PAIS
    
# AÑADIMOS REGIONES QUE QUEDEN SIN INFROMAR
TDC_PAIS = add_region(pais='COREA DEL SUR',region='BUSAN',cod_region='BSN')
TDC_PAIS = add_region(pais='CHINA',region='SHENZHEN',cod_region='SNZ')
TDC_PAIS = add_region(pais='ESTONIA',region='TALLIN',cod_region='TLN')
TDC_PAIS = add_region(pais='LETONIA',region='RIGA',cod_region='RGA')
TDC_PAIS = add_region(pais='LITUANIA',region='VILNA',cod_region='VLA')
TDC_PAIS = add_region(pais='ISLANDIA',region='REIKIAVIK',cod_region='RKK')
TDC_PAIS = add_region(pais='ARMENIA',region='EREVAN',cod_region='ERV')
TDC_PAIS = add_region(pais='AUSTRALIA',region='SIDNEY',cod_region='SNY')
TDC_PAIS = add_region(pais='BRASIL',region='SAO PAULO',cod_region='SPL')

TDC_PAIS = add_region(pais='TAILANDIA',region='BANGKOK',cod_region='BGK')
TDC_PAIS = add_region(pais='INDONESIA',region='YAKARTA',cod_region='YKT')

#############################################################################
#############################################################################

# preparamos para carga (cod_region es clave primaria en TDC_PAIS)
TDC_PAIS = TDC_PAIS.dropna(subset=['COD_REGION'])
TDC_PAIS['FEC_CARGA'] = datetime.now()

if not TDC_PAIS[TDC_PAIS.duplicated(subset=['COD_REGION'])].empty:
    dups = TDC_PAIS[TDC_PAIS.duplicated(subset=['COD_REGION'])]['COD_REGION'].tolist()
    for e in dups:
        print(e)
        print(TDC_PAIS.loc[TDC_PAIS['COD_REGION'] == e].values)
else:
    print('      -> NO HAY DUPLICADOS EN TDC_PAIS')

##############################################################################
##############################################################################  
    
for var in dir():
    
    # print([elemento for elemento in dir() if callable(globals()[elemento])==False])
    # print([elemento for elemento in dir() if hasattr(globals()[elemento], '__spec__')==False])
    
    # Solo eliminamos variables del programa => ni modulos ni funcioens
    if hasattr(globals()[var], '__spec__')==False and callable(globals()[var])==False and var[0] != '_':
        if var not in e.mis_variables:
            del globals()[var]
            