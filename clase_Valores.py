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

class Valores:
    
    # Constructor
    def __init__(self,entorno,mis_valores=[],only_one=False):
        
        self.e = entorno
        if mis_valores == []:
            self.mis_valores = entorno.mis_valores
        else:
            # Para particularizar pa un solo tipo de valor
            self.mis_valores = mis_valores
        self.datos = []
        self.cols = []
        self.only_one = only_one 
        
    # -----------------------------------------------------------------------
    
    def nombre(self,url):
        
        try:
            
            driver = self.e.inicio(url=url)
            # <span class="mr-1 flex-grow-0 overflow-hidden text-ellipsis whitespace-nowrap text-base">
            # --------------------------------------------------------           
            selector = 'mr-1 flex-grow-0 overflow-hidden text-ellipsis whitespace-nowrap text-base'
            elemento_html = self.e.busqueda_html(fuente=driver,tag='span',s_class=selector,w=True)
            nombre = ud(elemento_html.text.upper())
            print('     '+nombre)
            driver.quit()
            
            return nombre
        
        except TimeoutException:
            # Por si falla por agun casulla
            driver.quit()
            nombre = self.nombre(url=url)
            return nombre
    
    # -----------------------------------------------------------------------

    def extraer_info(self,parser,tipo_valor):
        
       
        datos = []
        dias_semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
            
        if tipo_valor == 'ACCIONES':
                                
            # Obtención de la url que contien nombre valor:
            # <ul class="arial_12 newBigSubTabs ">
            # ---------------------------------------
            url_nombre = ''
            selector = 'arial_12 newBigSubTabs'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='ul',s_class=selector)
            elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='a',n=True)
            for elemento in elementos_html:
                if 'RESUMEN' in elemento.text.upper():
                    url_nombre = 'https://es.investing.com'+elemento.get('href')
                    
            # Obtención del tick del valor:
            # <h1 class="float_lang_base_1 relativeAttr">
            # ---------------------------------------
            selector = 'float_lang_base_1 relativeAttr'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='h1',s_class=selector)
            tick = elemento_html.text.split('(')[1].split(')')[0].upper()
                                                
            # Obtención de la bolsa donde cotiza el precio extraido:
            # <i class="btnTextDropDwn arial_12 bold">
            # ---------------------------------------
            selector = 'btnTextDropDwn arial_12 bold'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='i',s_class=selector)
            bolsa = elemento_html.text.upper()
                            
            # Sede
            # <span class="float_lang_base_2 text_align_lang_base_2 dirLtr">
            # ---------------------------------------
            sede = ''
            selector = 'float_lang_base_2 text_align_lang_base_2 dirLtr'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='span',s_class=selector)
            elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='span',n=True)
            for ind,elemento in enumerate(elementos_html):
                if ind == 0:
                   sede = elemento.text.upper()
                else:
                    sede = sede + ', ' + elemento.text.upper()
                    
            sede = ud(sede).upper()
            pais_sede = ud(sede).upper().split(',')
            pais_sede = pais_sede[len(pais_sede)-1].lstrip()
                                                
            # Industria y sector:
            # <div class="companyProfileHeader">
            # ---------------------------------------
            industria = ''
            sector = ''
            selector = 'companyProfileHeader'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='div',s_class=selector)   
            elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='a',n=True)
            for ind,elemento in enumerate(elementos_html):
                if ind == 0:
                    industria = elemento.text.upper()
                elif ind == 1:
                    sector = elemento.text.upper()
                else:
                    break
                
            columnas = ['TICK','EMPRESA','BOLSA','SEDE','PAIS_SEDE','INDUSTRIA','SECTOR']
            # datos = [datetime.now().date()]
            datos.append(tick)
            datos.append(self.nombre(url_nombre))
            datos.append(ud(bolsa))
            datos.append(ud(sede))
            datos.append(ud(pais_sede))
            datos.append(ud(industria))
            datos.append(ud(sector))
            
        elif tipo_valor == 'INDICES':
            
            # columnas = ['FEC_DATO','TICK','INDICE','BOLSA','NUM_COMPONENTES']
            
            # Obtención de nombre y tick de valor:
            # <h1 class="float_lang_base_1 relativeAttr">
            # ---------------------------------------
            selector = 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='h1',s_class=selector)
            nombre = ud(elemento_html.text.split(' (')[0].upper())
            tick = elemento_html.text.split('(')[1].split(')')[0].upper()
                                        
            # Obtención de la bolsa donde cotiza el indice:
            # <i class="btnTextDropDwn arial_12 bold">
            # ---------------------------------------
            selector = 'relative flex cursor-pointer items-center gap-3 border-b-2 border-transparent hover:border-[#1256A0] hover:text-[#1256A0]'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='div',s_class=selector)
            bolsa = elemento_html.text.upper()
                    
            # Componentes
            # <div class="mb-12 flex justify-between md:mb-10">
            # ------------------------------------------------
            aux=''
            mercado = ''
            componentes = 0
            selector = 'mb-12 flex justify-between md:mb-10'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='div',s_class=selector)
            elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='a',n=True)
            counter = 0
            for ind,elemento in enumerate(elementos_html):
                if elemento.text != '':
                    if counter == 1:
                        mercado = aux.upper()
                        componentes = int(elemento.text)
                        break
                    aux = elemento.text
                    counter = counter + 1
                    
            columnas = ['FEC_DATO','DIA_SEMANA','TICK','INDICE','BOLSA','PAIS_REFERENCIA','NUM_COMPONENTES']
            
            print('     '+nombre)
            fecha = datetime.now().date()
            datos = [fecha]
            datos.append(dias_semana[fecha.weekday()])
            datos.append(tick)
            datos.append(ud(nombre))
            datos.append(ud(bolsa))
            # mercado = PAIS_REFERENCIA
            if mercado == 'ESPAÑA':
                datos.append('ESPANIA')
            else:
                datos.append(mercado)
            datos.append(componentes)
            
        elif tipo_valor == 'DIVISAS':
            
            # columnas = ['TICK','NOMBRE']
            
            # Obtención de nombre y tick de valor:
            # <h1 class="float_lang_base_1 relativeAttr">
            # ---------------------------------------
            selector = 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='h1',s_class=selector)
            tick = elemento_html.text.split('/')[0].upper()
            nombre = elemento_html.text.split(' ')[2].upper()
            # para eliminar acentos (ud) y caracteres raros (re)
            nombre = re.sub(r'[^a-zA-Z]', '',ud(nombre))
            
            columnas = ['TICK','DIVISA']
            
            print('     '+nombre)
            datos = []
            datos.append(tick)
            datos.append(ud(nombre))
            
        elif tipo_valor == 'CRIPTOMONEDAS':
            
            # columnas = ['FEC_DATO','TICK','NOMBRE','PAR','BOLSA','OFERTA_ACTUAL','OFERTA_MAXIMA']
            
            # Divisa
            # <h1 class="mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr">
            # -------------------------------------------------------------------------
            selector = 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='h1',s_class=selector)
            tick = elemento_html.text.split('/')[0].upper()
            nombre = ud(elemento_html.text.split(' ')[2].upper())
                    
            # BOLSA
            # <span class="flex-shrink overflow-hidden text-ellipsis text-xs/5 font-normal>
            # -------------------------------------------------------------------------       
            selector = 'flex-shrink overflow-hidden text-ellipsis text-xs/5 font-normal'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='span',s_class=selector)
            bolsa = elemento_html.text.upper()
            
            # Emisiones
            # <dd data-test="circulatingSupply">
            # ------------------------
            elemento_html = self.e.busqueda_html(fuente=parser,tag='dd',s_atributo=['data-test','circulatingSupply'])
            oferta_actual = elemento_html.text.upper()
            
            if oferta_actual == '-':
                oferta_actual = ''
            else: 
                por = oferta_actual[len(oferta_actual)-1]
                oferta_actual = oferta_actual.split(tick)[1].split(por)[0]
                oferta_actual = oferta_actual.replace(',','.')
                
                if por.upper() == 'K':
                    oferta_actual = float(oferta_actual)*pow(10,3)
                elif por.upper() == 'M':
                    oferta_actual = float(oferta_actual)*pow(10,6)
                elif por.upper() == 'G':
                    oferta_actual = float(oferta_actual)*pow(10,9)
                elif por.upper() == 'T':
                    oferta_actual = float(oferta_actual)*pow(10,12)
                elif por.upper() == 'P':
                    oferta_actual = float(oferta_actual)*pow(10,15)
                else:
                    oferta_actual = float(oferta_actual)
            
            # Emisiones
            # <dd data-test="maxSupply">
            # ------------------------
            elemento_html = self.e.busqueda_html(fuente=parser,tag='dd',s_atributo=['data-test','maxSupply'])
            oferta_maxima = elemento_html.text.upper()
            
            if oferta_maxima == '-':
                oferta_maxima = ''
            else: 
                por = oferta_maxima[len(oferta_maxima)-1]
                oferta_maxima = oferta_maxima.split(tick)[1].split(por)[0]
                oferta_maxima = oferta_maxima.replace(',','.')
                
                if por.upper() == 'K':
                    oferta_maxima = float(oferta_maxima)*pow(10,3)
                elif por.upper() == 'M':
                    oferta_maxima = float(oferta_maxima)*pow(10,6)
                elif por.upper() == 'G':
                    oferta_maxima = float(oferta_maxima)*pow(10,9)
                elif por.upper() == 'T':
                    oferta_maxima = float(oferta_maxima)*pow(10,12)
                elif por.upper() == 'P':
                    oferta_maxima = float(oferta_maxima)*pow(10,15)
                else:
                    oferta_maxima = float(oferta_maxima)
                    
            columnas = ['FEC_DATO','DIA_SEMANA','TICK','CRIPTOMONEDA','BOLSA','OFERTA_ACTUAL','OFERTA_MAXIMA']
            
            print('     '+nombre)
            fecha = datetime.now().date()
            # Se requiere fecha para construir luego historico de oferta
            datos = [fecha]
            datos.append(dias_semana[fecha.weekday()])
            datos.append(tick)
            datos.append(ud(nombre))
            datos.append(ud(bolsa))
            datos.append(oferta_actual)
            datos.append(oferta_maxima)
                    
        elif tipo_valor in ['ETFs','FIs']:
            
            # columnas = ['FEC_DATO','TICK','FI','ISIN','EMISOR','BOLSA','TIPO_VALOR_SUBYACENTE','SUBYACENTE']
            # columnas = ['FEC_DATO','FEC_INICIO','TICK','ETF','ISIN','EMISOR','BOLSA','TIPO_VALOR_SUBYACENTE',
            #             'CATEGORIA','DES_CATEGORIA','RATING MORNINGSTAR']
            
            # Nombre ETF
            # <h1 class="float_lang_base_1 relativeAttr">
            # -------------------------------------------
            selector = 'float_lang_base_1 relativeAttr'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='h1',s_class=selector)
            nombre = ud(elemento_html.text.upper().split(' (')[0])
            nombre = re.sub(r'[^A-Z0-9\s\+\-]', '',nombre)
            tick = elemento_html.text.upper().split(' (')[1].split(')')[0]
            
            # Bolsa
            # <i class="btnTextDropDwn arial_12 bold">
            # ----------------------------------------
            selector = 'btnTextDropDwn arial_12 bold'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='i',s_class=selector)
            bolsa = ud(elemento_html.text.upper())
                        
            # Resto de campos
            # <div class="general-info">
            # ---------------------------------------------
            mercado = ''
            emisor = ''
            isin = ''
            tipo_valor_subyacente = ''
            subyacente = ''
            
            selector = 'general-info'
            elemento_html = self.e.busqueda_html(fuente=parser,tag='div',s_class=selector)
            elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='span',n=True)
            aux = ''
            for elemento in elementos_html:
                if 'EMISOR' in aux.upper():
                    emisor = ud(elemento.text.upper())
                elif 'ISIN' in aux.upper():
                    isin = elemento.text.upper()
                    if isin == None:
                        isin = ''
                elif 'CLASE DE ACTIVO' in aux.upper():
                    tipo_valor_subyacente = ud(elemento.text.upper())
                elif 'SUBYACENTE' in aux.upper():
                   subyacente = elemento.text.upper()
                   if subyacente == None:
                       subyacente = ''
                   else:
                       subyacente = re.sub(r'[^A-Z0-9\s\+\-]', '', ud(subyacente))
                else:
                    None
                aux = elemento.text
    
            if tipo_valor == 'ETFs':
                
                columnas = ['TICK','ETF','ISIN','EMISOR','BOLSA','TIPO_VALOR_SUBYACENTE','SUBYACENTE']
                
                print('     '+nombre)
                datos = [tick]
                datos.append(ud(nombre))
                datos.append(isin)
                datos.append(emisor)
                datos.append(ud(bolsa))
                datos.append(ud(tipo_valor_subyacente))
                datos.append(ud(subyacente))
                
            elif tipo_valor == 'FIs':
                
                # Añadimos fec_inicio y categoria:
                # <div class="companyProfileHeader">
                # -----------------------
                categoria = ''
                
                selector = 'companyProfileHeader'
                elemento_html = self.e.busqueda_html(fuente=parser,tag='div',s_class=selector)
                elementos_html = self.e.busqueda_html(fuente=elemento_html,tag='div',n=True)
                for ind,elemento in enumerate(elementos_html):
                    
                    # Necesitamos determinar el contenedor de la etiqueta 'p'
                    if 'CATEGORIA' in ud(elemento.text.upper()):
                        categoria = ud(elemento.find('p').text.upper())
                        
                # Ratin morningstar:
                # <i class="morningStarDark"></i>
                # -------------------------------
                selector = 'morningStarDark'
                elementos_html = self.e.busqueda_html(fuente=parser,tag='i',s_class=selector,n=True)
                rating_morningstar = len(elementos_html)
                        
                columnas = ['TICK','FI','ISIN','EMISOR','BOLSA','TIPO_VALOR_SUBYACENTE','CATEGORIA','RATING_MORNINGSTAR']
                
                print('     '+nombre)
                datos = [tick]
                datos.append(nombre)
                datos.append(isin)
                datos.append(emisor)
                # bolsa = region
                datos.append(bolsa)
                datos.append(tipo_valor_subyacente)
                datos.append(categoria)
                datos.append(str(rating_morningstar)+'/5')
                
            else:
                None
                
        else:
            print('aaaaaaaaaabbbbbbbbbbbb')
            
        return datos,columnas

    # -----------------------------------------------------------------------

    def dim_info(self,tipo_valor):
        
        # Para cada JSON (valor) hay que resetearlos
        self.datos = []
        self.cols = []
        
        with open(self.e.ruta_fuentes+tipo_valor+'.json') as j:
            data_source = json.load(j)
                         
        print('')
        for ind,elemento in enumerate(data_source):
            url = elemento['INFO']
            
            print('**************************************************************')
            print('DIM_VALORES - ' + tipo_valor + ' ' + str(ind) + ' - ' + url)
            print('**************************************************************')
    
            parser = self.e.inicio(url,quiero_parser=True)
            aux, self.cols = self.extraer_info(parser=parser,tipo_valor=tipo_valor)
            self.datos.append(aux)
            
            if self.only_one:
                break
                
        return pd.DataFrame(self.datos,columns=self.cols)