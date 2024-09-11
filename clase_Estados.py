# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import json,csv,pd,re,ud,datetime,timedelta,sleep

# Constantes de teclado
from clase_Entorno import ActionChains
from clase_Entorno import Keys

# Excepciomes
from clase_Entorno import ElementNotInteractableException
from clase_Entorno import ElementClickInterceptedException
from clase_Entorno import NoSuchElementException
from clase_Entorno import TimeoutException

############################################################################# 
############################################################################# 

codigo = """

from clase_Entorno import Entorno,sleep
e = Entorno(headless=False)

url = 'https://es.investing.com/equities/bbva-income-statement?cid=32289'
driver = e.inicio(url=url,close_driver=False)
actions = ActionChains(driver) 

sleep(2)

from clase_Entorno import ActionChains
from clase_Entorno import Keys

# para cerrar publicidad => parece ser que no se carga toda la página 
# hasta que se cierra 
# <div id="native_playerSekindoSPlayer66afd41cb7e98">
# <div id="skipBtn">
publi = e.busqueda_html(fuente=driver,s_id='native_playerSekindoSPlayer66afd41cb7e98')
skip = e.busqueda_html(fuente=publi,s_id='skipBtn')
skip.click()

elemento_html = e.busqueda_html(fuente=driver,tag='div',s_class='alignBottom')
botones = e.busqueda_html(fuente=elemento_html,tag='a',n=True)
for boton in botones:
    if boton.text.upper() in ['ANNUAL','ANUAL']:
        actions.send_keys(Keys.ESCAPE).perform()  
        boton.click()
        break


actions.send_keys(Keys.ESCAPE).perform()  

"""

############################################################################# 
############################################################################# 

class Estados:
    
    # Constructor
    def __init__(self,entorno,only_one=False):
        
        self.e = entorno
        self.tipo_valor = 'ACCIONES'
        self.data_a = []
        self.data_t = []
        self.cols = []
        self.only_one = only_one
        
    # -----------------------------------------------------------------------
    
    def extraer_estado(self,driver,estado,periodo):
        
        if periodo == 'A':
            
            salir = 0
            # Solo hay problemas cuando pasamos a extraer el informe anual, 
            # que es cuando se debe pulsar el boton
            # --------------------------------------------------------------
            # quedamos en bucle procesando excepciones (pop-ups y publicidad) 
            # hasta que se pulse el boton
            while salir == 0:
                
                try:
                    actions = ActionChains(driver) 
                    # Informes anuales
                    
                    # Clik sobre boton "Annual"
                    # <div class="alignBottom">
                    # ----------------------------
                    elemento_html = self.e.busqueda_html(fuente=driver,tag='div',s_class='alignBottom')
                    botones = self.e.busqueda_html(fuente=elemento_html,tag='a',n=True)
                    for boton in botones:
                        if boton.text.upper() in ['ANNUAL','ANUAL']:
                            # El pop up solo nos fastidia si aparece antes de 
                            # hacer click => si aparece => cerramos pop_up a tra-
                            # vés de tecla scape => luego click
                            actions.send_keys(Keys.ESCAPE).perform() 
                            # imprimimos periodicidad
                            print('     - '+boton.text.upper())
                            # click para obtener informe anual => por defecto
                            # la pagina se carga con el trimestral
                            boton.click()
                            salir = 1
                            break
                            
                except (ElementClickInterceptedException,NoSuchElementException):
                    # SI LLEGAMOS AQUI ES POR LA PUBLICIDAD
                    # para cerrar publicidad => parece ser que no se carga toda la 
                    # página hasta que se cierra 
                    # ----------------------------------------------------------------
                    # <div id="native_playerSekindoSPlayer66afd41cb7e98">
                    # <div id="skipBtn">
                    # ----------------------------------------------------------------
                    try:
                        skip = self.e.busqueda_html(fuente=driver,s_id='skipBtn')
                        skip.click()
                        print('     + Se ha cerrado la publi ...')
                    except NoSuchElementException:
                        # Por si es por otro motivo y no hay puble => SCAPE
                        actions.send_keys(Keys.ESCAPE).perform()  
                            
        else:
            
            # imprimimos periodicidad
            elemento_html = self.e.busqueda_html(fuente=driver,tag='div',s_class='alignBottom')
            botones = self.e.busqueda_html(fuente=elemento_html,tag='a',n=True)
            for boton in botones:
                if boton.text.upper() in ['TRIMESTRAL']:
                    print('     - '+boton.text.upper())
                    break
                
        
        # 1) Tick
        # <h1 class="float_lang_base_1 relativeAttr">
        # -------------------------------------------
        selector = 'float_lang_base_1 relativeAttr'
        elemento_html = self.e.busqueda_html(fuente=driver,tag='h1', s_class=selector)
        tick = elemento_html.text.upper().split('(')[1].split(')')[0]
        
        # 2) Tabla
        # <table class="genTbl reportTbl">
        # -------------------------------------------
        selector = 'genTbl reportTbl'
        data_table = self.e.busqueda_html(fuente=driver,tag='table', s_class=selector,w=True)
        filas = self.e.busqueda_html(fuente=data_table,tag='tr',n=True)
    
        columnas = ['TICK','COD_MAGNITUD','MAGNITUD']        
        datos = []
        componente = 1
        indice = 1
    
        for ind,fila in enumerate(filas):
            
            # COLUMNAS => fec_dato
            #------------------------------------------------------------
            # print(fila.text)
            # a cierre terminado
            if ind == 0 and fila != []:
                
                cols = self.e.busqueda_html(fuente=fila,tag='th',n=True)
                for ind,col in enumerate(cols):
                    if ind in [1,2,3,4]:
                        # aux = dd/mm/yyyy
                        aux = col.text[5:7]+'/'+col.text[8:10]+'/'+col.text[:4]
                        print(aux)
                        
                        # Columnas para informes anuales
                        # -------------------------------
                        if periodo == 'A':
                            if col.text[8:10] == '12':
                                columnas.append(col.text[:4]+'_A')
                            elif col.text[8:10] == '01': 
                                # A periodo terminado => cierre del año anterio
                                cierre = str(int(col.text[:4])-1)
                                columnas.append(cierre+'_A')
                            else:
                                columnas.append('0000'+'_AX')
                                
                        # Columnas para informes trimestrales
                        # -----------------------------------
                        else:
                            # Las de EEUU
                            if col.text[8:10] == '01':
                                # Porque aparece al año siguiente
                                cierre = str(int(col.text[:4])-1)+'_T4'
                                columnas.append(cierre)
                            elif col.text[8:10] == '04':
                                columnas.append(col.text[:4]+'_T1')
                            elif col.text[8:10] == '07':
                                columnas.append(col.text[:4]+'_T2')
                            elif col.text[8:10] == '10':
                                columnas.append(col.text[:4]+'_T3')
                            # Las de EUROPA
                            elif col.text[8:10] == '03':
                                columnas.append(col.text[:4]+'_T1')
                            elif col.text[8:10] == '06':
                                columnas.append(col.text[:4]+'_T2')
                            elif col.text[8:10] == '09':
                                columnas.append(col.text[:4]+'_T3')
                            elif col.text[8:10] == '12':
                                columnas.append(col.text[:4]+'_T4')
                            else:
                                columnas.append('0000'+'_TX')
                            
                #print(columnas)
                # Para comprobar que el registro extraido tiene el número correc-
                # to de columnas y construir en dichos casos el cod_epigrafe
                print('     - '+str(columnas))
                control = len(columnas)
            
                
            # DATOS => 1 fila por "tr"
            #------------------------------------------------------------
            if fila != [] and ind != 0:
    
                vector = [tick]
                td = self.e.busqueda_html(fuente=fila,tag='td',n=True)
                for data in td:                 
                    
                    try:
                        aux = data.text.replace('.','').replace(',','.')
                        vector.append(float(aux))
                        componente = componente + 1
                        #print('Componente ........: ' + str(aux))
                    except ValueError:
                        # En caso de que falle la conversión a float es porque 
                        # tenemos un encabezado o un valor nulo ('-')
                        if data.text == '':
                            None
                        else:
                            # Valor nulo
                            if data.text == '-':
                                aux = ''
                                vector.append(aux)
                                componente = componente + 1
                            # Encabezado
                            else:
                                aux = re.sub(r'[^A-Z()\- ]', '',ud(data.text.upper()))
                                if aux != '':
                                    vector.append(aux)
                                    # Es el primer valor (encabezado) de los 5 a 
                                    # añadir
                                    componente = 1
                                    
                # Hemos extraido la fila => añadimos cod_epigrafe
                # print(vector)
                if componente == 5 and len(vector)==len(columnas)-1:
                    if indice <= 9:
                        apartado = '0'+str(indice)
                    else:
                        apartado = str(indice)
                    vector.insert(1,estado+'_'+apartado)
                    datos.append(vector)
                    indice = indice + 1
    
        # INFORMES ANUALES
        for fila in datos:
            aux = fila[2].split(' ')
            # En millones de EUR (excepto para los elementos por acción)
            # buscamos en el *descriptivo del epigrafre*
            if 'ACCION' not in aux:
                for i in range(3, len(fila)):
                    # y multimplicamos a partir de la 4a columna
                    fila[i] = fila[i]*1000000
                              
        return datos,columnas

    def construccion_historico(self,fec_dato=[],ticks=[]):
        
        with open(self.e.ruta_fuentes+self.tipo_valor+'.json') as j:
            data_source = json.load(j)
            
        for ind,elemento in enumerate(data_source):
            
            if self.e.act:
                if elemento['PAR'].split('/')[0] not in ticks:
                    self.fec_dato = []
                else:
                    self.fec_dato = fec_dato
            
            k=1 # primer (k=0) o segundo (k=1) elemento del campo del JSON
            urls = [elemento['CUENTA DE RESULTADOS'][k],elemento['BALANCE'][k]]
            print('')
            print('**************************************************************')
            
            for ind,url in enumerate(urls):
                 
                print('H_ESTADOS_CONTABLES'+' - '+url)         
                driver = self.e.inicio(url=url,close_driver=False)
                
                if ind == 0:
                    
                    # CUENTA DE RESULTADOS
                    print('')
                    print('     + Extrayendo informes trimestrales ...')
                    datos = []
                    columnas_t = []
                    datos,columnas_t = self.extraer_estado(driver=driver,estado='CR',periodo='T')
                    self.data_t.extend(datos)
                    
                    print('')
                    print('     + Extrayendo informes anuales ...')
                    datos = []
                    columnas_a = []
                    datos,columnas_a = self.extraer_estado(driver=driver,estado='CR',periodo='A')
                    self.data_a.extend(datos)
                                   
                elif ind == 1:
                    
                    # BALANCE DE SITUACION
                    print('')
                    print('     + Extrayendo informes trimestrales ...')
                    datos = []
                    columnas_t = []
                    datos,columnas_t = self.extraer_estado(driver=driver,estado='BS',periodo='T')
                    self.data_t.extend(datos)
                    
                    print('')
                    print('     + Extrayendo informes anuales ...')
                    datos = []
                    columnas_a = []
                    datos,columnas_a = self.extraer_estado(driver=driver,estado='BS',periodo='A')
                    self.data_a.extend(datos)
                    
                else:
                    None
                    
                driver.quit()
                del driver
                
            print('**************************************************************')
            if self.only_one:
                # print(self.data_t[0])
                # print(self.data_a[0])
                break
                                                                       
        datos_a = pd.DataFrame(self.data_a,columns=columnas_a)
        datos_t = pd.DataFrame(self.data_t,columns=columnas_t)
        self.cols = ['TICK','ANIO','PERIODO','COD_MAGNITUD','MAGNITUD','VALOR_MAGNITUD']

        datos_a = datos_a.melt(id_vars=columnas_a[:3], var_name='PERIODO_INFORME', value_name='VALOR_MAGNITUD').sort_values(by=columnas_a[:2])
        datos_a['ANIO'] = datos_a['PERIODO_INFORME'].apply(lambda campo: int(campo[:4]))
        datos_a['PERIODO'] = 'A'
        datos_a = datos_a[self.cols]

        datos_t = datos_t.melt(id_vars=columnas_a[:3], var_name='PERIODO_INFORME', value_name='VALOR_MAGNITUD').sort_values(by=columnas_a[:2])
        datos_t['ANIO'] = datos_t['PERIODO_INFORME'].apply(lambda campo: int(campo[:4]))
        datos_t['PERIODO'] = datos_t['PERIODO_INFORME'].apply(lambda campo: 'T'+campo[6:7])
        datos_t = datos_t[self.cols]
        
        if self.e.act:
            
            if self.fec_dato != []:
                
                filtrados = datos_a[datos_a.iloc[:, 1] >= self.fec_dato[0]]  
                datos_a = filtrados
                
                filtrados = datos_t[datos_t.iloc[:, 1] >= self.fec_dato[0]]  
                datos_t = filtrados
        
        salida = pd.concat([datos_a, datos_t])
        salida = salida[salida['ANIO'] != 0]
        
        return salida