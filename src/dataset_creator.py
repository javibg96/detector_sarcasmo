# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import src.googletrans_scrap
from googletrans import Translator
import pandas as pd
import time
import translate
from tqdm import tqdm
import logging


def traductor_csv(ruta, nombre_fin, idioma, columnas, inicio, fin):
    ruta_split = ruta.split("/")
    nombre_ini = ruta_split[-1]
    ruta_fin = ruta.replace(nombre_ini, nombre_fin)

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
        frase = google_translator.translate(sentence, dest=idioma).text
        print(str(frase) + ": api OK, continuamos")
    except Exception as e:
        print("\nFallo controlado en la API de Google, asi que empezamos con Selenium")
        logging.error(f"Error en la API de Google: {e.args}")
        traductor = src.googletrans_scrap.google_trans()
        # ponerle un tiempo estimado seria de pro
        google_api = False

    for index, row in tqdm(df_clean.iterrows(), total=df_clean.shape[0]):
        sentence = df_clean.iloc[index - inicio]['parent_comment']
        try:
            # print(f"frase eng: {sentence}")
            if index - inicio < 1000 and google_api and len(sentence) < 200:
                google_translator = Translator()
                frase = google_translator.translate(sentence, dest=idioma).text
                df_trans = df_trans.replace(sentence, frase)
                # if frase == "":
                # añadir lo de exceso de caracteres y tal
            else:
                try:
                    df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta_fin)
                except Exception as e:
                    logging.error(f"error en sele_translator: {type(e)} : {e.args}, index: {index}")
        except Exception as e:
            logging.error(f"Error con la api de Google: {type(e)} : {e.args}")
            print("\nFallo en la API de Google, reintentamos....\n")
            try:
                if len(sentence) < 200:
                    google_translator = Translator()
                    frase = google_translator.translate(sentence, dest=idioma).text
                    df_trans = df_trans.replace(sentence, frase)
                else:
                    if traductor is None:
                        traductor = src.googletrans_scrap.google_trans()
                    df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta_fin)

            except Exception as e:
                logging.error(f"error: {type(e)} : {e.args}")
                google_api = False
                # error_handler()
            traductor = src.googletrans_scrap.google_trans()
            df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta_fin)

    print("\n\n----PROCESO FINALIZADO-------\n")

    ruta_temp = "../entreno_sarcasmo/entrenamiento-equilibrado-sarcasmo.csv"
    df_trad = pd.read_csv(ruta_temp, sep="|")
    print(df_trad.tail())
    df_trad = df_trad.append(df_trans)
    df_trad.to_csv(ruta_temp, sep='|', index=False, header=True)

    traductor.exit_browser()
    # print(df_trans.head())
    print(f"ACUERDATE DE QUE EMPEZASTE EN {inicio}, buen dia")


def sele_translation(traductor, sentence, index, inicio, df_trans, ruta_fin):
    frase = traductor.translate_into_esp(sentence)

    if not frase:
        traductor = translate.Translator(to_lang="es")
        frase = traductor.translate(sentence)
        logging.warning(f"Tweet a revisar: \nIndex: {index}\nTweet: {sentence}\ntranslation2: {frase}\n")

    df_trans = df_trans.replace(sentence, frase)

    if index % 500 == 0 and index != inicio:
        logging.info(f"Ya he traducido hasta la fila {index}\n")
        df_trans.to_csv(ruta_fin, sep='|', index=False, header=True)

    if index % 2000 == 0 and index != inicio:
        traductor.exit_browser()
        # traductor = src.googletrans_scrap.google_trans()
        df_trans.to_csv(ruta_fin, sep='|', index=False, header=True)

    return df_trans


def error_handler():
    f = open("src/troll.txt", "r")
    print(f.read())
    f.close()
