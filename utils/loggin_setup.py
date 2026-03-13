# utils/logging_setup.py
import logging
import os
from datetime import datetime

def configurar_logging(
    nombre_script="ejecucion_bot_recibidos",
    carpeta="logs",
    nivel=logging.INFO,
    mostrar_consola=True
):
    """
    Configura el logging para crear un archivo único por ejecución
    Retorna el logger configurado.
    """
    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)
    
    # Nombre del archivo con timestamp
    # fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_log = f"{carpeta}/{nombre_script}.log"
    
    # Formato limpio y legible
    formato = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        
    # Configuración base
    logging.basicConfig(
        level=nivel,
        format=formato,
        encoding='utf-8'
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler(nombre_log, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(formato))
    
    # # Handler para consola (opcional)
    # if mostrar_consola:
    #     console_handler = logging.StreamHandler()
    #     console_handler.setFormatter(logging.Formatter(formato))
    #     logging.getLogger().addHandler(console_handler)
    
    # Aplicar handler al root logger (o al logger específico)
    logging.getLogger().addHandler(file_handler)
    
    logger = logging.getLogger(nombre_script)
    logger.info(f"Logging iniciado → {nombre_log}")
    
    return logger, nombre_log