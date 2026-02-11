from pathlib import Path

import time

CARPETA="F:\\Bots\Bot_BMI\DOC_IG\SPLIT_FILES" # RUTA DE ARCHIVOS DIVIDIDOS IG


def subir_archivo_desglosado(
    page,
    selector_input: str = 'input[type="file"]',
    carpeta_o_lista: str = list,
    espera_despues_subida: float = 5.0,      
    espera_confirmacion: float = 3.0,        
    selector_boton_enviar: str = None,       
    selector_mensaje_exito: str = None,      
    timeout_por_subida: int = 90000
):
    if isinstance(carpeta_o_lista, (str, Path)):
        carpeta = Path(carpeta_o_lista)
        archivos = sorted(carpeta.glob("*.*"))  # todos los archivos

        print("existen archivos",archivos)
    else:
        archivos = [Path(f) for f in carpeta_o_lista]

    archivos = [f for f in archivos if f.is_file() and f.exists()]
    
    if not archivos:
        print("No se encontraron archivos para subir")
        return
    
    total = len(archivos)
    print(f"Iniciando subida secuencial de {total} archivos...")
    
    exitosos = 0
    for idx, archivo in enumerate(archivos, 1):
        print(f"\n[{idx}/{total}] Procesando: {archivo.name}")
        
        try:
            # 1. Esperamos que el input file esté disponible
            page.wait_for_selector(selector_input, state="visible", timeout=20000)
            page.wait_for_timeout(1000)
            
            # 2. Cargamos SOLO este archivo
            print(f"   → Cargando archivo...")
            page.set_input_files(selector_input, files=str(archivo))
            
            # 3. Pequeña pausa para que la página procese el archivo cargado
            page.wait_for_timeout(2000)
            
            # 4. Si hay botón de "Enviar", "Guardar", "Subir" o "Aceptar"
            if selector_boton_enviar:
                print(f"   → Buscando botón de enviar...")
                boton = page.locator(selector_boton_enviar)
                boton.wait_for(state="visible", timeout=15000)
                boton.click()
                print("   → Clic en botón de enviar/guardar")
            
            # 5. Esperamos procesamiento / mensaje de éxito / carga completa
            if selector_mensaje_exito:
                print("   → Esperando mensaje de éxito...")
                page.wait_for_selector(selector_mensaje_exito, timeout=timeout_por_subida)
                print("   → Éxito confirmado")
            else:
                # Si no tienes selector de éxito, solo esperamos tiempo fijo
                print(f"   → Esperando {espera_despues_subida} segundos después de subir...")
                page.wait_for_timeout(int(espera_despues_subida * 1000))
            
            # 6. Pausa adicional para estabilidad
            time.sleep(espera_confirmacion)
            
            exitosos += 1
            print(f"   ✓ Archivo {archivo.name} subido correctamente")
            
        except Exception as e:
            print(f"   ✗ Error al procesar {archivo.name}: {str(e)}")

        time.sleep(2)
    
    print("\n" + "═"*60)
    print(f"Proceso finalizado:")
    print(f"  Archivos subidos correctamente: {exitosos}/{total}")
    print("═"*60)
    
    