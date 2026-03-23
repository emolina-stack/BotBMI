from BOTS.bot_bmi import main_bmi
from BOTS.bot_ig import main_ig
from BOTS.bot_me import main_me
from subir_recibidos import ejecutar_bots_en_paralelo
from subir_recibidos import subir_comprobantes_recibidos_bmi
from subir_recibidos import subir_comprobantes_recibidos_me
from utils.loggin_setup import configurar_logging
from utils.keep_user_active import iniciar_hilo_keep_alive

import logging

logger, ruta_log = configurar_logging(
        nombre_script="ejecucion_bot_recibidos_general",
        carpeta="logs",
        nivel=logging.DEBUG,
        mostrar_consola=True
    )

def execute_bots():
    logger.info("===========INICIANDO BOT IG=============")
    iniciar_hilo_keep_alive()
    main_ig()# BOT IG
    logger.info("===========FINALIZADO BOT IG=============")
    logger.info("*********************************************")
    logger.info("===========INICIANDO BOT BMI=============")
    iniciar_hilo_keep_alive()
    main_bmi()# BOT BMI
    logger.info("===========FINALIZADO BOT BMI=============")
    logger.info("===========INICIANDO BOT ME=============")
    iniciar_hilo_keep_alive()
    main_me()# BOT ME
    logger.info("===========FINALIZADO BOT ME=============")

def carga_archivos():
    logger.info("===========INICIANDO CARGA DE ARCHIVOS IGUALAS=============")
    ejecutar_bots_en_paralelo()
    logger.info("===========FINALIZADA CARGA DE ARCHIVOS BMI=============")
    

if __name__ == "__main__":
    iniciar_hilo_keep_alive()
    execute_bots()
    logger.info("*************************************")
    carga_archivos()
