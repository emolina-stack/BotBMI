from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pathlib import Path
import numpy as np


URL_PATH="https://www.trancenter.com.ec/IFacturaEcuadorBMI/"
#F:\Bots\NavegadorCamoufox\anulados_emitidos_20260130_1421.csv
URL_COMPROBANTES_RECIBIDOS_BMI=Path(r"F:\\Bots\1791301692001_Recibidos.txt") #BMI
URL_COMPROBANTES_RECIBIDOS_IG=Path(r"F:\\Bots\1791927559001_Recibidos.txt") #IG
URL_COMPROBANTES_RECIBIDOS_ME=Path(r"F:\\Bots\1791301692001_Recibidos.txt") #BMI

# BMI
# USERNAME="usrBotRecepcionBMI"
# PASSWORD="jK~471|6s*"

# IGUALAS
USERNAME="usrBotRecepcionIG"
PASSWORD="y3677D.7lh"


def subir_comprobantes_recibidos():
    with Camoufox(window=(1366, 768), headless=False) as browser:  # headless=True si no quieres verlo
        page = browser.new_page()
        page.goto(URL_PATH)
        page.wait_for_timeout(3000) 

        print("CARGA DE DOCUMENTOS ANULADOS" )
        print("LOGIN")
        page.type("#UserName", USERNAME, delay=400)
        print('INGRESO DE USERNAME: ', USERNAME)

        page.keyboard.press("Tab")
        #Password
        page.type("#Password", PASSWORD, delay=400)
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
                files=str(URL_COMPROBANTES_RECIBIDOS_IG)
        )
        print("Archivo de emitidos subido!")
        print("GUARDAR DOCUMENTOS EMITIDOS")
        page.wait_for_timeout(3000)
        page.locator("#cpCol1_btnAceptar").click()

        input("Inicia sesión y presiona Enter para continuar...")