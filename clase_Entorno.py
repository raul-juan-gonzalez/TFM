# -*- coding: utf-8 -*-
"""
@author: Raul Juan González
"""
# directamente en la terminal del sistema operativo
# -------------------------------------------------
#   python --version
#   pip --version
#   python -m pip install --upgrade pip
#   pip freeze
#   pip show mi_modulo

#   pip install spyder-kernels==2.5.*

#   pip install selenium
#   pip install webdriver_manager
#   pip install bs4
#   pip install lxml
#   pip install unidecode

#   pip uninstall pandas
#   pip install -Iv --user pandas==2.2.0

#   pip install psycopg2
#   pip install sqlalchemy 

#   python C:\ruta\mi_script.py
# -------------------------------------------------

import mes
from datetime import date,datetime,timedelta
from time import time,sleep

#############################################################################
#############################################################################

# Para configurar el driver que controlara Google Chrome:
from selenium import webdriver

# Para seleccionar los elementos del navegador sobre los que vamos a 
# interaccionar:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC

# Para simular envios de formularios (etiquetas <input>) y realizar envios
# de teclado ("enter","arrow up",...):
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Excepciones
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException

# Scraping con BeautifulSoup => parseo del codigo fuente
from bs4 import BeautifulSoup as bs
from bs4.element import ResultSet as bs_result_set
from bs4.element import Tag as bs_result_tag
import lxml

# Para procesamiento da texto/datos
import re
from unidecode import unidecode as ud
import pandas as pd
import csv
import json

#############################################################################
#############################################################################

class Entorno:
    
    # Constructor
    def __init__(self,act=False,nav='GC',headless=True,resize=False,fec_dato=[2000,1,1]):
          
        # Para proceso de actualizacion  => act = True
        # Para proceso de inicializacion => act = False
        self.act = act
        
        # -----------------------------------------------------------------
        
        self.ruta_fuentes_externas = './Fuentes de datos - externas/'
        if act:
            # Para subida a BD de produccion => act = True
            self.ruta_fuentes = './Fuentes de datos - produccion/'
            self.ruta_FIs = './Fuentes de datos - produccion/FIs (ficheros planos)/'

        else:
            # Entorno de preproduccion (pruebas y carga inicial) => act = False
            self.ruta_fuentes = './Fuentes de datos - preproduccion/'
            self.ruta_FIs = './Fuentes de datos - preproduccion/FIs (ficheros planos)/'
            
        # -----------------------------------------------------------------

        self.mis_variables = ['e', 'inicializacion',
                              # TDCs
                             'TDC_PAIS','TDC_INDUSTRIA','TDC_SECTOR','TDC_ESTADOS',
                             # HISTORICOS
                             'H_HISTORICO','H_CRIPTO_EMISIONES','H_ACC_DIVIDENDOS','H_ESTADOS_CONTABLES',
                             # DIMENSIONALES
                             'DIM_ACCIONES','DIM_CRIPTOMONEDAS','DIM_ETFs','DIM_FIs','DIM_DIVISAS','DIM_INDICES',
                             'DIM_BOLSA_VALORES','DIM_EXCHANGE_CRIPTO',
                             # SUPER-DIMENSIONALES
                             'SDIM_MERCADOS','SDIM_VALORES',
                             # OTRAS VARIABLES
                             'mis_variables',
                             'mis_valores','headless','lapso','var',
                             'ini','fin']
        
        # -----------------------------------------------------------------
        
        self.nav = nav
        self.resize = resize
        self.headless = headless
        self.lapso = 15
        
        self.driver_path = ''
        self.nav_path = ''
        self.user_agent = ''
        
        self.mis_valores = ['ACCIONES','FIs','ETFs','DIVISAS','CRIPTOMONEDAS','INDICES']
        self.mis_tablas_dim = ['DIM_'+valor for valor in self.mis_valores]

        # Fecha de inicio de H_HISTORICO => por defecto será la fecha para el
        # proceso de inicializacion => para los proceso de actualizacion se
        # utilziara.......    **select distinct min(fec_dato) from historico**
        self.fec_dato = fec_dato
        
    # -----------------------------------------------------------------------
    
    def opciones_driver(self,opts):
        
        opts.add_argument(self.user_agent)
        opts.add_argument('log-level=3')
        opts.binary_location = self.nav_path
        if self.headless:
            # Para evitar el renderizado del navegador
            opts.add_argument('--headless')
            if self.resize:
                # Full HD (FHD) o 1080p
                # Si la página es responsive => si está "minimizada",
                # no aparecen todos los elementos
                opts.add_argument('--window-size=1920,1080')
        if self.resize:
            opts.add_argument('--start-maximized')
            
        # https://github.com/SergeyPirogov/webdriver_manager/issues/664#issuecomment-2247178221
        codigo = """
        driver_path = ChromeDriverManager().install()
        driver_path = ChromeDriverManager(version='').install()
        if driver_path:
            driver_name = driver_path.split('/')[-1]
            if driver_name!="chromedriver.exe":
                driver_path = driver_path.split('/')[0]+"\\chromedriver.exe"
                os.chmod(driver_path, 0o755)
        """
        return opts
    
    def inicializacion_driver (self):
               
        # GOOGLE CHROME => GC
        if self.nav == 'GC':
            
            # Definicion del user agent
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            self.user_agent = 'user-agent=' + user_agent
            
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome  import ChromeDriverManager 
            
            v = '126.0.6478.127'
            punto_exe = 'chrome.exe'
            self.nav_path = 'C:/Program Files/Google/Chrome/Application/'+punto_exe
            opts = Options()
            opts = self.opciones_driver(opts)
            
            self.driver_path = ChromeDriverManager().install()
            driver = webdriver.Chrome (
                service = Service(self.driver_path),
                options = opts
            )
    
             # DevTools listening on ws://127.0.0.1:49531/devtools/browser/409d3070-b1db-4967-911e-5d131b800d36
             # Al inicializar el driver aparece este mensaje al ejecutar nuestro
             # script de pyhton desde el CMD, el cual en spyder no se muestra
        
        # MICROSOFT EDGE => ME
        elif self.nav == 'ME':
            
            # Definicion del user agent
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
            self.user_agent = 'user-agent=' + user_agent
            
            from selenium.webdriver.edge.options import Options
            from selenium.webdriver.edge.service import Service
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            
            punto_exe = '/msedge.exe'
            self.nav_path = 'C:/Program Files (x86)/Microsoft/Edge/Application'+punto_exe
            opts = Options()
            opts = self.opciones_driver(opts)
            
            self.driver_path = EdgeChromiumDriverManager().install()
            driver = webdriver.Edge (
                service = Service(self.driver_path),
                options = opts
            )
        
        else:
            print('Navegador no soportado')
            
        return driver
            
    # -----------------------------------------------------------------------  
    
    def busqueda_html (self,fuente,tag=None,
                       s_class=None,s_id=None,s_atributo=None,
                       n=False,w=False,):
               
        # Arg. fuente puede ser driver de Selenium o parser de BeautifulSoup (bs)
        # -----------------------------------------------------------------------
        # es_parser = False => ha pasado el driver => entra Selenium
        # es_parser = True  => ha pasado el parser (instancia bs) o ha pasado 
        #                      un ResultSet del parser (instancia bs_result) => en-
        #                      tra BeautifulSoup (se ignora wait -w-)
    
        es_parser = isinstance(fuente, bs) or isinstance(fuente,bs_result_set) or isinstance(fuente,bs_result_tag)
        
        # Identificacion de elementos con Selenium/BeautifulSoup:
        # ---------------------------------------------------------
        # s_class    => seleccion de elemento html por 'class'
        # s_id       => seleccion de elemento hmtl por 'id' (ignora 'tag')
        # s_atributo => seleccion de elemento html por 'atributo="valor"'
        
        # Para eliminar las clases del selector que no sean "puras" de css (solo
        # es necesario para scraping con selenium) => estandarizamos el selector 
        # que recibe la funcion => independencia de scraping con bs o selenium
        # ---------------------------------------------------------
        def clases_a_eliminar(elemento):
            filtro = ['.','#','.',':','/']
            return all(c not in filtro for c in elemento)
        
        if tag != None and s_class != None:
            
            if not es_parser:
                # fuente = driver
                element_class = s_class.split(' ')
                element_class = list(filter(clases_a_eliminar, element_class))
                
                element_class  = '.'.join(element_class)
                element_class =  f'{tag}.{element_class}'
                by_elemento = (By.CSS_SELECTOR,element_class)
            else:
                element_class = s_class.split(' ')
                by_elemento = [tag,element_class]
            
        elif tag != None and s_atributo != None:
            atributo = s_atributo[0]
            valor = s_atributo[1]
            
            if not es_parser:
                # fuente = driver
                element_class = f'//{tag}[@{atributo}="{valor}"]'
                by_elemento = (By.XPATH, element_class)
            else:
                # fuente = parser
                atributo_valor = {atributo: valor}
                by_elemento = [tag,atributo_valor]
            
        elif tag != None: # s_class,s_id,s_atributo = None
            if not es_parser:
                # fuente = driver
                by_elemento = [By.TAG_NAME,tag]
            else:
                # fuente = parser
                by_elemento = [tag,'']
                
        elif s_id != None:
            if not es_parser:
                # fuente = driver
                by_elemento = (By.ID,s_id)
            else:
                # fuente = parser
                by_elemento = s_id
                 
        else:
            None
            
        # print(by_elemento)         
        # Busqueda de elementos con Selenium/BeautifulSoup:
        # --------------------------------------------------------- 
        # n => para devolver 1 (False) o todos (True) los elementos
        # w => para esperar a que aparezcan los elementos (True)
            
        if n:
            if not es_parser:
                # fuente = fuente
                if w:
                    elemento = Wait(fuente,self.lapso).until(EC.presence_of_all_elements_located (by_elemento))
                else:
                    elemento = fuente.find_elements(by_elemento[0],by_elemento[1])
            else:
                # fuente = parser and n = True
                if s_class != None:
                    elemento = fuente.find_all(name=by_elemento[0], class_=lambda x: x and set(by_elemento[1]).issubset(x.split()))
                elif s_id != None:
                    # probablemente se use directamente (sin invocar funcion)
                    elemento = fuente.find_all(id=by_elemento) 
                elif s_atributo != None:
                    elemento = fuente.find_all(name=by_elemento[0], attrs=by_elemento[1]) 
                else:
                    # probablemente se use directamente (sin invocar funcion)
                    elemento = fuente.find_all(by_elemento[0])
                
        else:
            if not es_parser:
                # fuente = fuente
                if w:
                    elemento = Wait(fuente,self.lapso).until(EC.presence_of_element_located(by_elemento))
                else:
                    elemento = fuente.find_element(by_elemento[0],by_elemento[1])
            else:
                # fuente = parser and n = False
                if s_class != None:
                    elemento = fuente.find(name=by_elemento[0], class_=lambda x: x and set(by_elemento[1]).issubset(x.split()))
                elif s_id != None:
                    # probablemente se use directamente (sin invocar funcion)
                    elemento = fuente.find(id=by_elemento)
                elif s_atributo != None:
                    elemento = fuente.find(name=by_elemento[0], attrs=by_elemento[1]) 
                else:
                    # probablemente se use directamente (sin invocar funcion)
                    elemento = fuente.find(by_elemento[0])
    
        return elemento
    
    # -----------------------------------------------------------------------
    
    def aceptar_cookies(self,driver,stop,pag='INV',c=1):
            
        contador = 1
    
        try:
            # Esperamos a que la página esté completamente cargada:
            # -----------------------------------------------------
            #   Esperamos a que aparezca el elemento "cookies" en el arbol DOM 
            #   (10 segs para que aparezca => sino excepcion). Una vez que ha 
            #   aparecido, se ejecuta el ** button_cookies **
            #   para poder hacer click
            
            # INVESTING
            if pag.upper() == 'INV':
            
                # Aceptar cookies:
                # <button id="onetrust-accept-btn-handler">Acepto</button>
                # --------------------------------------------------------
                selector = 'onetrust-accept-btn-handler'
                boton_cookies = self.busqueda_html(fuente=driver,s_id=selector,w=True)
                boton_cookies.click()
                if stop:
                    # Pulsacion tecla scape para detener la carga una vez se han
                    # aceptado las cookies
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    
            # Yahoo finance
            elif pag.upper() == 'YF':
                
                # Aceptar cookies:
                # <button type="submit" class="btn secondary accept-all " name="agree" value="agree">
                # --------------------------------------------------------
                selector = 'btn secondary accept-all'
                boton_cookies = self.busqueda_html(fuente=driver,tag='button',s_class=selector,w=True)
                boton_cookies.click()
                if stop:
                    # Pulsacion tecla scape para detener la carga una vez se han
                    # aceptado las cookies
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                
            else:
                None
                          
            
        except TimeoutException:
            
            contador = c + 1
            # Mandamos un par de ESCAPES
            actions = ActionChains(driver) 
            actions.send_keys(Keys.ESCAPE).perform() 
            actions.send_keys(Keys.ESCAPE).perform() 
            
            if contador == 3: 
                print(" + Tiempo máximo excedido")
                return
            else:
                print(" + Esperando a aceptar cookies...")
                self.aceptar_cookies(driver=driver,stop=stop,pag=pag,c=contador)
                
    # -----------------------------------------------------------------------
                
    def pop_up(self,driver):
        
        # Para cerrar el pop up:
            
        # 1) Ventana emergente:
        # <div class="signupWrap js-gen-popup dark_graph">
        # ------------------------------------------------
        selector = 'signupWrap js-gen-popup dark_graph'
        pop_up = self.busqueda_html(fuente=driver,tag='div',s_class=selector)
        
        # 2) boton "close" pop up:
        # <i class="popupCloseIcon largeBannerCloser"></i>
        selector = 'popupCloseIcon largeBannerCloser'
        close = self.busqueda_html(fuente=pop_up,tag='i',s_class=selector)
        close.click()
      
    # -----------------------------------------------------------------------        
      
    def inicio(self,url=None,pag='INV',driver=None,elemento=None,quiero_parser=False,stop=False,close_driver=True):
        
        # OPERATIVA FUNCION INICIO => necesario diferenciar procesamiento entre
        # driver y elemento obtenido del driver:
        # ------------------------------------------------------------------------
            # driver   => codigo fuente en "driver.page_source"
            # elemento => codigo fuente en "elemento.get_attribute('outerHTML'))"
        # ------------------------------------------------------------------------
        """
         1) url                    => obtencion del driver
         1) url,quiero_parser=true => inicializacion y parseo del driver
         3) driver                 => parseo del driver ya inicializado con ante-
                                      rioridad
         4) elemento               => parseo del codigo html asociado a un ele- 
                                      mento ya escrapeado con anterioridad
        """
    
        if url != None and driver == None and elemento == None:
            driver = self.inicializacion_driver()
            driver.get(url)
    
            # Por defecto siempre será investing
            if pag.upper() == 'INV':
                self.aceptar_cookies(driver=driver,pag='INV',stop=stop)                
            elif pag.upper() == 'YF':
                self.aceptar_cookies(driver=driver,pag='YF',stop=stop)
            else:
                # Para obtener driver de otras páginas
                if stop:
                    # para detener la carga de la pagina o cerrar pop ups (tambin
                    # si queremos pagina de investing que no requiera de aceptar 
                    # cookies)
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                else:
                    None       
                    
            if quiero_parser:
                # [url, quiero_parser = True]
                # parsemaos documento hmtl para raspado de datos => la busqueda
                # de elementos es mucho más rapida con bs que con selenium
                parser = bs(driver.page_source,'lxml')
                driver.quit()
                return parser
            else:
                return driver
            
        elif driver != None:
            parser = bs(driver.page_source,'lxml')
            if close_driver:
                driver.quit()
            return parser
            
        elif elemento != None:
            # elemento = elemento html escrapeado => simplemente 
            # parseamos el codigo asociado al elemento en lugar de todo el codigo
            # fuente
            parser = bs(elemento.get_attribute('outerHTML'),'lxml')
            # print(' + Parseo del elemento correcto')
            return parser
        
        else: 
            print('Error en funcion inicio()')