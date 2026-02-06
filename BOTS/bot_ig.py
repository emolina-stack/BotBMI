from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from BOTS.documents import click_con_movimiento

import undetected_chromedriver as uc
import time
import sys, os

def main_ig():
    CHROME_MAJOR_VERSION = 144
    BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    SRI_URL = "https://srienlinea.sri.gob.ec/auth/realms/Internet/protocol/openid-connect/auth?client_id=app-sri-claves-angular&redirect_uri=https%3A%2F%2Fsrienlinea.sri.gob.ec%2Fsri-en-linea%2F%2Fcontribuyente%2Fperfil&state=04b7b077-e0ef-489f-81df-fa7e8b371002&nonce=79d20507-d1a2-4f75-843b-0f0f48e13c3a&response_mode=fragment&response_type=code&scope=openid"

    # FACTURAS, NC, COMPROBANTES DE RETENCION
    # IGUALAS
    RUC="1791927559001"
    IDENTIFICACION="1711542959"
    PASSWORD_SRI="ASDasd123."

    DOWNLOAD_DIR = os.path.abspath("F:/Bots/Bot_BMI/DOC_IG")  # ← RUTA IGUALAS
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    options = uc.ChromeOptions()

    # Prueba A: Sin binary_location → suele eliminar la ventana extra (recomendado para empezar)
    options.binary_location = BRAVE_PATH  # Comenta esta línea primero

    # Flags para estabilidad y menos procesos
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--process-per-site")  # reduce procesos auxiliares
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-gpu")  # a veces ayuda en Windows
    options.add_argument("--disable-features=DownloadBubble")

    # Configuración clave para descargas automáticas
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,                  # Carpeta destino
        "download.prompt_for_download": False,                       # Sin ventana "Guardar como"
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,            # Evita bloqueos de "archivo peligroso"
        "profile.default_content_setting_values.automatic_downloads": 1,  # Permite descargas múltiples automáticas
    }
    options.add_experimental_option("prefs", prefs)

    driver = None

    try:
        wait = WebDriverWait(driver, 20)
        print(f"Intentando con major version {CHROME_MAJOR_VERSION}...")
        driver = uc.Chrome(
            options=options,
            version_main=CHROME_MAJOR_VERSION,
            use_subprocess=True,
            suppress_welcome=True
        )
        driver.maximize_window()

        print("¡Driver iniciado OK!")
        driver.set_page_load_timeout(60)

        # Carga SRI directamente
        driver.get(SRI_URL)
        time.sleep(10)  # Dale tiempo para redirects y carga
        print("SRI cargó → URL final:")
        print("Título de la página:")

        # Aquí agrega tu login cuando funcione la carga
        # Ejemplo básico (ajusta selectores si cambian)
        time.sleep(3)
        driver.find_element("id", "usuario").send_keys(RUC)
        driver.find_element("id", "ciAdicional").send_keys(IDENTIFICACION)
        driver.find_element("id", "password").send_keys(PASSWORD_SRI)

        time.sleep(3)
        driver.find_element("id", "kc-login").click()
        time.sleep(10)  
        
        #//*[@id="mySidebar2"]/div[3]/div/button
        time.sleep(10)  
        print("MENU")
        fe=driver.find_element(By.XPATH, '//button[@title="Facturación Electrónica"]')
        click_con_movimiento(driver, fe)
        time.sleep(5)

        print("Comprobantes electronicos recibidos")
        cer=driver.find_element(By.XPATH, '//*[@id="mySidebar"]/p-panelmenu/div/div[2]/div[2]/div/p-panelmenusub/ul/li/a')
        click_con_movimiento(driver, cer)
        time.sleep(10)

        time.sleep(10)
        #   SELECCIONA FECHA
        print("Inicio Captcha")
        select_elem = driver.find_element(By.ID, "frmPrincipal:dia")
        dia_select = Select(select_elem)
        # now = datetime.now()
        # last_date=(now-timedelta(days=1)).day
        # day_str=str(last_date)
        # print('dia anterior: ', day_str)
        dia_select.select_by_visible_text("Todos")  # Selecciona "Todos"

        print("Consultar")
        time.sleep(3)
        fe=driver.find_element(By.ID, "frmPrincipal:btnBuscar")
        click_con_movimiento(driver, fe)
        time.sleep(10)

        # Validar si existe mensaje de captcha
        def verificar_captcha():
            try:
                msgCaptcha = driver.find_element(By.ID, "formMessages")
                return msgCaptcha.is_displayed()
            except:
                return False

        def seleccionar_documentos():
                try:
                    chk_document = driver.find_element(By.ID, "frmPrincipal:cmbTipoComprobante")
                    click_con_movimiento(driver, chk_document)
                    document_select = Select(chk_document)
                    document_select.select_by_visible_text("Notas de Crédito")
                    # BUSCAR NOTAS DE CREDITO
                    time.sleep(3)
                    nc=driver.find_element(By.ID, "frmPrincipal:btnBuscar")
                    click_con_movimiento(driver, nc)
                    time.sleep(5)

                    descargar = driver.find_element(By.ID, "frmPrincipal:lnkTxtlistado")
                    click_con_movimiento(driver, descargar)

                    # SELECCIONAR COMPROBANTES DE RETENCION
                    time.sleep(3)
                    chk_document = driver.find_element(By.ID, "frmPrincipal:cmbTipoComprobante")
                    click_con_movimiento(driver, chk_document)
                    document_select = Select(chk_document)
                    document_select.select_by_visible_text("Comprobante de Retención")
                    # BUSCAR COMPROBANTES DE RETENCION
                    time.sleep(3)
                    nc=driver.find_element(By.ID, "frmPrincipal:btnBuscar")
                    click_con_movimiento(driver, nc)
                    time.sleep(5)

                    descargar = driver.find_element(By.ID, "frmPrincipal:lnkTxtlistado")
                    click_con_movimiento(driver, descargar)

                    print("✓ Todos los documentos seleccionados.")
                except Exception as e:
                    print(f"✗ Error al seleccionar documentos: {str(e)}")
        # Intentar resolver captcha con reintentos

        max_intentos = 5
        intentos = 0
        captcha_resuelto = False
        if verificar_captcha():
            print("⚠️ Captcha detectado. Por favor, resuélvelo manualmente en el navegador.")
            print(f"Tienes un máximo de {max_intentos} intentos de reintentos automáticos.\n")

            while intentos < max_intentos and not captcha_resuelto:
                intentos += 1
                tiempo_espera = 10  # segundos entre reintentos
                print(f"[Intento {intentos}/{max_intentos}] Esperando resolución de captcha ({tiempo_espera}s)...")
                time.sleep(tiempo_espera)
                
                # Reintentar consulta
                try:
                    btn_buscar = driver.find_element(By.ID, "frmPrincipal:btnBuscar")
                    click_con_movimiento(driver, btn_buscar)
                    time.sleep(3)
                    
                    # Verificar si el captcha sigue visible
                    if not verificar_captcha():
                        print("✓ Captcha resuelto exitosamente!")
                        time.sleep(5)  # Espera extra para asegurar descarga completa
                        print("SUBIENDO COMPROBANTES RECIBIDOS")
                        #subir_comprobantes_recibidos()
                        captcha_resuelto = True
                    else:
                        print(f"  → Captcha aún presente. Reintentando...")
                        
                except Exception as e:
                    print(f"  → Error en reintentos: {str(e)}")
                    break

            if not captcha_resuelto:
                print("⚠️ Captcha no se resolvió después de máximo de intentos.")
        else:
            print("✓ No se detectó captcha, continuando...")
        # Descargar resultado
        try:
            descargar = driver.find_element(By.ID, "frmPrincipal:lnkTxtlistado")
            click_con_movimiento(driver, descargar)
            print("✓ Archivo descargado correctamente!")
            time.sleep(5)  # Espera extra para asegurar descarga completa
            print("SELECCIONAR DOCUMENTOS")
            seleccionar_documentos()

            print("SUBIENDO COMPROBANTES RECIBIDOS")
            #subir_comprobantes_recibidos()
            time.sleep(2)
        except Exception as e:
            print(f"✗ Error al descargar archivo: {str(e)}")
        
        driver.close()
        driver.quit()
    
    except Exception as e:
        print("Error principal:", str(e))
        print("\nFixes rápidos:")
        print("- Borra %APPDATA%\\undetected_chromedriver")
        print("- Prueba version_main=143 o 145")
        print("- pip install --upgrade undetected-chromedriver selenium")
        sys.exit(1)

