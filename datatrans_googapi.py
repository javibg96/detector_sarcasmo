from googletrans import Translator
import translate
import pandas as pd
import logging
import json
import time

# GoogleApi
google_translator = Translator()
traductor = translate.Translator(to_lang="es")
sentence = "you are such an asshole"

# GoogleApi, si la usas mucho te banean la VPN
# frase = google_translator.translate(sentence, dest='es').text

# frase = translator.translate(sentence)
# print(frase)


df = pd.read_csv("../entreno_sarcasmo/train-balanced-sarcasm.csv")
df_temp = df.head(500)
df_clean = df_temp[['label', 'parent_comment']]
df_trans = df_clean
list_index_to_check = []


for index, row in df_clean.iterrows():
    try:
        # GoogleApi, reinicio por errores de VPN
        google_translator = Translator()

        if index <= 1000:
            sentence = df_clean.iloc[index]['parent_comment']
            # print(f"frase eng: {sentence}")

            frase = google_translator.translate(sentence, dest="es")

            df_trans = df_trans.replace(sentence, frase)

    except json.decoder.JSONDecodeError:

        print(sentence)
        frase = traductor.translate(sentence)
        print("\nERROR EN LA API DE GOOGLE, TRADUCIDO POR LA API DE TRADUCCION")
        df_trans = df_trans.replace(sentence, frase)
        list_index_to_check.append(index)
        logging.exception("error traceback")
        continue

print(f"LIST: {list_index_to_check}")
text_file = open("list_to_check.txt", "w")
n = text_file.write(f"LIIST: {list_index_to_check}")
text_file.close()
df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo_googleapi.csv", sep='|', index=False, header=True)
