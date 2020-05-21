from googletrans import Translator
import translate
import pandas as pd
import logging
import json
import time


# ruta = input("Introduce la ruta del fichero .csv que quieres traducir")
idioma = input("introduce el idioma al que quieres traducir:\n").lower()
if idioma == "ingles" or idioma == "inglés":
    lang = "en"
else:
    lang = idioma[0:2]

# GoogleApi
google_translator = Translator()
traductor = translate.Translator(to_lang="es")

# sentence = "you are such an asshole"

# GoogleApi, si la usas mucho te banean la VPN
# frase = google_translator.translate(sentence, dest='es').text

# frase = translator.translate(sentence)
# print(frase)


df = pd.read_csv("../entreno_sarcasmo/train-balanced-sarcasm.csv")

# La API de google solo te permite 3000!!
inicio = 6001
fin = inicio + 2999

df_temp = df[inicio:fin]
df_clean = df_temp[['label', 'parent_comment']]
df_trans = df_clean
lista = list([])
for i in range(12, 20):
    lista.append(i*500)
list_index_to_check = []


for index, row in df_clean.iterrows():
    if index - inicio < fin:
        sentence = df_clean.iloc[index - inicio]['parent_comment']
        try:
            # GoogleApi, reinicio por errores de VPN
            google_translator = Translator()
            sentence = df_clean.iloc[index]['parent_comment']
            # print(f"frase eng: {sentence}")

            frase = google_translator.translate(sentence, dest="es")

            df_trans = df_trans.replace(sentence, frase)

            if index % 500 == 0:
                print(f"\nYa he traducido {index}\n")
            if index in lista:
                df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-{index}.csv", sep='|', index=False, header=True)
                print(f"Ya he traducido {index}")

        except json.decoder.JSONDecodeError:

            print(sentence)
            frase = traductor.translate(sentence)
            print("\nERROR EN LA API DE GOOGLE, TRADUCIDO POR LA API DE TRADUCCION")
            df_trans = df_trans.replace(sentence, frase)
            list_index_to_check.append(index)
            logging.exception("error traceback")
            raise

print(f"LIST: {list_index_to_check}")
text_file = open("list_to_check.txt", "w")
n = text_file.write(f"LIIST: {list_index_to_check}")
text_file.close()
df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo_googleapi.csv", sep='|', index=False, header=True)
