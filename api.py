from fastapi import FastAPI, BackgroundTasks
import subprocess
import os
app = FastAPI()

def ejecutar_bot():
    python_exe = r"F:\Bots\Bot_BMI\har\Scripts\python.exe"
    script_path = r"F:\Bots\Bot_BMI\inicio_bot.py"
    cwd = r"F:\Bots\Bot_BMI"

    # Verificaciones básicas (para depurar, puedes quitar después)
    if not os.path.exists(python_exe):
        raise FileNotFoundError(f"No se encuentra el python del venv: {python_exe}")
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"No se encuentra el script: {script_path}")

    process = subprocess.Popen(
        [python_exe, "-m", "inicio_bot"],
        cwd=cwd
        # creationflags=subprocess.CREATE_NO_WINDOW   # evita ventana cmd visible (útil en background)
    )

    print(f"Bot lanzado → PID: {process.pid}")
    # subprocess.Popen(["cmd.exe", "/c", "F:\\Bots\\Bot_BMI\\execute.bat"])

@app.post("/lanzar-bmi")
async def lanzar_bmi(background_tasks: BackgroundTasks):
    background_tasks.add_task(ejecutar_bot)
    return {"mensaje": "Bot BMI lanzado en segundo plano"}