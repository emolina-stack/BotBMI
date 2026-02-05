from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pathlib import Path
import numpy as np


URL_PATH="https://www.trancenter.com.ec/IFacturaEcuadorBMI/"
#F:\Bots\NavegadorCamoufox\anulados_emitidos_20260130_1421.csv
# URL_COMPROBANTES_RECIBIDOS_BMI=Path(r"F:\\Bots\1791301692001_Recibidos.txt") #BMI
# URL_COMPROBANTES_RECIBIDOS_IG=Path(r"F:\\Bots\1791927559001_Recibidos.txt") #IG
# URL_COMPROBANTES_RECIBIDOS_ME=Path(r"F:\\Bots\1791301692001_Recibidos.txt") #BMI

rutas_ig={
    "IG_FACT":Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos.txt"), #  FACTURAS
    "IG_NC":Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos (1).txt"),# NOTAS DE CREDITO
    "IG_COMPRET":Path(r"F:\\Bots\Bot_BMI\DOC_IG\1791927559001_Recibidos (2).txt"),#   COMPROBANTES DE RETENCION
}

rutas_bmi={
    "BMI_FACT":Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos.txt"),#  FACTURAS
    "BMI_NC":Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos (1).txt"),# NOTAS DE CREDITO
    "BMI_COMPRET":Path(r"F:\\Bots\Bot_BMI\DOC_BMI\1791301692001_Recibidos (2).txt"),#   COMPROBANTES DE RETENCION
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
        print("SUBIDA DE DOCUMENTOS RECIBIDOS FACTURAS")
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files(
                'input[type="file"]',
                #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                files=str(rutas_ig["IG_FACT"])
        )
        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()

#   CARGA DE NOTAS DE CREDITO
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS NOTAS DE CREDITO")
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files(
                'input[type="file"]',
                #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                files=str(rutas_ig["IG_NC"])
        )

        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()

#   CARGA DE COMPROBANTES DE RETENCION
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS COMPROBANTES DE RETENCION")
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files(
                'input[type="file"]',
                #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                files=str(rutas_ig["IG_COMPRET"])
        )

        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()

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
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files(
                'input[type="file"]',
                #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                files=str(rutas_bmi["BMI_FACT"])
        )
        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()

#   CARGA DE NOTAS DE CREDITO
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS NOTAS DE CREDITO")
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files(
                'input[type="file"]',
                #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                files=str(rutas_bmi["BMI_NC"])
        )

        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()

#   CARGA DE COMPROBANTES DE RETENCION
        page.wait_for_timeout(2000)
        print("SUBIDA DE DOCUMENTOS RECIBIDOS COMPROBANTES DE RETENCION")
        page.wait_for_selector('input[type="file"]', timeout=20000)
        page.wait_for_timeout(3000)
        page.set_input_files(
                'input[type="file"]',
                #files=str(URL_COMPROBANTES_RECIBIDOS_IG)
                files=str(rutas_bmi["BMI_COMPRET"])
        )

        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        # page.locator("#cpCol1_btnAceptar").click()
        page.locator("#cpCol1_btnCerrar").click()

        page.close()
    