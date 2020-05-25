# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:53:51 2020

@author: JBLASCO
"""
import logging
import os
from src.dataset_creator import traductor_csv
from src.config_loader import load_yml
from src.intro_datos import metodo_intro_terminal

try:
    FORMAT = '%(asctime)s--%(levelname)s--%(message)s'
    logging.basicConfig(filename='logs_traductor.log', filemode='a', format=FORMAT, level='INFO')

    terminalMethod = False  # Si quieres añadir los valores por pantalla terminalMethod = True

    if terminalMethod:
        cfg = metodo_intro_terminal()
    else:
        cfg = load_yml()

    traductor_csv(cfg)

    if cfg["noche"]:
        os.system("shutdown /s /t 1")  # como tarda mucho, para que se apague solo si lo dejas corriendo x la noche

except:
    logging.exception("Error traceback")
