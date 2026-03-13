import threading
import time
import pyautogui

def mantener_usuario_activo(intervalo_segundos=60):
    while True:
        # pequeño movimiento de ratón
        x, y = pyautogui.position()
        pyautogui.moveTo(x + 1, y + 1, duration=0.1)
        pyautogui.moveTo(x, y, duration=0.1)
        time.sleep(intervalo_segundos)

def iniciar_hilo_keep_alive():
    hilo = threading.Thread(target=mantener_usuario_activo, daemon=True)
    hilo.start()