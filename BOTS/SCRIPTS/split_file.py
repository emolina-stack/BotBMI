from pathlib import Path

def dividir_con_cabecera(ruta_entrada, lineas_por_parte=1500, carpeta_salida=None):
    entrada = Path(ruta_entrada)
    
    if carpeta_salida:
        salida_dir = Path(carpeta_salida)
        salida_dir.mkdir(exist_ok=True)
    else:
        salida_dir = entrada.parent
    
    with open(entrada, 'r', encoding='latin1') as f:
        lineas = f.readlines()
    
    if not lineas:
        print("El archivo está vacío")
        return
    
    # La cabecera es la primera línea
    cabecera = lineas[0]
    contenido = lineas[1:]  # todo lo demás sin cabecera
    
    total_contenido = len(contenido)
    print(f"Total líneas de datos (sin cabecera): {total_contenido}")
    
    for i in range(0, total_contenido, lineas_por_parte):
        inicio = i
        fin = min(i + lineas_por_parte, total_contenido)
        parte_datos = contenido[inicio:fin]
        
        numero = (i // lineas_por_parte) + 1
        nombre = f"{entrada.stem}_parte{numero:02d}"
        ruta_salida = salida_dir / nombre
        
        with open(ruta_salida, 'w', encoding='latin1') as f_out:
            # Escribimos la cabecera + los datos de esta parte
            f_out.write(cabecera)
            f_out.writelines(parte_datos)
        
        print(f"→ {nombre} creado ({len(parte_datos)} líneas de datos + cabecera)")
