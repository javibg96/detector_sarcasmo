# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import src.googletrans_scrap
from googletrans import Translator
import pandas as pd
import logging


def traductor_csv(ruta, nombre_fin, idioma, columnas, inicio, fin):


    google_api = True
    try:
        df = pd.read_csv(ruta)
    except:
        logging.error("fallo leyendo el archivo")
        raise

    if columnas is None:
        columnas = [df[1], df[2]]

    df_temp = df[inicio:fin]  # en un test inicial ya he traducido las primeras 6002
    # print(df_temp.head())
    df_clean = df_temp[columnas]
    df_trans = df_clean
    traductor = None

    try:
        sentence = "testing google api"
        google_translator = Translator()
        frase = google_translator.translate(sentence, dest=idioma)
        print(frase + ": api OK, continuamos")
    except:
        print("\nFallo controlado en la API de Google, asi que empezamos con Selenium")
        traductor = src.googletrans_scrap.google_trans()
        # ponerle un tiempo estimado seria de pro
        google_api = False

    for index, row in df_clean.iterrows():
        sentence = df_clean.iloc[index - inicio]['parent_comment']
        try:
            # print(f"frase eng: {sentence}")
            if index - inicio < 2999 and google_api:
                google_translator = Translator()
                frase = google_translator.translate(sentence, dest=idioma)
                df_trans = df_trans.replace(sentence, frase)
                # if frase == "":
                # añadir lo de exceso de caracteres y tal
            else:
                df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta+nombre_fin)
        except:
            google_api = False
            df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta+nombre_fin)

    print("\n\n----PROCESO FINALIZADO-------\n")
    ruta_temp = "../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo.csv"
    df_trad = pd.read_csv(ruta_temp)
    df_trad = df_trad.append(df_trans)
    df_trad.to_csv(ruta_temp, sep='|', index=False, header=True)
    traductor.exit_browser()
    # print(df_trans.head())
    print(f"ACUERDATE DE QUE EMPIEZASTE EN {inicio}, buen dia")


def sele_translation(traductor, sentence, index, inicio,df_trans, ruta_fin):
    frase = traductor.translate_into_esp(sentence)
    df_trans = df_trans.replace(sentence, frase)
    if not frase:
        print(f"\n\nCHEEEEEEEEEECK {index}  !!!!!!!!!!!!!!!!!!!!!!!!\n\n")
    if index % 500 == 0 and index != inicio:
        print(f"\nYa he traducido {index}\n")

        df_trans.to_csv(ruta_fin, sep='|',
                        index=False, header=True)
    if index % 2000 == 0 and index != inicio:
        traductor.exit_browser()
        traductor = src.googletrans_scrap.google_trans()
        df_trans.to_csv(ruta_fin, sep='|',
                        index=False,
                        header=True)
    return df_trans
