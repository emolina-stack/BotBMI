from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from BOTS.SCRIPTS.upload_file import subir_archivo_desglosado
from utils.loggin_setup import configurar_logging

import os
import logging

logger, ruta_log = configurar_logging(
    nombre_script="subida_bot_recibidos",
    carpeta="logs",
    nivel=logging.DEBUG,
    mostrar_consola=True
)

URL_PATH = "https://www.trancenter.com.ec/IFacturaEcuadorBMI/"

rutas_ig = {
    "IG_FACT":    Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos_Factura.txt"),
    "IG_NC":      Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos_NC.txt"),
    "IG_COMPRET": Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos_CompRet.txt"),
}

rutas_bmi = {
    "BMI_FACT":    Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos_Factura.txt"),
    "BMI_NC":      Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos_NC.txt"),
    "BMI_COMPRET": Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos_CompRet.txt"),
}

rutas_me = {
    "ME_FACT":    Path(r"F:\\Bots\Bot_BMI\DOC_ME\0991433686001_Recibidos.txt"),
    "ME_NC":      Path(r"F:\\Bots\Bot_BMI\DOC_ME\0991433686001_Recibidos (1).txt"),
    "ME_COMPRET": Path(r"F:\\Bots\Bot_BMI\DOC_ME\0991433686001_Recibidos (2).txt"),
}

USERNAME_BMI = "usrBotRecepcionBMI"
PASSWORD_BMI = ":f6#Nd}-rW3ODP"
USERNAME_IG  = "usrBotRecepcionIG"
PASSWORD_IG  = ";?8?Ax@eg^B53o"
USERNAME_ME  = "usrBotRecepcionME"
PASSWORD_ME  = "Ae3Zx1+KzfFAve"


# ─── Helper reutilizable ──────────────────────────────────────────────────────
def _eliminar_archivo(ruta: Path):
    """Elimina un archivo con manejo de errores estándar."""
    try:
        os.remove(str(ruta))
        logger.info(f"Archivo ELIMINADO correctamente: {ruta.name}")
    except PermissionError:
        logger.warning("No se pudo eliminar (archivo en uso o permisos insuficientes)")
    except FileNotFoundError:
        logger.info("El archivo ya no existe (posiblemente eliminado antes)")
    except Exception as e:
        logger.warning(f"Error al eliminar el archivo: {e}")


def _subir_archivo(page, clave: str, ruta: Path):
    """Sube un archivo al input y hace clic en Aceptar. Elimina el archivo si tiene éxito."""
    try:
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files('input[type="file"]', files=str(ruta))
        logger.info(f"Archivo subido: {ruta.name}")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()
        _eliminar_archivo(ruta)
    except Exception as e:
        logger.error(f"Error durante la subida de {clave}: {e}")
        logger.info("→ NO se elimina el archivo para que puedas revisarlo")


def _login(page, username: str, password: str):
    """Realiza el login en la plataforma."""
    page.goto(URL_PATH)
    page.wait_for_timeout(3000)
    logger.info(f"LOGIN — usuario: {username}")
    page.type("#UserName", username, delay=400)
    page.keyboard.press("Tab")
    page.type("#Password", password, delay=400)
    page.keyboard.press("Enter")
    page.wait_for_timeout(5000)
    page.get_by_role("link", name="Carga Documentos Recibidos", exact=True).click()


# ─── Funciones de cada bot ────────────────────────────────────────────────────
def subir_comprobantes_recibidos_ig():
    logger.info("=" * 50)
    logger.info("🟢 BOT IG — Iniciando")
    with Camoufox(window=(1366, 768), headless=False) as browser:#   True para no visualizar pantalla
        page = browser.new_page()
        try:
            _login(page, USERNAME_IG, PASSWORD_IG)

            logger.info("BOT IG — Subiendo Facturas")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "IG_FACT", rutas_ig["IG_FACT"])

            logger.info("BOT IG — Subiendo Notas de Crédito")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "IG_NC", rutas_ig["IG_NC"])

            logger.info("BOT IG — Subiendo Comprobantes de Retención")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "IG_COMPRET", rutas_ig["IG_COMPRET"])
        
        except Exception as ex:
            logger.error(f"❌ BOT IG — Error durante ejecución: {ex}")
            enviar_correo_error(
                subject="Error al subir archivos en IG PRUEBAS",
                body=f"⚠️⚠️ Ocurrio un error al subir los archivos en el portal de IFactura: {ex}"
            )
        
        finally:
            try:
                page.close()
            except Exception:
                pass
    logger.info("✅ BOT IG — Completado")


def subir_comprobantes_recibidos_bmi():
    logger.info("=" * 50)
    logger.info("🔵 BOT BMI — Iniciando")
    with Camoufox(window=(1366, 768), headless=True) as browser:#   True para no visualizar pantalla
        page = browser.new_page()
        try:
            _login(page, USERNAME_BMI, PASSWORD_BMI)

            logger.info("BOT BMI — Subiendo Facturas")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "BMI_FACT", rutas_bmi["BMI_FACT"])

            logger.info("BOT BMI — Subiendo Notas de Crédito")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "BMI_NC", rutas_bmi["BMI_NC"])

            logger.info("BOT BMI — Subiendo Comprobantes de Retención")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "BMI_COMPRET", rutas_bmi["BMI_COMPRET"])

        except Exception as ex:
            logger.error(f"❌ BOT BMI — Error durante ejecución: {ex}")
            enviar_correo_error(
                subject="Error al subir archivos en BMI PRUEBAS",
                body=f"⚠️⚠️ Ocurrio un error al subir los archivos en el portal de IFactura: {ex}"
            )

        finally:
            try:
                page.close()
            except Exception:
                pass
    logger.info("✅ BOT BMI — Completado")


def subir_comprobantes_recibidos_me():
    logger.info("=" * 50)
    logger.info("🟡 BOT ME — Iniciando")
    with Camoufox(window=(1366, 768), headless=True) as browser:#   True para no visualizar pantalla
        page = browser.new_page()
        try:
            _login(page, USERNAME_ME, PASSWORD_ME)

            logger.info("BOT ME — Subiendo Facturas")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "ME_FACT", rutas_me["ME_FACT"])

            logger.info("BOT ME — Subiendo Notas de Crédito")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "ME_NC", rutas_me["ME_NC"])

            logger.info("BOT ME — Subiendo Comprobantes de Retención")
            page.wait_for_timeout(2000)
            _subir_archivo(page, "ME_COMPRET", rutas_me["ME_COMPRET"])

        except Exception as ex:
            logger.error(f"❌ BOT ME — Error durante ejecución: {ex}")
            enviar_correo_error(
                subject="Error al subir archivos en MAS-Ecuador PRUEBAS",
                body=f"⚠️⚠️ Ocurrio un error al subir los archivos en el portal de IFactura: {ex}"
            )

        finally:
            try:
                page.close()
            except Exception:
                pass
    logger.info("✅ BOT ME — Completado")


# ─── Ejecución en paralelo ────────────────────────────────────────────────────
def ejecutar_bots_en_paralelo():
    bots = {
        "BOT_IG":  subir_comprobantes_recibidos_ig,
        "BOT_BMI": subir_comprobantes_recibidos_bmi,
        "BOT_ME":  subir_comprobantes_recibidos_me,
    }

    logger.info("🚀 Iniciando ejecución paralela de los 3 bots")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futuros = {
            executor.submit(fn): nombre
            for nombre, fn in bots.items()
        }

        for futuro in as_completed(futuros):
            nombre = futuros[futuro]
            try:
                futuro.result()
                logger.info(f"✅ {nombre} — Finalizado correctamente")
            except Exception as e:
                logger.error(f"❌ {nombre} — Error inesperado: {e}")

    logger.info("🏁 Todos los bots han finalizado")
