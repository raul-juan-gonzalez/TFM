# -*- coding: utf-8 -*-
"""
@author: Raul
"""

from selenium.webdriver.common.keys import Keys

def enero (input_date,mes_obj):
    
    if mes_obj in (5,9):
        if mes_obj == 5:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 2:
            None
            # print(mes_obj)
        elif mes_obj == 6:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 3:
            None
            # print(mes_obj)
        elif mes_obj == 7:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj == (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 4:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
            
def febrero (input_date,mes_obj):
    
    if mes_obj in (6,10):
        if mes_obj == 6:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 1:
            None
            # print(mes_obj)
        elif mes_obj == 5:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 3:
            None
            # print(mes_obj)
        elif mes_obj == 7:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 4:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
            
def marzo (input_date,mes_obj):
    
    if mes_obj in (7,11):
        if mes_obj == 7:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 1:
            None
            # print(mes_obj)
        elif mes_obj == 5:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 2:
            None
            # print(mes_obj)
        elif mes_obj == 6:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 4:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')

def abril (input_date,mes_obj):
    print('Procesamiento para mes_obj = abril')
    if mes_obj in (8,12):
        if mes_obj == 7:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 1:
            None
            # print(mes_obj)
        elif mes_obj == 5:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 2:
            None
            # print(mes_obj)
        elif mes_obj == 6:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 4:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
                       
def mayo (input_date,mes_obj):
    
    if mes_obj in (1,9):
        if mes_obj == 1:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 6:
            None
            # print(mes_obj)
        elif mes_obj == 2:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 7:
            None
            # print(mes_obj)
        elif mes_obj == 3:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj == (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 8:
            None
            # print(mes_obj)
        elif mes_obj == 4:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
        
def junio (input_date,mes_obj):
    
    if mes_obj in (2,10):
        if mes_obj == 2:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 5:
            None
            # print(mes_obj)
        elif mes_obj == 1:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 7:
            None
            # print(mes_obj)
        elif mes_obj == 3:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 8:
            None
            # print(mes_obj)
        elif mes_obj == 4:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
        
def julio (input_date,mes_obj):
    
    if mes_obj in (3,11):
        if mes_obj == 3:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 5:
            None
            # print(mes_obj)
        elif mes_obj == 1:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 6:
            None
            # print(mes_obj)
        elif mes_obj == 2:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 8:
            None
            # print(mes_obj)
        elif mes_obj == 4:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
        
def agosto (input_date,mes_obj):
    
    if mes_obj in (4,12):
        if mes_obj == 4:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 5:
            None
            # print(mes_obj)
        elif mes_obj == 1:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 6:
            None
            # print(mes_obj)
        elif mes_obj == 2:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
            
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 7:
            None
            # print(mes_obj)
        elif mes_obj == 3:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')

def septiembre (input_date,mes_obj):
    
    if mes_obj in (1,5):
        if mes_obj == 5:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 10:
            None
            # print(mes_obj)
        elif mes_obj == 6:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
            
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 11:
            None
            # print(mes_obj)
        elif mes_obj == 7:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
            
    elif mes_obj == (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 12:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
    else:
        print('ERROR')
        
def octubre (input_date,mes_obj):
    
    if mes_obj in (2,6):
        if mes_obj == 6:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 9:
            None
            # print(mes_obj)
        elif mes_obj == 5:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 11:
            None
            # print(mes_obj)
        elif mes_obj == 7:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
            
    elif mes_obj in (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 12:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
    else:
        print('ERROR')
            
def noviembre (input_date,mes_obj):
    
    if mes_obj in (3,7):
        if mes_obj == 7:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 9:
            None
            # print(mes_obj)
        elif mes_obj == 5:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 10:
            None
            # print(mes_obj)
        elif mes_obj == 6:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
            
    elif mes_obj in (4,8,12):
        input_date.send_keys(Keys.ARROW_RIGHT)
        if mes_obj == 12:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
    else:
        print('ERROR')

def diciembre (input_date,mes_obj):
    
    if mes_obj in (8,4):
        if mes_obj == 8:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
    
    if mes_obj in (1,5,9):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 9:
            None
            # print(mes_obj)
        elif mes_obj == 5:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        
    elif mes_obj in (2,6,10):
        input_date.send_keys(Keys.ARROW_LEFT)
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 10:
            None
            # print(mes_obj)
        elif mes_obj == 6:
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_UP)
            input_date.send_keys(Keys.ARROW_UP)
            # print(mes_obj)
            
    elif mes_obj in (3,7,11):
        input_date.send_keys(Keys.ARROW_LEFT)
        if mes_obj == 4:
            None
            # print(mes_obj)
        elif mes_obj == 8:
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
        else:
            input_date.send_keys(Keys.ARROW_DOWN)
            input_date.send_keys(Keys.ARROW_DOWN)
            # print(mes_obj)
    else:
        print('ERROR')
        
        
##################################################
##################################################

def seleccion_mes (input_date,mes_obj):
    
    fec_input = input_date.get_attribute('value')
    if '-' in fec_input:
        mes_input = int(fec_input.split('-')[1])
    elif '.' in fec_input:
        mes_input = int(fec_input.split('.')[0])
        
    # print("mes_input = " + str(mes_input))
    
    if mes_input == mes_obj:
        None
        # print('mes_input == mes_obj')
        # print(mes_obj)
    else:
        if mes_input == 1: enero(input_date,mes_obj)
        elif mes_input == 2: febrero(input_date,mes_obj)
        elif mes_input == 3: marzo(input_date,mes_obj)
        elif mes_input == 4: abril(input_date,mes_obj)
        elif mes_input == 5: mayo(input_date,mes_obj)
        elif mes_input == 6: junio(input_date,mes_obj)
        elif mes_input == 7: julio(input_date,mes_obj)
        elif mes_input == 8: agosto(input_date,mes_obj)
        elif mes_input == 9: septiembre(input_date,mes_obj)
        elif mes_input == 10: octubre (input_date,mes_obj)
        elif mes_input == 11: noviembre(input_date,mes_obj)
        elif mes_input == 12: diciembre(input_date,mes_obj)
        else: print('error en funcion mes()')
        
            