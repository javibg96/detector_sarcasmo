# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:53:51 2020

@author: JBLASCO
"""
import logging
from src.dataset_creator import traductor_csv

try:
    # ruta = input("Introduce la ruta del fichero .csv que quieres traducir")
    ruta = "../entreno_sarcasmo/train-balanced-sarcasm.csv"

    idioma = input("introduce el idioma al que quieres traducir:\n").lower()
    if idioma == "ingles" or idioma == "inglés":
        lang = "en"
    else:
        lang = idioma[0:2]

    # n_col = input("introduce el numero de columnas con las que quieres quedarte del csv:\n")
    # for i in range (0, n_col):
        # col = input(f"introduce el nombre de la columna {1}:\n")
        # columnas.append(col)
    # col_trans = input("¿Cual es la columna a traducir?: \n")
    # poner un señalizador

    columnas = ['label', 'parent_comment']

    # inicio = input("\nIntroduce desde que fila quieres empezar a traducir: \n")
    # fin = input("\nIntroduce hasta que fila traducir: \n")
    inicio, fin = 6002, 8000

    traductor_csv(ruta, lang, columnas, inicio, fin)

except:
    logging.exception("Error traceback")
