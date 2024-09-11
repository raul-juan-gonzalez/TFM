# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from clase_Entorno import json,csv,pd,re,ud,datetime,timedelta,sleep

# Constantes de teclado
from clase_Entorno import Keys
# Excepciomes
from clase_Entorno import ElementNotInteractableException
from clase_Entorno import ElementClickInterceptedException
from clase_Entorno import NoSuchElementException
from clase_Entorno import TimeoutException

from clase_Entorno import mes

############################################################################# 
############################################################################# 

class Historico:
    
    # Constructor
    def __init__(self,entorno):
        
        self.e = entorno
        self.mis_valores = []
        self.ticks = []
        self.fec_dato = []        # [yyyy,m,d]
    
    # -----------------------------------------------------------------------
    
        self.pares = []
        self.datos = []
        
    # -----------------------------------------------------------------------
    
    def input_granularidad(self,driver,valor):
        
        
        if valor not in ['FIs']:
            
            # 1) INPUT GRANULARIDAD VALORES COTIZADOS
            # --------------------------------------------------
            selector = 'historical-data-v2_selection-arrow__3mX7U relative flex flex-1 items-center justify-start gap-1'
            input_granularidad = self.e.busqueda_html (fuente=driver,tag='div',w=True,s_class=selector) 
            input_granularidad.click()
    
            # 2) UNA VEZ INTERACTUADO SOBRE EL MENU "PLAZO" => aparecerá el 
            # desplegable y selecionaremos el <div> "diario"
            selector = 'historical-data-v2_menu-row__oRAlf'
            options_granularidad =  self.e.busqueda_html (fuente=driver,tag='div',w=True,s_class=selector,n=True) 
            
            for option in options_granularidad:
                
                if option.text.upper() in ['DIARIO','DAILY']:
                    option.click()
                    # Para evitar error "StaleElementReferenceException" en Selenium => ocurre 
                    # cuando el elemento con el que se está tratando de interactuar ha sido 
                    # eliminado o ya no está adjunto al DOM (Document Object Model) actual => 
                    # cuando hacemos click en una de las opciones del display, el display 
                    # desaparece del arbol DOM => rompemos el bucle for para evitar lios
                    break
            
        elif valor in ['FIs']:
            None
            
        else:
            print('Procesamiento no disponible para el valor introducido')
            
    # -----------------------------------------------------------------------
              
    def fecha_objetivo(self,input_date, year_obj, month_obj, day_obj):
        
        fecha_actual = datetime.now().date()
                  
        try:
            fecha_obj = datetime(year=year_obj, month=month_obj, day=day_obj).date()
        except ValueError as e:
            print('Error en los parametros de la fecha objetivo:', e)
            return None
        
        if fecha_obj > fecha_actual:
            print('La fecha de inicio del hitórico de datos excede a la más reciente')
            return None
        
        codigo = """
        # PARA EMPEZAR EN FECHA ACTUAL (botono "hoy" del desplegable)
        input_date.send_keys(Keys.TAB)
        input_date.send_keys(Keys.TAB)
        input_date.send_keys(Keys.ENTER)
        """
        
        if fecha_actual.year != year_obj:
    
            # Para poder introducir el año => 3 tabuladores + 1 intro
            input_date.send_keys(Keys.TAB)
            input_date.send_keys(Keys.TAB)
            input_date.send_keys(Keys.TAB)
            input_date.send_keys(Keys.ENTER)
        
            # Calculo del numero de ARROWs UP para llegar al año objetivo => todo
            # esto depende de la estructura del formulario que estamos procesando
            if fecha_actual.month in (1, 2, 3, 4):
                aux = 1
            elif fecha_actual.month in (5, 6, 7, 8):
                aux = 2
            else:
                aux = 3
        
            flechas = aux + ((fecha_actual.year-year_obj)-1)*3
            while flechas != 0:
                # una pulsación de la tecla "ARROW_UP"
                input_date.send_keys(Keys.ARROW_UP)
                flechas = flechas-1
        
            # 2 enters para introducir el año objetivo en la fecha objetivo
            input_date.send_keys(Keys.ENTER)
            input_date.send_keys(Keys.ENTER)
        
            # 7) Seleccionar el mes
            input_date.click()
    
        # Si el año objetivo coincide con el actual, pasamos directamente a se-
        # leccionar el mes
        input_date.send_keys(Keys.TAB)
        input_date.send_keys(Keys.TAB)
        input_date.send_keys(Keys.TAB)
        input_date.send_keys(Keys.ENTER)
        
        # input_date.get_attribute('value')
        # FUNCION QUE MAPEA EL INPUT PARA SELECCIONAR EL MES
        mes.seleccion_mes (input_date,mes_obj = month_obj)
        input_date.send_keys(Keys.ENTER)
        input_date.send_keys(Keys.ENTER)
    
        # 7) Dia y mes => para comppletar la fecha objetivo => despues de 
        # seleccionar el año y el mes, funciona bien el introducir el dia simulan-
        # do un "envio del formulario " con  input_date.send_keys)
        input_date.send_keys(day_obj)
            
    # -----------------------------------------------------------------------    
        
    # para fondos de inversion ('FI') la seleccion de la fecha de inicio requiere
    # un escrapeo diferente: 
        
    def inputs_fecha (self,driver,tipo_valor,fec_ini):
        
        filas_ini = 0
        if tipo_valor not in ['FIs']:
            
            # 0) Numero de filas inicial: NUMERO DE REGISTROS DE LA TABLA HTML
            # ANTES DE INTRODUCIR LOS INPUTS DE FECHA => PARA COMPROBAR EN 
            # FUNCION historico() CUANDO HAN TERMINADO DE CARGAR LOS DATOS
            # <table class="freeze-column-w-1 w-full overflow-x-auto text-xs leading-4">
            # ---------------------------------------------------------
            selector = 'freeze-column-w-1 w-full overflow-x-auto text-xs leading-4'
            try:
                data_table = self.e.busqueda_html (fuente=driver,tag='table',s_class=selector)         
                filas_ini = len(self.e.busqueda_html(fuente=data_table,tag='tr',n=True))
            except (NoSuchElementException):
                # En la fecha actual, puede no haber datos (fin de semana) y 
                # puede no cargarse la tabla
                filas_ini = 0
            
            # 1) SELECTOR DEL MENU DE INPUTS DE FECHA + PROCESAMIENTO
            # <div class="flex flex-1 flex-col justify-center text-sm leading-5 text-[#333]">
            # ---------------------------------------------------------
            selector = 'flex flex-1 items-center rounded border border-solid bg-white py-2 shadow-select'        
            menus = self.e.busqueda_html(fuente=driver,tag='div',s_class=selector,n=True) 
           
            # 2) En variable "menus" tenemos menu "PLAZO" y menu de "INPUTS DATE" por coin-
            # cidencia de selectores => recorremos y nos quedamos con los que tengan el 
            # año actual en el contenido de la etiqueta:
            # ---------------------------------------------------------
            for ind,menu in enumerate(menus):
                if ind==1:
                    menu.click()
                    break
                    
            # 3) Nos quedamos con input de inicio del histórico e introducimos fechas
            # <input class="absolute left-0 top-0 h-full w-full opacity-0" type="date">
            # ---------------------------------------------------------
            input_date = self.e.busqueda_html(fuente=driver,tag='input',s_atributo=['type','date']) 
            input_date.click()
            
            # 4) INTRODUCIMO FEC_INICIO DEL HISTORICO
            # ---------------------------------------------------------
            self.fecha_objetivo ( input_date, 
                             year_obj = fec_ini[0], 
                             month_obj = fec_ini[1],
                             day_obj = fec_ini[2] )
                 
            # 5) BOTON ACEPTAR
            # ---------------------------------------------------------
            selector = 'flex cursor-pointer items-center gap-3 rounded bg-v2-blue pl-4 pr-6 shadow-button'
            boton_aceptar = self.e.busqueda_html (fuente=driver,tag='div',s_class=selector) 
            boton_aceptar.click()
    
            # 5) Fechas introducidas
            print(' + Fechas inicio y fin del historico introducidas: ' + menu.text)
                            
        # 2) ['FI'] => De Yahoo Finace
        # -------------------------------------------
        elif tipo_valor in ['FIs']:
            
            # 0) Numero de filas inicial:
            # <table class="table yf-ewueuo">
            # ---------------------------------------------------------
            selector = 'table yf-ewueuo'
            data_table = self.e.busqueda_html(fuente=driver,tag='table',s_class=selector)         
            filas_ini = len(self.e.busqueda_html(fuente=data_table,tag='tr',n=True))
            
            # 1) Abrimos desplegable de los inputs de fecha
            # <button class="tertiary-btn fin-size-small menuBtn rounded yf-2hwppo">
            # ---------------------------------------------------------
            selector = 'tertiary-btn fin-size-small menuBtn rounded yf-2hwppo'        
            menu = self.e.busqueda_html(fuente=driver,tag='button',s_class=selector) 
            menu.click()
            
            # 2) Con el menu desplegado seleccionamos "fecha inicio"
            # <input type="date" name="startDate">
            # ---------------------------------------------------------
            input_date = self.e.busqueda_html(fuente=driver,tag='input',s_atributo=['name','startDate']) 
            print(fec_ini)
            
            input_date.send_keys(str(fec_ini[2]).zfill(2))
            #input_date.send_keys(Keys.TAB)
            sleep(0.5)
            
            input_date.send_keys(str(fec_ini[1]).zfill(2))
            #input_date.send_keys(Keys.TAB)
            sleep(0.5)
            
            input_date.send_keys(str(fec_ini[0]))
            sleep(0.5)
                    
            # 3) Aceptamos para cerrar el menu y listo
            # <button class="primary-btn fin-size-small rounded yf-2hwppo">
            # ---------------------------------------------------------
            selector = 'primary-btn fin-size-small rounded yf-2hwppo'        
            ok = self.e.busqueda_html(fuente=driver,tag='button',s_class=selector) 
            ok.click()
            
            # Despues de introducir las fechas, las leemos para verificacion
            fechas = menu.text.split(' - ')
            fec_ini = str(datetime.strptime(fechas[0], '%b %d, %Y').date())
            fec_fin = str(datetime.strptime(fechas[1], '%b %d, %Y').date())
            
            print(' + Fechas inicio y fin del historico introducidas: ' + fec_ini + ' - ' + fec_fin)
             
        else:
            print('Procesamiento no disponible para el valor introducido')
            
        return filas_ini
        
    # -----------------------------------------------------------------------
    
    def inputs_fecha_hoy(self,driver,tipo_valor):
        
        # Para volver a fecha actual despues de introducir inputs y asi poder
        # introducir nuevos inputs y añadir datos de cotizacion faltantes => para
        # llegar a la fecha objetivo => el mapeo inicia en "current date"
        
        if tipo_valor not in ['FIs']:
            
            # 1) SELECTOR DEL MENU DE INPUTS DE FECHA + PROCESAMIENTO
            # ---------------------------------------------------------
            selector = 'flex flex-1 items-center rounded border border-solid bg-white py-2 shadow-select'
            menus = self.e.busqueda_html(fuente=driver,tag='div',s_class=selector,n=True) 
            
            # 2) En variable "menus" tenemos menu "PLAZO" y menu de "INPUTS DATE" por coin-
            # cidencia de selectores => recorremos y nos quedamos con los que tengan el 
            # año actual en el contenido de la etiqueta:
            # ---------------------------------------------------------
            for ind,menu in enumerate(menus):
                if ind==1:
                    menu.click()
                    break
                
            # 3) Nos quedamos con input de inicio y pulsamos tecla "hoy" del desplegable
            # ---------------------------------------------------------        
            input_date = self.e.busqueda_html(fuente=driver,tag='input',s_atributo=['type','date']) 
            
            # Menu de fec_inicio desplegado
            input_date.click()
            # Dos tabuladores + INTRO sobre boton "hoy"
            input_date.send_keys(Keys.TAB)
            input_date.send_keys(Keys.TAB)
            input_date.send_keys(Keys.ENTER)
                            
            # 5) BOTON ACEPTAR
            # ---------------------------------------------------------
            selector = 'flex cursor-pointer items-center gap-3 rounded bg-v2-blue pl-4 pr-6 shadow-button'
            boton_aceptar = self.e.busqueda_html(fuente=driver,tag='div',s_class=selector) 
            boton_aceptar.click()
                            
        elif tipo_valor in ['FIs']:
            print()
        else:
            print('Procesamiento no disponible para el valor introducido')
            
    # -----------------------------------------------------------------------
    
    # Para obtener el par y la bolsa que aparecerán en la tabla histórico
    def clave(self,driver,tipo_valor):

        par = ''
        bolsa = ''

        if tipo_valor in ['ACCIONES','INDICES','ETFs']:
        
            # Obtención del tick del valor:
            # <h1 class="mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr">
            # ---------------------------------------
            selector = 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'
            elemento_html = self.e.busqueda_html(fuente=driver,tag='h1',s_class=selector) 
            
            tick = elemento_html.text.split('(')[1].split(')')[0].upper()
                
            # Obtención del par VALOR/DIVISA:
            # <div class="flex items-center pb-0.5 text-xs/5 font-normal'>
            # ---------------------------------------
            selector = 'flex items-center pb-0.5 text-xs/5 font-normal'
            elemento_html = self.e.busqueda_html(fuente=driver,tag='div',s_class=selector) 
            elemento_html = self.e.busqueda_html(fuente=elemento_html,tag='span') 
            
            par = tick + '/' + elemento_html.text.upper()
            
            # Obtencion de la bolsa => cod_bolsa
            # <span class="">
            selector = 'flex-shrink overflow-hidden text-ellipsis text-xs/5 font-normal'
            elemento_html = self.e.busqueda_html(fuente=driver,tag='span',s_class=selector) 

            bolsa = elemento_html.text.upper()
                
        elif tipo_valor in ['DIVISAS']:
            
            # Obtención del tick y par del valor:
            # <h1 class="mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr
            # ---------------------------------------
            selector = 'text-left text-xl font-bold leading-7'
            elemento_html = self.e.busqueda_html(fuente=driver,tag='h1',s_class=selector)
        
            par = elemento_html.text.split(' ')[0].upper()
            bolsa = ''
            
        elif tipo_valor in ['CRIPTOMONEDAS']:
            
            # Obtención del tick y par del valor:
            # <h1 class="mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr">
            # -------------------------------------------------------------------------            
            selector = 'text-left text-xl font-bold leading-7'
            elemento_html = self.e.busqueda_html(fuente=driver,tag='h1',s_class=selector)
            
            par = elemento_html.text.split(' ')[0].upper()
            
            # Obtencion de la bolsa => cod_bolsa
            # <span class="">
            selector = 'flex-shrink overflow-hidden text-ellipsis text-xs/5 font-normal'
            elemento_html = self.e.busqueda_html (fuente=driver,tag='span',s_class=selector) 

            bolsa = elemento_html.text.upper()

        else:
            print('aaaaaa')
            
        return par,bolsa
    
    def extraer_historico (self,driver,tipo_valor,filas_ini):
        
        print(' + Esperando a que se descarguen los datos...')
    
        selector = 'freeze-column-w-1 w-full overflow-x-auto text-xs leading-4'    
        try:
            data_table = self.e.busqueda_html(fuente=driver,tag='table',w=True,s_class=selector)
        except TimeoutException:
            # Por si tarda demasiado en cargar
            data_table = self.e.busqueda_html(fuente=driver,tag='table',w=True,s_class=selector)
            
        # Esperamos a que todos los registros esten en la tabla 
        filas = self.e.busqueda_html(fuente=data_table,tag='tr',w=True,n=True)
            
        # HASTA QUE NO SE CARGEN TODOS LOS DATOS, SEGUIMOS EN EL BUCLE
        while len(filas) == filas_ini:
            
            # Cada dos segundos leemos la tabla para determinar su numero de filas 
            # Cuando el numero de filas ha cambiado respecto a la lectura inicial
            # salimos del bucle
            
            filas = self.e.busqueda_html(fuente=data_table,tag='tr',n=True)
            print('      Filas iniciales = ' + str(filas_ini) + ', filas cargadas = ' + str(len(filas)))
            
            # Damos tiempo a que cargue
            sleep(2)
            
        # y parsemaos documento hmtl => mucho más rapido
        parser = self.e.inicio(elemento=data_table,close_driver=False)
        filas = self.e.busqueda_html(fuente=parser,tag='tr',n=True)
                       
        # PARA CONSTRUIR DATASET
        dias_semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
        columnas = ['PAR','TICK','BOLSA','FECHA','DIA_SEMANA','CIERRE','APERTURA','MAXIMO','MINIMO','VOLUMEN_NEGOCIADO','VARIACION_PORCENTUAL','TIPO_VALOR']
        datos = []
        par,bolsa = self.clave(driver,tipo_valor)
        
        aux_tipo_valor = ''
        if tipo_valor == 'CRIPTOMONEDAS':
            aux_tipo_valor = 'CRIPTOMONEDA'
        elif tipo_valor == 'ACCIONES':
            aux_tipo_valor = 'ACCION'
        elif tipo_valor == 'ETFs':
            aux_tipo_valor = 'ETF'
        elif tipo_valor == 'INDICES':
            aux_tipo_valor = 'INDICE'
        elif tipo_valor == 'DIVISAS':
            aux_tipo_valor = 'DIVISA'
        elif tipo_valor == 'FIs':
            aux_tipo_valor = 'FI'
        else:
            None
        
        # todo el contenido ya se ha terminando de descargar al pseudonavegador 
        # de selenium => bucle for para recorrer todas las filas de la tabla
        for ind,fila in enumerate(filas):
                        
            # DATOS => 1 fila por "tr"
            #------------------------------------------------------------
            if fila != []:
                vector = [par,par.split('/')[0],bolsa]
                td = self.e.busqueda_html(fuente=fila,tag='td',n=True)
                for ind,data in enumerate(td):
                                
                    # Fecha (y añadimos dia de la semana)
                    if ind == 0:
                        if data.text != '':
                            if '.' in data.text:
                                aux = datetime.strptime(data.text, '%d.%m.%Y').date()
                            else:
                                aux = datetime.strptime(data.text, '%m/%d/%Y').date()
                            vector.append(aux) 
                            vector.append(dias_semana[aux.weekday()])
                            
                        else: vector.append(None) 
                        
                    elif ind==6:  
                        if data.text != '':
                            aux = data.text.split('%')[0]
                            vector.append(round(float(aux),2))
                        else: vector.append(None) 
                        
                    else:         # resto => eliminamos '.' y luego cambiamos '.' por ','
                        if data.text != '':
                            if 'K' in data.text.upper():
                                aux = data.text.upper().split('K')[0].replace(',','.')
                                vector.append(float(aux)*1000)
                            elif 'M' in data.text.upper():
                                aux = data.text.upper().split('M')[0].replace(',','.')
                                vector.append(float(aux)*1000000) 
                            elif 'B' in data.text.upper():
                                aux = data.text.upper().split('B')[0].replace(',','.')
                                vector.append(float(aux)*1000000000) 
                            else:
                                aux = data.text.replace('.','').replace(',','.')
                                vector.append(float(aux))
                        else: vector.append(None) 
                vector.append(aux_tipo_valor)            
                datos.append(vector)
                    
        datos = [elemento for elemento in datos if elemento and len(elemento) == len(columnas)]      
        print('      Total columnas extraidas... ' + str(len(columnas)))
        print('      Total registros extraidas... ' + str(len(datos)))
        print('')
        return datos,columnas

    # -----------------------------------------------------------------------

    def carga_inicial_FI(self,archivo,clave):
                   
        # PARA CONSTRUIR datosSET
        dias_semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
        columnas = ['PAR','TICK','BOLSA','FECHA','DIA_SEMANA','CIERRE','APERTURA','MAXIMO','MINIMO','VOLUMEN_NEGOCIADO','VARIACION_PORCENTUAL','TIPO_VALOR']
        datos = []
        
        with open(self.e.ruta_FIs+archivo, 'r') as file:
            reader = csv.reader(file)
            datos = [row for row in reader]
            
        # Eliminamos cabeceras
        datos = datos[1:len(datos)]
        
        # PROCESAMIENTO DE REGISTROS
        for ind,array in enumerate(datos):
            # 0) AÑADIMOS PAR, TICK y bolsa
            array.insert(0,clave[0])
            array.insert(1,clave[0].split('/')[0])
            array.insert(2,clave[1])
            # 1) CONVERTIMOS FECHA
            aux = datetime.strptime(array[3], '%d.%m.%Y').date()
            array[3] = aux
            # 2) DIA_SEMANA
            array.insert(4,dias_semana[aux.weekday()])
            # 3) CIERRE: es la del dia (registro que se procesa)
            array[5] = float(array[5].replace(',','.'))
    
        # ORDENAMOS SEGUN FECHA (2a componente de cada array tras añadir el par)
        datos = sorted(datos, key=lambda x: x[3])   
     
        # Ahora la primera componente es el dato más antiguo => su precio de 
        # cierre es el de apertura del siguiente => para calculo var. %
        cierre_anterior = None
        for ind,array in enumerate(datos):
            if ind == 0:
                # Para calcular variacion segundo registro
                cierre_anterior = array[5]
                array[6] = None
                array[7] = None
                array[8] = None
                array[9] = None
                array.insert(10,None)
                array.insert(11,'FI')
            else:
                # 4) APERTURA (es el de cierre del dia anterior )  
                array[6] = cierre_anterior # (array[4] = apertura[N]) = cierre[N-1]
                cierre_anterior = array[5]
                # 6) MAXIMO
                array[7] = None
                # 7) MINIMO
                array[8] = None
                # 8) VOLUMEN_NEGOCIADO (como sobrescribimos, almacenamos comp. 7)
                variacion = array[9]
                array[9] = None
                # 9) VARIACION_PORCENTUAL
                variacion = float(variacion.replace('%','').replace(',','.'))
                array.insert(10,round(variacion,2))
                # 10) tipo_valor
                array.insert(11,'FI')
            
        print('      Total columnas extraidas... ' + str(len(columnas)))
        print('      Total registros extraidas... ' + str(len(datos)))
            
        return datos, columnas
        
    # -----------------------------------------------------------------------

    def extraer_historico_FI (self,driver,clave,filas_ini):
        
        # <table class="table yf-ewueuo"> => De Yahoo Finace
        # ---------------------------------------------------
        selector = 'table yf-ewueuo'    
        data_table = self.e.busqueda_html(fuente=driver,tag='table',w=True,s_class=selector)
        # Esperamos a que todos los registros esten en la tabla 
        filas = self.e.busqueda_html(fuente=data_table,tag='tr',w=True,n=True)
            
        # HASTA QUE NO SE CARGEN TODOS LOS DATOS, SEGUIMOS EN EL BUCLE
        contador = 0
        while len(filas) == filas_ini:
            
            # Cada dos segundos leemos la tabla para determinar su numero de filas 
            # Cuando el numero de filas ha cambiado respecto a la lectura inicial
            # salimos del bucle
            
            filas = self.e.busqueda_html(fuente=data_table,tag='tr',n=True)
            print('      Filas iniciales = ' + str(filas_ini) + ', filas cargadas = ' + str(len(filas)))
            
            # => en caso de que tarde mucho en cambiar => salimos tras 12''
            sleep(2)
            contador+=1
            if contador == 5: # 12 segundos
                break
            
        # y parsemaos elemento data_table => mucho más rapido
        parser = self.e.inicio(elemento=data_table,close_driver=False)
        filas = self.e.busqueda_html(fuente=parser,tag='tr',n=True)
                       
        # PARA CONSTRUIR DATASET
        dias_semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
        columnas = ['PAR','TICK','BOLSA','FECHA','DIA_SEMANA','CIERRE','APERTURA','MAXIMO','MINIMO','VOLUMEN_NEGOCIADO','VARIACION_PORCENTUAL','TIPO_VALOR']
        datos = []
        
        # todo el contenido ya se ha terminando de descargar al pseudonavegador 
        # de selenium => bucle for para recorrer todas las filas de la tabla
    
        for ind,fila in enumerate(filas):
           
            # DATOS => 1 fila por "tr"
            #------------------------------------------------------------
            fecha = None
            cierre = None
            
            # El primer <tr> son las cabeceras
            if fila != [] and ind != 0:
                td = self.e.busqueda_html(fuente=fila,tag='td',n=True)
                for ind,data in enumerate(td):
                    if data.text not in ['','\n','\n\n']:
                        if ind == 0:
                            if ',' in data.text:
                                aux = datetime.strptime(data.text, '%b %d, %Y').date()
                            elif '.' in data.text:
                                aux = datetime.strptime(data.text, '%d.%m.%Y').date()
                            elif '/' in data.text:
                                aux = datetime.strptime(data.text, '%m/%d/%Y').date()
                            else:
                                None 
                        if ind == 4: # Close
                            cierre = float(data.text)
                                       
                # 0,1,2) PAR, TICK y BOLSA
                vector = [clave[0],clave[0].split('/')[0],clave[1]]
                # 3,4) FECHA y DIA_SEMANA         
                vector.append(aux) 
                vector.append(dias_semana[aux.weekday()])
                # 5) cierre => en realidad esta columna se corresponde con open,
                # pero todos los valores del registro son iguales
                vector.append(cierre)
                # 6) aperutra
                vector.append(None)
                # 7,8,9) MAXIMO, MINIMO Y VOLUMEN
                vector.append(None)
                vector.append(None)
                vector.append(None)
                # 10) VAR. %
                vector.append(None)
                # 11) tipo_valor
                vector.append('FI')
                        
                datos.append(vector)
                    
        # ORDENAMOS SEGUN FECHA (2a componente de cada array tras añadir el par)
        datos = sorted(datos, key=lambda x: x[3])
        # LIMPIAMOS
        datos = [elemento for elemento in datos if elemento and len(elemento) == len(columnas)] 
        
        # Ahora la primera componente es el dato más antiguo => su precio de 
        # cierre es el de apertura del siguiente => para calculo var. %
        cierre_anterior = None
        for ind,array in enumerate(datos):
            if ind == 0:
                # Para calcular variacion segundo registro
                cierre_anterior = array[5]
                array[6] = None
                array[7] = None
                array[8] = None
            else:
                # 4) APERTURA (es el de cierre del dia anterior )  
                array[6] = cierre_anterior # (array[4] = apertura[N]) = cierre[N-1]
                cierre_anterior = array[5] # almacenamos cierre[N-1]
                # RESTO IGUAL
                # 8) VARIACION_PORCENTUAL
                if isinstance(array[5],float) and isinstance(array[6],float):
                    # var = (cierre-apertura)/cierre*100 (%)
                    array[10] = round((array[5]-array[6])/array[5]*100,2)
                else:
                    array[10] = None
                            
        print('      Total columnas extraidas... ' + str(len(columnas)))
        print('      Total registros extraidas... ' + str(len(datos)))
        print('')
        return datos,columnas
    
    # -----------------------------------------------------------------------
    
    # EN CASO DE HISTÓRICOS CON UNA PROFUNDIDAD MUY AMPLIA, EN LA PÁGINA HTML 
    # NO SE INCRUSTAN TODAS LAS FECHAS => empezamos en fec_min, una vez scra-
    # peados los datos detectamos FEC_MAX, Y VOLVEMOS A LANZAR ESCRAPEO CON
    # fec_min = FEC_MAX
    def resto_del_historico(self,driver,fec_min,tipo_valor):
               
        # Para poder añadir los datos faltantes => necesitamos volver a la 
        # fecha de inicio => el
        self.inputs_fecha_hoy(driver=driver,tipo_valor=tipo_valor)
        # Esperamos a que actulice todo
        sleep(5)
                
        # ESPECIFICAMOS INPUTS DATE DE INVESTING PARA SELEECIONAR LA NUEVA
        # FEC_INICIO
        filas_carga = self.inputs_fecha (driver=driver, 
                                         tipo_valor=tipo_valor, 
                                         fec_ini=[fec_min.year,fec_min.month,fec_min.day])
        # Esperamos a que actulice todo
        sleep(5)
        datos, columnas = self.extraer_historico (driver, tipo_valor, filas_ini=filas_carga)
        
        return datos
    
    # Para lanzar la extracción de los valores segun las urls de cada JSON
    def historico_valor (self,fuente_json,ind,tipo_valor):
                        
        url = fuente_json['HISTORICO']
        
        if tipo_valor == 'FIs':
            
            if self.fec_dato[0] == 2000:
                print('')
                print('**************************************************************')
                print('H_HISTORICO - ' + tipo_valor + ' ' + str(ind) + ' - ' + url[1])
                print('**************************************************************')
            else:
                print('')
                print('**************************************************************')
                print('H_HISTORICO - ' + tipo_valor + ' ' + str(ind) + ' - ' + url[2])
                print('**************************************************************')
        else:
            print('')
            print('**************************************************************')
            print('H_HISTORICO - ' + tipo_valor + ' ' + str(ind) + ' - ' + url)
            print('**************************************************************')
        
        print(' + Esperando a que se extraigan los datos...')
        datos_aux = []
                   
        # FONDOS DE INVERSION
        # --------------------
        if tipo_valor == 'FIs':
            
            # 1) Extraacion del par
            parser = self.e.inicio(url=url[0],quiero_parser=True)            
            
            tick = ''
            selector = 'float_lang_base_1 relativeAttr'
            elemento_html =self.e.busqueda_html(fuente=parser,tag='h1',s_class=selector)
            tick = elemento_html.text.upper().split(' (')[1].split(')')[0]
            
            par = ''
            selector = 'bottom lighterGrayFont arial_11'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='div',s_class=selector)
            elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='span',n=True)
            for ind,elemento in enumerate(elementos_html):
                if ind == 3:
                    par = tick+'/'+elemento.text.upper()
                    break
                
            bolsa = ''
            selector = 'btnTextDropDwn arial_12 bold'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='i',s_class=selector)
            bolsa = elemento_html.text.upper()
            
            # 2) Extracción del histórico
            if self.fec_dato[0] == 2000:
                # carga inicial por fichero .csv => solo pasamos el nombre
                datos_aux,columnas = self.carga_inicial_FI(archivo=url[1],clave=[par,bolsa])
            else:   
                # actualizaciones con yahoo finance
                driver = self.e.inicio(url=url[2],pag='YF',stop=True)
                filas_carga = self.inputs_fecha(driver=driver, tipo_valor=tipo_valor,fec_ini=self.fec_dato)
                datos_aux,columnas = self.extraer_historico_FI(driver=driver, clave=[par,bolsa],filas_ini=filas_carga)
                driver.quit()
                          
        # RESTOS DE VALORES
        # --------------------
        else:
            
            try:
                driver = self.e.inicio(url)
                self.input_granularidad(driver, tipo_valor)
            except TimeoutException:
                # Llegamos aqui si ha habido algun problema al cargar la pagina
                driver.quit()
                del driver
                driver = self.e.inicio(url)
                self.input_granularidad(driver, tipo_valor)
                
            filas_carga = self.inputs_fecha(driver=driver,tipo_valor=tipo_valor,fec_ini=self.fec_dato)
            datos_aux,columnas = self.extraer_historico(driver, tipo_valor, filas_ini=filas_carga)
            
            max_fec_historico = max(datos_aux, key=lambda x: x[3])[3]
            dias_semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
            # Siempre tomamos como referencia 2 dias anteriores al actual
            fec_actual = datetime.now().date() - timedelta(days=2)
            
            # PRIMER DIA HABIL ("A timedelta object represents a duration, the 
            # difference between two datetime or date instances") => si es 
            # sabado o domingo => movemos fec_actual al viernes
            if dias_semana[fec_actual.weekday()] == 'SABADO':
                fec_actual = fec_actual - timedelta(days=1)
            elif dias_semana[fec_actual.weekday()] == 'DOMINGO':
                fec_actual = fec_actual - timedelta(days=2)
                
            # LA CONFORMACIÓN DEL HISTÓRICO TERMINA CUANDO LA FECHA DEL MISMO 
            # MAS ACTUAL COINCIDE CON LA DEFINIDA:
            while max_fec_historico < fec_actual:
                aux = self.resto_del_historico(driver=driver, fec_min=max_fec_historico, tipo_valor=tipo_valor )
                datos_aux.extend(aux)
                max_fec_historico = max(datos_aux, key=lambda x: x[3])[3]
                print(' + Añadiendo restos de filas => ultima fecha maxima: ' + str(max_fec_historico) + ' - fecha actual: ' + str(fec_actual))
                             
            driver.quit()
        return datos_aux,columnas

    def construccion_historico(self,fec_dato=[2000,1,1],mis_valores=[],ticks=[]):
        
        # Fecha de inicio de H_HISTORICO => por defecto será la fecha para el
        # proceso de inicializacion [2000,1,1] => para los proceso de actuali-
        # zacion se utilziara el fec_dato proveniente de query a BD
        self.fec_dato = fec_dato        # [yyyy,m,d]
        self.fec_inicio = fec_dato      # [yyyy,m,d]
        
        if mis_valores == []:
            self.mis_valores = self.e.mis_valores
        else:
            # Para particularizar pa un solo tipo de valor
            self.mis_valores = mis_valores
            
        self.ticks = ticks
        cols = []
        
        # -----------------------------------------------------------------------
        
        for valor in self.mis_valores:
            
            with open(self.e.ruta_fuentes+valor+'.json') as j:
                data_source = json.load(j)
                
            for ind,e_json in enumerate(data_source):
                
                if self.e.act:
                    # Para cargar todo el historico e los procesos de actua-
                    # lizacion cuando se añada un nuevo valor a los json
                    if e_json['PAR'].split('/')[0] not in self.ticks:
                        self.fec_dato = [2000,1,1]
                    else:
                        # fec_dato x parámetro de construccion_historico()
                        self.fec_dato = fec_dato
                        
                datos_aux, columnas = self.historico_valor(fuente_json=e_json, ind=ind, tipo_valor=valor)
                self.datos.extend(datos_aux)
                cols = columnas
                        
        return pd.DataFrame(self.datos,columns=cols)
                