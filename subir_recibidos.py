from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pathlib import Path
from BOTS.SCRIPTS.upload_file import subir_archivo_desglosado

import os

URL_PATH="https://www.trancenter.com.ec/IFacturaEcuadorBMI/"

FILE_SPLIT=r"F:\Bots\Bot_BMI\DOC_IG\SPLIT_FILES" # RUTA DE ARCHIVOS DIVIDIDOS IG
carpeta = Path(FILE_SPLIT)

partes = sorted(
    carpeta.glob("1791927559001_Recibidos_Factura_parte*.txt")
)

rutas_ig={
    "IG_FACT":partes, #  FACTURAS
    "IG_NC":Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos_NC.txt"),# NOTAS DE CREDITO
    "IG_COMPRET":Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos_CompRet.txt"),#   COMPROBANTES DE RETENCION
}

rutas_bmi={
    "BMI_FACT":Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos_Factura.txt"),#  FACTURAS
    "BMI_NC":Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos_NC.txt"),# NOTAS DE CREDITO
    "BMI_COMPRET":Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos_CompRet.txt"),#   COMPROBANTES DE RETENCION
}

# BMI
USERNAME_BMI="usrBotRecepcionBMI"
PASSWORD_BMI="jK~471|6s*"

# IGUALAS
USERNAME_IG="usrBotRecepcionIG"
PASSWORD_IG="y3677D.7lh"


def subir_comprobantes_recibidos_ig():
    with Camoufox(window=(1366, 768), headless=False) as browser:  # headless=True si no quieres verlo
        page = browser.new_page()
        page.goto(URL_PATH)
        page.wait_for_timeout(3000) 

        print("CARGA DE DOCUMENTOS RECIBIDOS" )
        print("LOGIN")
        page.type("#UserName", USERNAME_IG, delay=400)
        print('INGRESO DE USERNAME: ', USERNAME_IG)

        page.keyboard.press("Tab")
        #Password
        page.type("#Password", PASSWORD_IG, delay=400)
        print('INGRESO DE PASSWORD: *******')
        page.keyboard.press("Enter")

        page.wait_for_timeout(5000)
        print("MENU")

        page.get_by_role("link", name="Carga Documentos Recibidos", exact=True).click()
    #   SUBIDA DE DOCUMENTOS RECIBIDOS FACTURAS


        print("SUBIDA DE DOCUMENTOS RECIBIDOS FACTURAS EN MASIVO")
        for idx, parte in enumerate(rutas_ig["IG_FACT"], 1):
                print(f"[{idx}/{len(rutas_ig['IG_FACT'])}] {parte.name}")
                exito = False
                page.wait_for_selector('input[type="file"]', timeout=20000)
                page.set_input_files('input[type="file"]', files=str(parte))

                page.wait_for_timeout(3000)
                try:
                        # page.locator("#cpCol1_btnAceptar").click()
                        page.locator("#cpCol1_btnCerrar").click()
                        print("   → Guardado/aceptado")
                        exito = True
                except:
                        print("   → No se encontró botón de aceptar, continuando...")
                page.wait_for_timeout(6000)  # tiempo prudencial

                if exito:
                        os.remove(parte)  # eliminar el archivo solo si se subió exitosamente
                        os.remove("F:\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos_Factura.txt")
                        print(f"El Archivo {parte.name} fue eliminado exitosamente")
        
        print("Terminada subida de Facturas divididas")

#   CARGA DE NOTAS DE CREDITO
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS NOTAS DE CREDITO")
        try:
                archivo_nc=rutas_ig["IG_NC"]
                page.wait_for_selector('input[type="file"]', timeout=20000)
                page.wait_for_timeout(3000)
                page.set_input_files(
                        'input[type="file"]',
                        #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                        files=str(archivo_nc)
                )
                print("GUARDAR DOCUMENTOS EMITIDOS")
                page.wait_for_timeout(3000)
                # page.locator("#cpCol1_btnAceptar").click()
                page.locator("#cpCol1_btnCerrar").click()
                try:
                        os.remove(str(archivo_nc))
                        print(f"Archivo ELIMINADO correctamente: {archivo_nc.name}")
                except PermissionError:
                        print("No se pudo eliminar (archivo en uso o permisos insuficientes)")
                except FileNotFoundError:
                        print("El archivo ya no existe (posiblemente eliminado antes)")
                except Exception as e:
                        print(f"Error al eliminar el archivo: {e}")
        except Exception as e:
                print(f"Error durante la subida de NC: {e}")
                print("→ NO se elimina el archivo para que puedas revisarlo")

#   CARGA DE COMPROBANTES DE RETENCION
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS COMPROBANTES DE RETENCION")
        try:
                archivo_compret=rutas_ig["IG_COMPRET"]
                page.wait_for_selector('input[type="file"]', timeout=20000)
                page.wait_for_timeout(3000)
                page.set_input_files(
                        'input[type="file"]',
                        files=str(archivo_compret)
                )

                print("Archivo de emitidos subido!")
                print("GUARDAR DOCUMENTOS EMITIDOS")
                page.wait_for_timeout(3000)
                # page.locator("#cpCol1_btnAceptar").click()
                page.locator("#cpCol1_btnCerrar").click()
                try:
                        os.remove(str(archivo_compret))
                        print(f"Archivo ELIMINADO correctamente: {archivo_compret.name}")
                except PermissionError:
                        print("No se pudo eliminar (archivo en uso o permisos insuficientes)")
                except FileNotFoundError:
                        print("El archivo ya no existe (posiblemente eliminado antes)")
                except Exception as e:
                        print(f"Error al eliminar el archivo: {e}")
        except Exception as e:
                print(f"Error durante la subida de comprobantes de retención: {e}")
        page.close()

def subir_comprobantes_recibidos_bmi():
    with Camoufox(window=(1366, 768), headless=False) as browser:  # headless=True si no quieres verlo
        page = browser.new_page()
        page.goto(URL_PATH)
        page.wait_for_timeout(3000) 

        print("CARGA DE DOCUMENTOS RECIBIDOS" )
        print("LOGIN")
        page.type("#UserName", USERNAME_BMI, delay=400)
        print('INGRESO DE USERNAME: ', USERNAME_BMI)

        page.keyboard.press("Tab")
        #Password
        page.type("#Password", PASSWORD_BMI, delay=400)
        print('INGRESO DE PASSWORD: *******')
        page.keyboard.press("Enter")

        page.wait_for_timeout(5000)
        print("MENU")

        page.get_by_role("link", name="Carga Documentos Recibidos", exact=True).click()
    #   SUBIDA DE DOCUMENTOS RECIBIDOS FACTURAS
        print("SUBIDA DE DOCUMENTOS RECIBIDOS FACTURAS")
        try:
                archivo_fact=rutas_bmi["BMI_FACT"]
                page.wait_for_selector('input[type="file"]', timeout=20000)
                page.wait_for_timeout(3000)
                page.set_input_files(
                        'input[type="file"]',
                        #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                        files=str(archivo_fact)
                )
                print("Archivo de emitidos subido!")
                print("GUARDAR DOCUMENTOS EMITIDOS")
                page.wait_for_timeout(3000)
                # page.locator("#cpCol1_btnAceptar").click()
                page.locator("#cpCol1_btnCerrar").click()
                try:
                        os.remove(str(archivo_fact))
                        print(f"Archivo ELIMINADO correctamente: {archivo_fact.name}")
                except PermissionError:
                        print("No se pudo eliminar (archivo en uso o permisos insuficientes)")
                except FileNotFoundError:
                        print("El archivo ya no existe (posiblemente eliminado antes)")
                except Exception as e:
                        print(f"Error al eliminar el archivo: {e}")
        except Exception as e:
                print(f"Error durante la subida de Facturas: {e}")


#   CARGA DE NOTAS DE CREDITO
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS NOTAS DE CREDITO")
        try:
                archivo_nc=rutas_bmi["BMI_NC"]
                page.wait_for_selector('input[type="file"]', timeout=20000)
                page.wait_for_timeout(3000)
                page.set_input_files(
                        'input[type="file"]',
                        #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                        files=str(archivo_nc)
                )

                print("Archivo de emitidos subido!")
                print("GUARDAR DOCUMENTOS EMITIDOS")
                page.wait_for_timeout(3000)
                # page.locator("#cpCol1_btnAceptar").click()
                page.locator("#cpCol1_btnCerrar").click()
                try:
                        os.remove(str(archivo_nc))
                        print(f"Archivo ELIMINADO correctamente: {archivo_nc.name}")
                except PermissionError:
                        print("No se pudo eliminar (archivo en uso o permisos insuficientes)")
                except FileNotFoundError:
                        print("El archivo ya no existe (posiblemente eliminado antes)")
                except Exception as e:
                        print(f"Error al eliminar el archivo: {e}")
        except Exception as e:
                print(f"Error durante la subida de NC: {e}")

#   CARGA DE COMPROBANTES DE RETENCION
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS COMPROBANTES DE RETENCION")
        try:
                archivo_compret=rutas_bmi["BMI_COMPRET"]
                page.wait_for_selector('input[type="file"]', timeout=20000)
                page.wait_for_timeout(3000)
                page.set_input_files(
                        'input[type="file"]',
                        #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                        files=str(archivo_compret)
                )

                print("Archivo de emitidos subido!")
                print("GUARDAR DOCUMENTOS EMITIDOS")
                page.wait_for_timeout(3000)
                # page.locator("#cpCol1_btnAceptar").click()
                page.locator("#cpCol1_btnCerrar").click()
                try:
                        os.remove(str(archivo_compret))
                        print(f"Archivo ELIMINADO correctamente: {archivo_compret.name}")
                except PermissionError:
                        print("No se pudo eliminar (archivo en uso o permisos insuficientes)")
                except FileNotFoundError:
                        print("El archivo ya no existe (posiblemente eliminado antes)")
                except Exception as e:
                        print(f"Error al eliminar el archivo: {e}")
        except Exception as e:
                print(f"Error durante la subida de comprobantes de retención: {e}")

        page.close()
    