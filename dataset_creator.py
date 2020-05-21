# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import googletrans_scrap
from googletrans import Translator
import pandas as pd
import logging

# ruta = input("Introduce la ruta del fichero .csv que quieres traducir")
idioma = input("introduce el idioma al que quieres traducir:\n").lower()
if idioma == "ingles" or idioma == "inglés":
    lang = "en"
else:
    lang = idioma[0:2]
ruta = "../entreno_sarcasmo/train-balanced-sarcasm.csv"
df = pd.read_csv(ruta)
# lista = [600, 1000, 2000, 3000, 4000, 5000,9000, 12000, 15000, 18000, 21000, 24000, 27000, 30000, 33000, 36000, 39000]
# lista = list([])
# for i in range(7, 20):
#    lista.append(i*500)

# inicio = input("\nIntroduce desde que fila quieres empezar a traducir: \n")
# fin = input("\nIntroduce hasta que fila traducir: \n")
inicio, fin = 5001, 10001

df_temp = df[inicio:fin]  # en un test inicial ya he traducido las primeras 302
# print(df_temp.head())

df_clean = df_temp[['label', 'parent_comment']]
df_trans = df_clean

tradutor = googletrans_scrap.google_trans()

for index, row in df_clean.iterrows():
    if index-inicio < fin-inicio:
        sentence = df_clean.iloc[index - inicio]['parent_comment']
        try:
            # print(f"frase eng: {sentence}")
            if index - inicio < 2999:
                google_translator = Translator()
                frase = google_translator.translate(sentence, dest="es")
                df_trans = df_trans.replace(sentence, frase)
            else:
                frase = tradutor.translate_into_esp(sentence)
                df_trans = df_trans.replace(sentence, frase)
            if not frase:
                print(f"\n\nCHEEEEEEEEEECK {index}  !!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            if index % 500 == 0:
                print(f"\nYa he traducido {index}\n")
                df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-temp.csv", sep='|',
                                index=False, header=True)
            if index % 1000 == 0:
                tradutor.exit_browser()
                tradutor = googletrans_scrap.google_trans()

        except:
            logging.exception("Error traceback")
            print("\nERROR EN LA API DE GOOGLE\n")
            print(f"\n\nindex con errores:{index}")
            df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-temp.csv", sep='|', index=False,
                            header=True)
tradutor.exit_browser()
# print(df_trans.head())
print(f"ACUERDATE DE QUE EMPIEZAS EN {inicio}")
