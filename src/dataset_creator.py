# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import src.googletrans_scrap
from googletrans import Translator
import pandas as pd
import logging


def traductor_csv(ruta=None, idioma='es', columnas=None, inicio=0, fin=100):

    if columnas is None:
        columnas = ['label', 'parent_comment']

    google_api = True
    df = pd.read_csv(ruta)

    df_temp = df[inicio:fin]  # en un test inicial ya he traducido las primeras 302
    # print(df_temp.head())

    df_clean = df_temp[columnas]
    df_trans = df_clean

    traductor = src.googletrans_scrap.google_trans()

    try:
        sentence = "testing google api"
        google_translator = Translator()
        frase = google_translator.translate(sentence, dest=idioma)
        print(frase + ": api OK, continuamos")
    except:
        print("todo correcto, google api no funciona asi que trabajamos con Selenium")
        # ponerle un tiempo estimado seria de pro
        google_api = False

    for index, row in df_clean.iterrows():
        sentence = df_clean.iloc[index - inicio]['parent_comment']
        try:
            # print(f"frase eng: {sentence}")
            if index - inicio < 2999 and google_api:
                google_translator = Translator()
                frase = google_translator.translate(sentence, dest=idioma)
                print(frase)
                df_trans = df_trans.replace(sentence, frase)
                # if frase == "":
                # añadir lo de exceso de caracteres y tal
            else:
                df_trans = sele_translation(traductor, sentence, index, df_trans)
        except:
            df_trans = sele_translation(traductor, sentence, index, df_trans)

    traductor.exit_browser()
    # print(df_trans.head())
    print(f"ACUERDATE DE QUE EMPIEZAS EN {inicio}")


def sele_translation(traductor, sentence, index, df_trans):
    frase = traductor.translate_into_esp(sentence)
    df_trans = df_trans.replace(sentence, frase)
    if not frase:
        print(f"\n\nCHEEEEEEEEEECK {index}  !!!!!!!!!!!!!!!!!!!!!!!!\n\n")
    if index % 500 == 0:
        print(f"\nYa he traducido {index}\n")
        df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-temp.csv", sep='|',
                        index=False, header=True)
    if index % 1000 == 0:
        traductor.exit_browser()
        traductor = googletrans_scrap.google_trans()
        df_trans.to_csv(f"../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo-temp.csv", sep='|',
                        index=False,
                        header=True)
    return df_trans
