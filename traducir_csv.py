# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:53:51 2020

@author: JBLASCO
"""
import logging
from src.dataset_creator import traductor_csv
from src.intro_datos import metodo_intro_terminal

try:
    FORMAT = '%(asctime)s--%(levelname)s--%(message)s'
    logging.basicConfig(filename='logs_traductor.log', filemode='a', format=FORMAT, level='INFO')

    terminalMethod = False  # Si quieres añadir los valores por pantalla terminalMethod = True

    traductor_csv(terminalMethod)



except:
    logging.exception("Error traceback")
