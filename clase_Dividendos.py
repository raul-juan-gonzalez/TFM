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

variable = """

"""

############################################################################# 
############################################################################# 

class Dividendos:
    
    # Constructor
    def __init__(self,entorno,only_one=False):
        
        self.e = entorno
        self.tipo_valor = 'ACCIONES'
        self.fec_dato = []
        self.ticks = []
        self.datos = []
        self.par = ''
        self.tick = ''
        self.only_one = only_one
        
    # -----------------------------------------------------------------------
     
    def extraer_par(self,url):
         
        tick = ''
        divisa = ''
        
        driver = self.e.inicio(url=url,close_driver=False)
         
        # Obtencio de la divisa:
        # <div class="bottom lighterGrayFont arial_11">
        # --------------------------------------------
        selector = 'bottom lighterGrayFont arial_11'
        elemento = self.e.busqueda_html(fuente=driver,tag='div',s_class=selector)
        
        elementos_html =  self.e.busqueda_html(fuente=elemento,tag='span',n=True)
        for ind,elemento in enumerate(elementos_html):
            if ind == 3 and elemento.text != '':
                divisa = elemento.text.upper()
            
        # Obtencion del tick
        # <h1 class="float_lang_base_1 relativeAttr">
        # ------------------------------------------
        selector = 'float_lang_base_1 relativeAttr'
        elemento = self.e.busqueda_html(fuente=driver,tag='h1',s_class=selector)
        tick = elemento.text.upper().split(' (')[1].split(')')[0]
        
        driver.quit()
                
        self.tick = tick
        self.par = tick+'/'+divisa
    
    # -----------------------------------------------------------------------
    
    def corrector_fecha(self,aux,lan):
        
        # convertimos al ingles
        if lan == 'ESP':
            
            if aux[1] == 'ene':
                fec = aux[0]+' '+'jan'+' '+aux[2]
            elif aux[1] == 'feb':
                fec = aux[0]+' '+'feb'+' '+aux[2]
            elif aux[1] == 'mar':
                fec = aux[0]+' '+'mar'+' '+aux[2]
            elif aux[1] == 'abr':
                fec = aux[0]+' '+'apr'+' '+aux[2]
            elif aux[1] == 'may':
                fec = aux[0]+' '+'may'+' '+aux[2]
            elif aux[1] == 'jun':
                fec = aux[0]+' '+'jun'+' '+aux[2]
            elif aux[1] == 'jul':
                fec = aux[0]+' '+'jul'+' '+aux[2]
            elif aux[1] == 'ago':
                fec = aux[0]+' '+'aug'+' '+aux[2]
            elif aux[1] == 'sept':
                fec = aux[0]+' '+'sep'+' '+aux[2]
            elif aux[1] == 'oct':
                fec = aux[0]+' '+'oct'+' '+aux[2]
            elif aux[1] == 'nov':
                fec = aux[0]+' '+'nov'+' '+aux[2]
            elif aux[1] == 'dic':
                fec = aux[0]+' '+'dec'+' '+aux[2]
                
        # convertimos al espaniol
        elif lan == 'ENG':
            
            if aux[1] == 'jan':
                fec = aux[0]+' '+'ene'+' '+aux[2]
            elif aux[1] == 'feb':
                fec = aux[0]+' '+'feb'+' '+aux[2]
            elif aux[1] == 'mar':
                fec = aux[0]+' '+'mar'+' '+aux[2]
            elif aux[1] == 'apr':
                fec = aux[0]+' '+'abr'+' '+aux[2]
            elif aux[1] == 'may':
                fec = aux[0]+' '+'may'+' '+aux[2]
            elif aux[1] == 'jun':
                fec = aux[0]+' '+'jun'+' '+aux[2]
            elif aux[1] == 'jul':
                fec = aux[0]+' '+'jul'+' '+aux[2]
            elif aux[1] == 'aug':
                fec = aux[0]+' '+'ago'+' '+aux[2]
            elif aux[1] == 'sep':
                fec = aux[0]+' '+'sept'+' '+aux[2]
            elif aux[1] == 'oct':
                fec = aux[0]+' '+'oct'+' '+aux[2]
            elif aux[1] == 'nov':
                fec = aux[0]+' '+'nov'+' '+aux[2]
            elif aux[1] == 'dec':
                fec = aux[0]+' '+'dic'+' '+aux[2]
            
        return fec

    
    def displays(self,url):
        
        driver = self.e.inicio(url=url,pag='YF',close_driver=False)
                
        # 1) Dividendos:
        # --------------
        elemento = self.e.busqueda_html(fuente=driver,tag='div',s_atributo=['data-test','select-container'])
        elemento.click()
        
        # Solo funcion con headles=True
        display = self.e.busqueda_html(fuente=driver,tag='div',s_atributo=['data-test','historicalFilter-menu'])
        options = self.e.busqueda_html(fuente=display,tag='span',n=True)
        for option in options:
            # print(option.text.upper())
            if 'SOLO DIVIDENDOS' in option.text.upper():
                option.click()
                break

        # 2) La opcion "solo dividendos" ya se ha seleccionado => introducimos
        # las fechas
        # --------------------------------------------------------------------
    
        # Nos ubicamos en la seccion para acotar busqueda de elementos
        # <section .... data-test="qsp-historical">
        section = self.e.busqueda_html(fuente=driver,tag='section',s_atributo=['data-test','qsp-historical'],w=True)
        # print(section.text[:50])
        
        # Desplegamos el menu
        fecha_actual = datetime.now().strftime('%d %b %Y').lower().split(' ')
        fecha_actual = self.corrector_fecha(aux=fecha_actual,lan='ENG')
        spans = self.e.busqueda_html(fuente=section,tag='span',n=True,w=True)
        
        for span in spans:
            if 'PERIODO DE TIEMPO' not in span.text.upper() and fecha_actual.upper() in span.text.upper():
                #print(span.text.upper())
                span.click()
                break
    
        # Con el menu ya desplegado seleccionamos "fecha inicio"
        # <input type="date" name="startDate">
        # ---------------------------------------------------------
        fec_dato = []
        if fec_dato != []:
            input_date = self.e.busqueda_html(fuente=driver,tag='input',s_atributo=['name','startDate']) 
            
            input_date.send_keys(str(fec_dato[2]))
            input_date.send_keys(Keys.TAB)
            
            input_date.send_keys(str(fec_dato[1]))
            input_date.send_keys(Keys.TAB)
            sleep(0.5)
            
            input_date.send_keys(str(fec_dato[0]))
            sleep(0.5)
            
            # Y pulsamos boton aceptar leyendo todos los botone en *section*
            botones = self.e.busqueda_html(fuente=section,tag='button',n=True)
            for boton in botones:
                if 'LISTO' in boton.text.upper():
                    #print(boton.text.upper())
                    boton.click()
                    break
        else:
           boton_max = self.e.busqueda_html(fuente=section,tag='button',s_atributo=['data-value','MAX'])
           boton_max.click()
    
        # 2) Boton *aplicar* para envio formulario utilizando lectura anterio
        # --------------------------------------------------------------------
        botones = self.e.busqueda_html(fuente=section,tag='button',n=True)
        for boton in botones:
            if 'APLICAR' in boton.text.upper():
                #print(boton.text.upper())
                boton.click()
                break
            
        sleep(5)
        table = self.e.busqueda_html(fuente=driver,tag='table',s_atributo=['data-test','historical-prices'],w=True)
        filas = self.e.busqueda_html(fuente=table,tag='tr',n=True)
            
        parser = self.e.inicio(elemento=table)
        return parser
        
    # scrapeo de los dividendos todo a traves del parser
    # ----------------------------------------------------------------
    def dividendos(self,parser):
    
        columnas = ['TICK','FEC_DIVIDENDO','DIVIDENDO']
        datos = []

        filas = self.e.busqueda_html(fuente=parser,tag='tr',n=True)
        for ind,fila in enumerate(filas):
            vector = [self.tick]
            if ind != 0 and ind!=len(filas)-1:
                td = self.e.busqueda_html(fuente=fila,tag='td',n=True)
                for ind,data in enumerate(td):
                    #print(str(ind)+data.text)
                    if ind == 0:
                        
                        if '.' in data.text:
                            aux = datetime.strptime(data.text, '%d.%m.%Y').date()
                            vector.append(aux)
                        elif '/' in data.text:
                            aux = datetime.strptime(data.text, '%m/%d/%Y').date()
                            vector.append(aux)
                        else:
                            aux = data.text.lower().split(' ')
                            fec = self.corrector_fecha(aux=aux,lan='ESP')
                            aux = datetime.strptime(fec, '%d %b %Y').date()
                            vector.append(aux)
                            
                    else:
                        aux = ud(data.text.replace(',','.'))
                        aux = round(float(re.sub(r'[^0-9/.]', '',aux)),4)
                        vector.append(aux)
                datos.append(vector)
                
        if self.e.act:
            if self.fec_dato != []:
                filtrados = [array for array in datos if array[1].year >= self.fec_dato[0]] 
                datos = filtrados
            else:
                None
        return datos,columnas

    # ----------------------------------------------------------------
    def construccion_historico(self,fec_dato=[],ticks=[]):
        
        with open(self.e.ruta_fuentes+self.tipo_valor+'.json') as j:
            data_source = json.load(j)
            
        for ind,elemento in enumerate(data_source):
            
            datos_aux = []
            url = elemento['DIVIDENDOS']
            if elemento['PAR'].split('/')[0] not in ticks:
                self.fec_dato = []
            else:
                self.fec_dato = fec_dato
            
            print('')
            print('**************************************************************')
            print('H_ACC_DIVIDENDOS - '+self.tipo_valor + ' ' + str(ind) + ' - ' + url[1])
            print('**************************************************************')
            
            print(' + Extrayendo datos ...')
            self.extraer_par(url[0])           
            parser = self.displays(url[1])
            datos_aux,columnas = self.dividendos(parser)
            self.datos.extend(datos_aux)
            print(' + Datos extraidos!!')
            
            if self.only_one:
                break
            
        return pd.DataFrame(self.datos,columns=columnas)