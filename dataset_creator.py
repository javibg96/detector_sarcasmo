# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import googletrans_scrap
import pandas as pd
import logging

df = pd.read_csv("../entreno_sarcasmo/train-balanced-sarcasm.csv")
# sentence = "you are so intense"
lista = [1000, 2000, 3000, 4000, 9000, 12000, 15000, 18000, 21000, 24000, 27000, 30000, 33000, 36000, 39000]
tradutor = googletrans_scrap.google_trans()
df_temp = df[900:4000]
print(df_temp.head())
df_clean = df_temp[['label', 'parent_comment']]
df_trans = df_clean

for index, row in df_clean.iterrows():
    sentence = df_clean.iloc[index]['parent_comment']
    try:
        if 300 < index:  # en un test inicial ya he traducido las primeras 102
            # print(f"frase eng: {sentence}")
            frase = tradutor.translate_into_esp(sentence)
            df_trans = df_trans.replace(sentence, frase)
            if index in lista:
                df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-{index}.csv", sep='|', index=False, header=True)
                tradutor.exit_browser()
                tradutor = googletrans_scrap.google_trans()
                print(f"Ya he traducido {index}")
        else:
            df_trans = df_trans.replace(sentence, " ")
    except:
        logging.exception("Error traceback")
        print(f"\n\nindex con errores:{index}")
        df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-{index}.csv", sep='|', index=False,
                        header=True)
tradutor.exit_browser()
# print(df_trans.head())
