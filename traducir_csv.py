# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:53:51 2020

@author: JBLASCO
"""
import logging
import os
from src.dataset_creator import traductor_csv

try:
    FORMAT = '%(asctime)s--%(levelname)s--%(message)s'
    logging.basicConfig(filename='logs_traductor.log', filemode='a', format=FORMAT, level='INFO')
    terminalMethod = True  # Si quieres añadir los valores por pantalla terminalMethod = True
    if terminalMethod:
        ruta = input("Introduce la ruta del fichero .csv que quieres traducir:\n")
        # ruta = "../entreno_sarcasmo/"

        if ".csv" not in ruta:
            nombre_ini = input("Introduce el nombre del fichero .csv que quieres traducir")
            # nombre_ini = "train-balanced-sarcasm.csv"
            if ".csv" not in nombre_ini:
                nombre_ini = nombre_ini + ".csv"
                ruta = ruta + nombre_ini
        else:
            ruta_split = ruta.split("/")
            nombre_ini = ruta_split[-1]
            print(f"\nNombre del archivo: {nombre_ini}\n")

        nombre_fin = input("Introduce como quieres llamar al fichero traducido:\n")
        # nombre_fin = "train-balanced-sarcasm-temp.csv"
        if ".csv" not in nombre_fin:
            nombre_fin = nombre_fin + ".csv"

        if nombre_fin == nombre_ini:
            nombre_fin = nombre_fin.replace(".csv", "(1).csv")

        idioma = input("\nIntroduce el idioma al que quieres traducir:\n").lower()
        if idioma == "ingles" or idioma == "inglés":
            lang = "en"
            # deberias añadir un .json con los idiomas y las posibles abreviaturas, esto es cutre
        else:
            lang = idioma[0:2]
        n_col = 0
        notInt = True
        while notInt:
            try:
                n_col = int(input("Introduce el número de columnas con las que quieres quedarte del csv:\n"))
                notInt = False
            except ValueError:
                print("Introduce un numero válido")
                continue

        columnas = list([])
        for i in range(0, n_col):
            col = input(f"Introduce el nombre de la columna {i+1}:\n")
            columnas.append(col)
        # col_trans = input("¿Cual es la columna a traducir?: \n")
        # poner un señalizador
        print(f"columnas elegidas: {columnas}, columna a traducir: {columnas[-1]}")

        notInt = True
        inicio, fin = 0, 0
        while notInt:
            try:
                inicio = int(input("\nIntroduce desde que fila quieres empezar a traducir: \n"))
                fin = int(input("\nIntroduce hasta que fila traducir: \n"))
                notInt = False
            except ValueError:
                print("Introduce un numero válido")
        print(f"\nInicio: {inicio}, Fin: {fin}\n")

        checkNoche = input("\nQuieres que me apague al acabar?: \n")
        if checkNoche.lower() == "si" or checkNoche.lower() == "yes":
            os.system("shutdown /s /t 1")   # como tarda mucho, para que se apague solo si lo dejas corriendo x la noche
        else:
            print("\n..Empezamos..")

    else:
        ruta = "../entreno_sarcasmo/train-balanced-sarcasm.csv"
        nombre_fin = "train-balanced-sarcasm-temp.csv"
        lang = "es"
        columnas = ['label', 'parent_comment']
        inicio, fin = 7000, 8000

    traductor_csv(ruta, nombre_fin, lang, columnas, inicio, fin)


except:
    logging.exception("Error traceback")
