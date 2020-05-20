# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import googletrans_scrap
import pandas as pd
import logging

df = pd.read_csv("../entreno_sarcasmo/train-balanced-sarcasm.csv")
# sentence = "you are so intense"
# lista = [600, 1000, 2000, 3000, 4000, 5000,9000, 12000, 15000, 18000, 21000, 24000, 27000, 30000, 33000, 36000, 39000]
lista = list([])
for i in range(9, 20):
    lista.append(i*500)
print(lista)
inicio, fin = 2001, 10001
df_temp = df[inicio:fin]  # en un test inicial ya he traducido las primeras 302
print(df_temp.head())
df_clean = df_temp[['label', 'parent_comment']]
df_trans = df_clean
tradutor = googletrans_scrap.google_trans()

for index, row in df_clean.iterrows():
    if index-inicio < fin:
        sentence = df_clean.iloc[index-inicio]['parent_comment']
        try:
            # print(f"frase eng: {sentence}")
            frase = tradutor.translate_into_esp(sentence)
            df_trans = df_trans.replace(sentence, frase)
            if not frase:
                print(f"\n\nCHEEEEEEEEEECK {index}  !!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            if index % 100 == 0:
                print(f"\nYa he traducido {index}\n")
            if index in lista:
                df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-{index}.csv", sep='|', index=False, header=True)
                tradutor.exit_browser()
                tradutor = googletrans_scrap.google_trans()
                print(f"Ya he traducido {index}")

        except:
            logging.exception("Error traceback")
            print(f"\n\nindex con errores:{index}")
            df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-{index}.csv", sep='|', index=False,
                            header=True)
tradutor.exit_browser()
# print(df_trans.head())
print(f"ACUERDATE DE QUE EMPIEZAS EN {inicio}")
