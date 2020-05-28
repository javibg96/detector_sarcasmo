# script de un solo uso para conseguir una bd sobre el sarcasmo en castellano
# utilizo selenium para traducir desde google translator

import src.googletrans_scrap
from googletrans import Translator
import os
from src.config_loader import load_yml,overwrite_yml
import pandas as pd
import time
import translate
from tqdm import tqdm
import logging


def traductor_csv(terminalMethod=False):

    if terminalMethod:
        cfg = metodo_intro_terminal()
    else:
        cfg = load_yml()
    ruta = cfg["ruta"]
    nombre_fin = cfg["nombre_fin"]

    ruta_split = ruta.split("/")
    nombre_ini = ruta_split[-1]
    ruta_fin = ruta.replace(nombre_ini, nombre_fin)
    ruta_temp = ruta.replace(".csv", "-temp.csv")
    google_api = True
    try:
        df = pd.read_csv(ruta)
    except:
        logging.error("fallo leyendo el archivo")
        raise
    columnas = cfg["columnas"]
    columna_a_traducir = cfg["columna_a_traducir"]
    inicio, fin = cfg["inicio"], cfg["fin"]
    df_temp = df[inicio:fin]  # en un test inicial ya he traducido las primeras 6002
    # print(df_temp.head())
    df_clean = df_temp[columnas]
    df_trans = df_clean
    traductor = None
    idioma = cfg["lang"]

    try:
        sentence = "testing google api"
        google_translator = Translator()
        frase = google_translator.translate(sentence, dest=idioma).text
        logging.info(f"{str(frase)} : api OK, continuamos")
    except Exception as e:
        logging.error(f"Error en la API de Google: {e.args}")
        traductor = src.googletrans_scrap.google_trans()
        google_api = False

    for index, row in tqdm(df_clean.iterrows(), total=df_clean.shape[0]):
        sentence = df_clean.iloc[index - inicio][columna_a_traducir]
        try:
            # print(f"frase eng: {sentence}")
            if index - inicio < 1000 and google_api and len(sentence) < 300:
                google_translator = Translator()
                frase = google_translator.translate(sentence, dest=idioma).text
                df_trans = df_trans.replace(sentence, frase)
                # if frase == "":
                # añadir lo de exceso de caracteres y tal
            else:
                try:
                    if traductor is None:
                        traductor = src.googletrans_scrap.google_trans()
                    df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta_temp)
                except Exception as e:
                    logging.error(f"error en sele_translator: {type(e)} : {e.args}, index: {index}")
        except Exception as e:
            logging.error(f"Error con la api de Google: {type(e)} : {e.args}, reintentamos...")
            time.sleep(0.3)
            try:
                if len(sentence) < 300:
                    google_translator = Translator()
                    frase = google_translator.translate(sentence, dest=idioma).text
                    df_trans = df_trans.replace(sentence, frase)
                else:
                    logging.info(f"frase larga ({len(sentence)}, intentamos traduccion con selenium...)")
                    traductor = src.googletrans_scrap.google_trans()
                    df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta_temp)
                    traductor.exit_browser()

            except Exception as e:
                logging.error(
                    f"Segundo intento fallido: {type(e)}: {e.args}, trabajamos con selenium de aqui en adelante\n")
                if traductor is not None:
                    traductor.exit_browser()
                google_api = False
                error_handler()
            traductor = src.googletrans_scrap.google_trans()
            df_trans = sele_translation(traductor, sentence, index, inicio, df_trans, ruta_temp)

    print("\n\n----PROCESO FINALIZADO-------\n")

    df_trad = pd.read_csv(ruta_fin, sep="|")
    print(df_trad.tail())
    df_trad = df_trad.append(df_trans)
    df_trad.to_csv(ruta_fin, sep='|', index=False, header=True)

    traductor.exit_browser()
    # print(df_trans.head())
    cfg["inicio"] = fin
    cfg["fin"] = fin + 4000
    overwrite_yml(cfg)

    if cfg["noche"]:
        os.system("shutdown /s /t 1")  # como tarda mucho, para que se apague solo si lo dejas corriendo x la noche


def sele_translation(traductor, sentence, index, inicio, df_trans, ruta):
    if len(sentence) < 4500:
        frase = traductor.translate_into_esp(sentence)

        if not frase and len(sentence) < 200:
            traductor = translate.Translator(to_lang="es")
            frase = traductor.translate(sentence)
            logging.warning(f"Tweet revisado: \nIndex: {index}\nTweet: {sentence}\ntranslation2: {frase}\n")
        elif frase == df_trans.iloc[index - inicio-1]['parent_comment']:
            logging.warning(f"Tweet a revisar: \nIndex: {index}\nTweet: {sentence}\nBusca FRASE DUPLICADA en .csv\n")
            frase = "FRASE DUPLICADA"
        else:
            time.sleep(0.5)
            if not frase:
                traductor = translate.Translator(to_lang="es")
                frase = traductor.translate(sentence)
                if not frase:
                    logging.warning(
                        f"Tweet a revisar: \nIndex: {index}\nTweet: {sentence}\nLongitud: {len(sentence)}\n")
                else:
                    logging.info(f"traducido como: {frase}, \nfrase original: {sentence}")
    else:
        logging.warning(f"Tweet muy largo: \nIndex: {index}\nTweet: {sentence}\n"
                        f"Longitud: {len(sentence)}\nBusca FRASE MUY LARGA en el .csv\n")
        frase = "FRASE MUY LARGA"
    df_trans = df_trans.replace(sentence, frase)

    if index % 500 == 0 and index != inicio:
        logging.info(f"Ya he traducido hasta la fila {index}\n")
        df_trans.to_csv(ruta, sep='|', index=False, header=True)

    if index % 2000 == 0 and index != inicio:
        # traductor.exit_browser()
        # logging.info("Exit browser...")
        time.sleep(0.6)
        # traductor = src.googletrans_scrap.google_trans()
        # logging.info("Tab re-opened...")

    return df_trans


def error_handler():
    f = open("src/troll.txt", "r")
    print(f.read())
    f.close()
