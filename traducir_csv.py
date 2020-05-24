# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:53:51 2020

@author: JBLASCO
"""
import logging
import os
from src.dataset_creator import traductor_csv
from src.intro_datos import metodo_intro_terminal

try:
    FORMAT = '%(asctime)s--%(levelname)s--%(message)s'
    logging.basicConfig(filename='logs_traductor.log', filemode='a', format=FORMAT, level='INFO')

    terminalMethod = False  # Si quieres añadir los valores por pantalla terminalMethod = True

    if terminalMethod:
        [ruta, nombre_fin, lang, columnas, inicio, fin, noche] = metodo_intro_terminal()
    else:
        ruta = "../entreno_sarcasmo/train-balanced-sarcasm.csv"
        nombre_fin = "entrenamiento-equilibrado-sarcasmo-temp.csv"
        lang = "es"
        columnas = ['label', 'parent_comment']
        inicio, fin = 22001, 35001
        noche = True

    traductor_csv(ruta, nombre_fin, lang, columnas, inicio, fin)
    if noche:     # no me digas por que no funciona
        os.system("shutdown /s /t 1")  # como tarda mucho, para que se apague solo si lo dejas corriendo x la noche

except:
    logging.exception("Error traceback")
