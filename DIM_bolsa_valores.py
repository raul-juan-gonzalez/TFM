# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import pd,ud,datetime
from clase_Entorno import Entorno
e = Entorno()

#############################################################################
#############################################################################

from TDC_pais import TDC_PAIS

aux_pais =  TDC_PAIS[['COD_PAIS','PAIS']].dropna().drop_duplicates()
aux_region =  TDC_PAIS[['COD_REGION','REGION']].dropna().drop_duplicates() 

#############################################################################
#############################################################################

print('')
print('**************************************************************')
print('DIM_BOLSA_VALORES')
print('**************************************************************')

url_1 = 'https://es.wikipedia.org/wiki/Anexo:Bolsas_de_valores_m%C3%A1s_grandes_del_mundo'
print(' + '+url_1)

# CREACION DE DIM_BOLSA_VALORES
# ---------------------
driver = e.inicio(url=url_1,pag='otra',stop=True)

# scrapeo de la tabla => regiones de las principales bolsas del mundo
# <table class="wikitable sortable col1der col2izq col3izq col4izq col5izq col6izq col7der col8der jquery-tablesorter">
# ----------------------------------------------------------
selector = 'wikitable sortable col1der col2izq col3izq col4izq col5izq col6izq col7der col8der jquery-tablesorter'
tabla = e.busqueda_html(fuente=driver,tag='table',s_class=selector,w=True)
parser = e.inicio(elemento=tabla)
driver.quit()

filas = e.busqueda_html(fuente=parser,tag='tr',n=True)
del driver,parser,tabla

datos = []
for fila in filas:
    vector = []
    tds = e.busqueda_html(fuente=fila,tag='td',n=True)
    for m in range(len(tds)):
        
        if m == 2:
            # bolsa
            bolsa = ud(tds[m].text.upper()).split('\n')[0].lstrip()
            vector.append(bolsa)
            
        if m == 3:
            # cod_bolsa
            cod_bolsa = ud(tds[m].text.upper()).split('\n')[0].lstrip()
            vector.append(cod_bolsa)
            
        if m == 4:
            paises = []
            a = e.busqueda_html(fuente=tds[m],tag='a',n=True)
            for data in a:
                if data.text not in ['','\n','\n\n']:
                    pais =  ud(data.text.upper()).split('\n')[0].lstrip()
                    paises.append(pais)
            # Añadimos a vector
            if len(paises) > 1:
                vector.append(paises)
            else:
                vector.append(paises[0])
                
        if m == 5:
            ciudades = []
            a = e.busqueda_html(fuente=tds[m],tag='a',n=True)
            for data in a:
                if data.text not in ['','\n','\n\n']:
                    ciudad =  ud(data.text.upper()).split('\n')[0].lstrip()
                    ciudades.append(ciudad)
            # Añadimos a vector
            if len(ciudades) > 1:
                vector.append(ciudades)
            else:
                vector.append(ciudades[0])
    # Añadimos el td
    datos.append(vector)
    
for m in range(len(datos)):
    for n in range(len(datos[m])):
        if datos[m][n] == ['UNION EUROPEA','ESPACIO ECONOMICO EUROPEO']:
            datos[m][n] = 'ESPACIO ECONOMICO EUROPEO'
                 
# Aplanamiento de la tabla
datos_aplanado = []
for array in datos:
    #print('')
    #print(str(array))
    vector =  []
    for m in range (len(array)):
        #print(str(m) + ' - ' + str(array[m]))
        if m in [0,1]:
            vector.append(array[m])
        if m == 2:
            if isinstance(array[m],str):
                vector.append(array[m]) 
                if isinstance(array[m+1],str):
                   vector.append(array[m+1])
                   datos_aplanado.append(vector)
                   # print(vector) 
                   # perfecto
                else:
                    for c in array[m+1]:
                        vector.append(c)
                        # print(vector)
                        # perfecto
                        datos_aplanado.append(vector)
                        vector = vector[0:len(vector)-1]
            else:
                for e1 in range(len(array[m])):
                    for e2 in range(len(array[m+1])):
                        if e1 == e2:
                            vector.append(array[m][e1])
                            vector.append(array[m+1][e2])
                            datos_aplanado.append(vector)
                            # perfecto
                            vector = vector[0:len(vector)-2]
                  
# Construimos dataframe
columnas = ['BOLSA','COD_BOLSA','PAIS','REGION']
DIM_BOLSA_VALORES = pd.DataFrame(datos_aplanado,columns=columnas)

# Primeras correcciones
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['BOLSA'] == 'BOLSAS Y MERCADOS ESPANOLES', 'BOLSA'] = 'BOLSAS Y MERCADOS ESPANIOLES'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['BOLSA'] == 'EURONEXT', 'COD_BOLSA'] = 'EURN'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['BOLSA'] == 'DEUTSCHE BORSE', 'BOLSA'] = 'BOLSA DE ALEMANIA'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'LSE', 'BOLSA'] = 'LONDON EXCHANGE GROUP'

DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['PAIS'] == 'ESPANA', 'PAIS'] = 'ESPANIA'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['PAIS'] == 'UNION EUROPEA', 'PAIS'] = 'ESPACIO ECONOMICO EUROPEO'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['PAIS'] == 'MEXICO', 'BOLSA'] = 'BOLSA DE MEXICO'

# Añadimos bolsas segun region
def add_region(pais,region):

    # Seleccionamos una bolsa del pais en cuestion => divisa
    fila = DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['PAIS'] == pais].head(1)
    # Añadimos region
    fila['REGION'] = region
    
    # Imprimos fila a añadir en el df
    # print('')
    # [print(elemento) for elemento in fila.values]
    
    # Control del estado de la adicion de la fila
    if fila.empty:
        print('      -> PAIS NO PRESENTE EN TDC_PAIS')
        return DIM_BOLSA_VALORES
    else:
        if DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['REGION'] == region].empty:
            return pd.concat([DIM_BOLSA_VALORES, fila], ignore_index=True)
        else:
            print('      -> ¡YA EXISTE UNA *REGION* (' + region + ') EN EL DATAFRAME! La fila no se añadirá ')
            return DIM_BOLSA_VALORES
        
DIM_BOLSA_VALORES = add_region('ESPANIA','BARCELONA')
DIM_BOLSA_VALORES = add_region('ALEMANIA','HAMBURGO')
DIM_BOLSA_VALORES = add_region('ALEMANIA','DUSSELDORF')

#############################################################################
#############################################################################

DIM_BOLSA_VALORES = pd.merge(DIM_BOLSA_VALORES, aux_pais, on='PAIS', how='left')
columnas = ['BOLSA','COD_BOLSA','PAIS','COD_PAIS','REGION']
DIM_BOLSA_VALORES = DIM_BOLSA_VALORES[columnas]

DIM_BOLSA_VALORES = pd.merge(DIM_BOLSA_VALORES, aux_region, on='REGION', how='left')
DIM_BOLSA_VALORES = DIM_BOLSA_VALORES.drop_duplicates()

DIM_BOLSA_VALORES['COD_BOLSA_INTEGRADA'] = DIM_BOLSA_VALORES['COD_REGION']
DIM_BOLSA_VALORES['BOLSA_INTEGRADA'] = 'BOLSA DE ' + DIM_BOLSA_VALORES['REGION']

columnas = ['COD_BOLSA','BOLSA','PAIS','COD_PAIS','COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA','COD_REGION','REGION']
DIM_BOLSA_VALORES = DIM_BOLSA_VALORES[columnas]

#############################################################################
#############################################################################

# MAS CORRECCIONES

# 1) EEUU
bolsa = 'BOLSA DE NUEVA YORK'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'NYSE',   ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['NYSE',bolsa]
bolsa = 'NATIONAL ASSOCIATION OF SECURITIES DEALERS AUTOMATED QUOTATION'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'NASDAQ', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA','COD_REGION','REGION']] = ['NASDAQ',bolsa,None,None]

cod_pais = aux_pais[aux_pais['PAIS']=='ESTADOS UNIDOS'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'].isin(['NYSE', 'NASDAQ']), ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE ESTADOS UNIDOS']

# 2) CHINA
bolsa = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES['COD_BOLSA']=='SSE'].reset_index().at[0,'BOLSA']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'SSE',   ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['SSE',bolsa]
bolsa = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES['COD_BOLSA']=='SZSE'].reset_index().at[0,'BOLSA']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'NASDAQ', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['SZSE',bolsa]

cod_pais = aux_pais[aux_pais['PAIS']=='CHINA'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'].isin(['SSE', 'SZSE']), ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE CHINA']

# 3) CANADA
bolsa = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES['COD_BOLSA']=='TSX'].reset_index().at[0,'BOLSA']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'TSX',   ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['TSX',bolsa]

cod_pais = aux_pais[aux_pais['PAIS']=='CANADA'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'TSX', ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE CANADA']

# 4) INDIA
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'BSE', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['BSE','BOLSA DE BOMBAI']
bolsa = 'NATIONAL STOCK EXCHANGE OF INDIA'
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'NSE', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA','COD_REGION','REGION']] = ['NSE',bolsa,None,None]

cod_pais = aux_pais[aux_pais['PAIS']=='CHINA'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'].isin(['BSE', 'NSE']), ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE LA INDIA']

# 5) BRASIL
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'B3', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['B3','BOLSA DE SAO PAULO']

cod_pais = aux_pais[aux_pais['PAIS'] == 'BRASIL'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'B3', ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE BRASIL']

# 6) SUDAFRICA
bolsa = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES['COD_BOLSA']=='JSE'].reset_index().at[0,'BOLSA']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'JSE', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['JSE',bolsa]

cod_pais = aux_pais[aux_pais['PAIS'] == 'SUDAFRICA'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'JSE', ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE SUDAFRICA']

# 7) RUSIA
bolsa = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES['COD_BOLSA']=='MOEX'].reset_index().at[0,'BOLSA']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'MOEX', ['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA']] = ['MOEX',bolsa]

cod_pais = aux_pais[aux_pais['PAIS'] == 'RUSIA'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA'] == 'MOEX', ['COD_BOLSA','BOLSA']] = [cod_pais,'BOLSA DE RUSIA']

# 8) ALEMANIA
cod_pais = aux_pais[aux_pais['PAIS'] == 'ALEMANIA'].reset_index().at[0,'COD_PAIS']
DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['PAIS'] == 'ALEMANIA', 'COD_BOLSA'] = cod_pais

#############################################################################
#############################################################################

# Añadimos bolsas segun region
def add_bolsa(pais,bolsa_integrada,cod_bolsa_integrada):

    # Seleccionamos una bolsa del pais en cuestion => divisa
    fila = DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['PAIS'] == pais].head(1)
    # Añadimos region
    fila[['COD_BOLSA_INTEGRADA','BOLSA_INTEGRADA','COD_REGION','REGION']] = [cod_bolsa_integrada,bolsa_integrada,None,None]
    
    # Imprimos fila a añadir en el df
    # print('')
    # [print(elemento) for elemento in fila.values]
    
    # Control del estado de la adicion de la fila
    if fila.empty:
        print('      -> PAIS ('+pais+') NO PRESENTE EN DIM_BOLSA_VALORES')
        return DIM_BOLSA_VALORES
    else:
        if DIM_BOLSA_VALORES.loc[DIM_BOLSA_VALORES['COD_BOLSA_INTEGRADA'] == cod_bolsa_integrada].empty:
            return pd.concat([DIM_BOLSA_VALORES, fila], ignore_index=True)
        else:
            print('      -> ¡YA EXISTE UN *COD_BOLSA_INTEGRADA* (' + cod_bolsa_integrada + ') EN EL DATAFRAME! La fila no se añadirá ')
            return DIM_BOLSA_VALORES
        
DIM_BOLSA_VALORES = add_bolsa('ALEMANIA','TRADEGATE','TDG')
DIM_BOLSA_VALORES = add_bolsa('ALEMANIA','XETRA','XTR')

#############################################################################
#############################################################################

# ARREGLAMOS COLUMNAS
columnas = ['BOLSA','BOLSA_INTEGRADA','COD_BOLSA_INTEGRADA','COD_REGION','REGION']
DIM_BOLSA_VALORES = DIM_BOLSA_VALORES[columnas]

#############################################################################
#############################################################################

def add_mercado(pais,region,cod_bolsa_integrada=None):
    
    # Falta comporbar que exicste pais y region
    if TDC_PAIS.loc[TDC_PAIS['PAIS'] == pais].empty:
        print('PAIS ('+pais+') NO PRESENTE EN DIM_BOLSA_VALORES')
        return DIM_BOLSA_VALORES
    if TDC_PAIS.loc[TDC_PAIS['REGION'] == region].empty:
        print('REGION ('+region+') NO PRESENTE EN DIM_BOLSA_VALORES')
        return DIM_BOLSA_VALORES
    
    # Si henos llegado aqui es porque hay "pais" y "region" en TDC_PAIS
    bolsa = 'BOLSA DE '+pais
    bolsa_integrada = 'BOLSA DE '+region 
    cod_region = TDC_PAIS[TDC_PAIS['REGION'] == region].reset_index().at[0,'COD_REGION']
    if cod_bolsa_integrada == None:
        cod_bolsa_integrada = cod_region
    
    fila = {}
    valores = [bolsa,bolsa_integrada,cod_bolsa_integrada,cod_region,region]
    for ind,col in enumerate(columnas):
        fila[col] = [valores[ind]]
    new_row = pd.DataFrame(fila)

    # Concatenar la nueva fila al final del DataFrame
    return pd.concat([DIM_BOLSA_VALORES, new_row], ignore_index=True)
    
DIM_BOLSA_VALORES = add_mercado('AUSTRIA','VIENA')

#############################################################################
#############################################################################

# control de claves
# ------------------

# columnas = ['BOLSA','BOLSA_INTEGRADA','COD_BOLSA_INTEGRADA','COD_REGION','REGION']
dup_1 = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES.duplicated(subset=['COD_BOLSA_INTEGRADA'])]
dup_2 = DIM_BOLSA_VALORES[DIM_BOLSA_VALORES.duplicated(subset=['COD_REGION'])]
dup_2 = dup_2.dropna(subset=['COD_REGION'])

if not dup_1.empty or not dup_2.empty:
    print('      -> Hay duplicados en DIM_BOLSA_VALORES')
else:
    print('      -> No hay duplicados en DIM_BOLSA_VALORES')
    
# PRESENTACION FINAL
DIM_BOLSA_VALORES = DIM_BOLSA_VALORES[columnas]
DIM_BOLSA_VALORES['FEC_CARGA'] = datetime.now()

##############################################################################
##############################################################################  
    
for var in dir():
    
    # print([elemento for elemento in dir() if callable(globals()[elemento])==False])
    # print([elemento for elemento in dir() if hasattr(globals()[elemento], '__spec__')==False])
    
    # Solo eliminamos variables del programa => ni modulos ni funcioens
    if hasattr(globals()[var], '__spec__')==False and callable(globals()[var])==False and var[0] != '_':
        if var not in e.mis_variables:
            del globals()[var]
            