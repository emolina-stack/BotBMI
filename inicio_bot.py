from BOTS.bot_bmi import main_bmi
from BOTS.bot_ig import main_ig
from subir_recibidos import subir_comprobantes_recibidos_ig
from subir_recibidos import subir_comprobantes_recibidos_bmi

def execute_bots():
    print("===========INICIANDO BOT IG=============")
    main_ig()# BOT IG
    print("===========FINALIZADO BOT IG=============")
    print("*********************************************")
    print("===========INICIANDO BOT BMI=============")
    main_bmi()# BOT BMI
    print("===========FINALIZADO BOT BMI=============")
 
# def carga_archivos():
#     print("===========INICIANDO CARGA DE ARCHIVOS IGUALAS=============")
#     subir_comprobantes_recibidos_ig()
#     print("===========FINALIZADA CARGA DE ARCHIVOS IGUALAS=============")
#     print("===========INICIANDO CARGA DE ARCHIVOS BMI=============")
#     subir_comprobantes_recibidos_bmi()
#     print("===========FINALIZADA CARGA DE ARCHIVOS BMI=============")
    

if __name__ == "__main__":
    execute_bots()
    print("*************************************")
    #carga_archivos()
