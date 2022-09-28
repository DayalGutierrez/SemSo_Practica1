import os
from time import sleep
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from random import randint as ran
from pynput import keyboard as kb

console = Console()

pause, werror, interrupcion = 0,0,0

def def_operacion(n_operacion, operando1, operando2):
    if n_operacion == 1:
        operacion = "+"
    elif n_operacion == 2:
        operacion = "-"
    elif n_operacion == 3:
        operacion = "*"
    elif n_operacion == 4:
        operacion = "/"
        while operando2 == 0:
            operando2 = ran(-100, 100)
    elif n_operacion == 5:
        operacion = "%"
        while operando2 == 0:
            operando2 = ran(-100, 100)
    elif n_operacion == 6:
        operacion = "^"
        while operando1 == 0 and operando2 == 0:
            operando1 = ran(-100, 100)
            operando2 = ran(-100, 100)
    return operacion, operando1, operando2

total_procesos = int(input("Ingrese el numero de procesos: "))

nuevos, listos, bloqueados, terminados = list(), list(), list(), list()
proceso_ejecucion = 0
tiempo_global = 0

for i in range(total_procesos):
    os.system("cls")

    operando1 = ran(-100, 100)
    operando2 = ran(-100, 100)
    n_operacion = ran(1, 6)
    operacion, operando1, operando2 = def_operacion(n_operacion, operando1,
                                                    operando2)

    tme = ran(6, 16)
    tiem_trans = 0
    tiem_rest = tme
    
    proceso = {
        "id":i+1, 
        "operando1":operando1,
        "operando2":operando2, 
        "operacion":operacion,
        "resultado":0,
        "tme":tme, 
        "tiem_trans":tiem_trans,
        "tiem_rest":tiem_rest,
        "f_respuesta":0,
        "tiem_bloq":0,
        "tiem_llegada":0,
        "tiem_finalizacion":0,
        "tiem_retorno":0,
        "tiem_respuesta":0,
        "tiem_espera":0,
        "tiem_servicio":0
        }
    nuevos.append(proceso)

os.system("cls")

def pulsa(tecla):
    global pause, werror, interrupcion
    if pause == 1:
        if tecla == kb.KeyCode.from_char('c'):
            pause = 0
    else:
        if tecla == kb.KeyCode.from_char('p'):
            pause = 1
        if tecla == kb.KeyCode.from_char('w'):
            werror = 1
        if tecla == kb.KeyCode.from_char('e'):
            interrupcion = 1
    

escuchador = kb.Listener(pulsa)
escuchador.start()

def make_layout() -> Layout:
    """Define el layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="head", size=3),
        Layout(name="chest", ratio=1),
        Layout(name="leg", ratio=1),
        Layout(name="foot", size=3),
    )
    layout["chest"].split_row(Layout(name="izq"), Layout(name="centro"),
                             Layout(name="der"))
    layout["foot"].split_row(Layout(name="tiempo"), Layout(name="final"))
    return layout


class Header:
    """Muestra el numero de procesos restantes"""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="right", ratio=1)
        grid.add_column(justify="left", ratio=1)
        grid.add_row(
            "Procesos restantes: ",
            str(len(nuevos)),
            style="grey3",
        )

        return Panel(grid, style="white on blue")

def tabla_listos(indice1,indice2) -> Table:
    """Genera la tabla de listos"""

    table = Table(title="Procesos listos")
        
    table.add_column("Identificador",
                     justify="left",
                     style="light_slate_blue")
    table.add_column("TME", justify="left", style="light_slate_blue")
    table.add_column("Tiempo transcurrido", justify="left", style="light_slate_blue")
    
    try:
        if listos[indice1]["tiem_rest"] == 0:
            pass
        else:
            table.add_row(str(listos[indice1]["id"]),str(listos[indice1]["tme"]),str(listos[indice1]["tiem_trans"]))
    except:
        pass
    try:
        if listos[indice2]["tiem_rest"] == 0:
            pass
        else:
            table.add_row(str(listos[indice2]["id"]),str(listos[indice2]["tme"]),str(listos[indice2]["tiem_trans"]))
    except:
        pass
    return table

def tabla_proceso_ejecucion() -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")

    table.add_row("Identificador: ",
                  str(listos[proceso_ejecucion]["id"]),
                  style="grey63")
    table.add_row("Operacion: ",
                  str(listos[proceso_ejecucion]["operando1"]) +
                  str(listos[proceso_ejecucion]["operacion"]) +
                  str(listos[proceso_ejecucion]["operando2"]),
                  style="medium_purple2")
    table.add_row("TME: ",
                  str(listos[proceso_ejecucion]["tme"]),
                  style="grey63")
    table.add_row("Tiempo transcurrido: ", str(listos[proceso_ejecucion]["tiem_trans"]), style="grey63")
    table.add_row("Tiempo restante: ",
                  str(listos[proceso_ejecucion]["tiem_rest"]),
                  style="medium_purple2")

    return table

def tabla_proceso_ejecucion_fin() -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")
    table.add_row("Identificador: ", style="grey63")
    table.add_row("Operacion: ", style="medium_purple2")
    table.add_row("TME: ", style="grey63")
    table.add_row("Tiempo transcurrido: ", style="medium_purple2")
    table.add_row("Tiempo restante: ", style="grey63")
    return table

def tabla_bloqueados() -> Table:
    """Genera la tabla de los procesos bloqueados"""
    table = Table(title="Procesos bloqueados")
    table.add_column("Identificador", justify="left", style="bold blue")
    table.add_column("Tiempo bloqueado", justify="left", style="bold blue")
    
    for proceso in bloqueados: 
        table.add_row(str(proceso["id"]), str(proceso["tiem_bloq"]))

    return table

"""Genera la tabla del procesos terminados"""
table_terminados = Table(title="Procesos terminados")
table_terminados.add_column("Identificador",
                             justify="left",
                             style="bold blue")
table_terminados.add_column("Operacion", justify="left", style="bold blue")
table_terminados.add_column("Resultado", justify="left", style="bold blue")

def agregar_terminado():
    global werror

    identificador = listos[proceso_ejecucion]["id"]
    operacion = str(listos[proceso_ejecucion]["operando1"]) + str(listos[proceso_ejecucion]["operacion"]) + str(listos[proceso_ejecucion]["operando2"])

    if werror == 0:
        if listos[proceso_ejecucion]["operacion"] == "+":
            resultado = listos[proceso_ejecucion]["operando1"] + listos[proceso_ejecucion]["operando2"]
        elif listos[proceso_ejecucion]["operacion"] == "-":
            resultado = listos[proceso_ejecucion]["operando1"] - listos[proceso_ejecucion]["operando2"]
        elif listos[proceso_ejecucion]["operacion"] == "*":
            resultado = listos[proceso_ejecucion]["operando1"] * listos[proceso_ejecucion]["operando2"]
        elif listos[proceso_ejecucion]["operacion"] == "/":
            resultado = listos[proceso_ejecucion]["operando1"] / listos[proceso_ejecucion]["operando2"]
        elif listos[proceso_ejecucion]["operacion"] == "%":
            resultado = listos[proceso_ejecucion]["operando1"] % listos[proceso_ejecucion]["operando2"]
        elif listos[proceso_ejecucion]["operacion"] == "^":
            resultado = listos[proceso_ejecucion]["operando1"] ** listos[proceso_ejecucion]["operando2"]    
    else:
        resultado = "!Error"
        werror = 0

    listos[proceso_ejecucion]["resultado"] = resultado

    table_terminados.add_row(str(identificador),
                              operacion,
                              str(resultado),
                              style="grey63")

def tabla_tiempo_global() -> Table:
    global tiempo_global
    tiempo_total = Table.grid(expand=True)
    tiempo_total.add_row("Tiempo transcurrido " + str(tiempo_global),
                         style="light_slate_blue")
    tiempo_global += 1

    return tiempo_total

def tabla_tiempo_global_inicial() -> Table:
    tiempo_total = Table.grid(expand=True)
    tiempo_total.add_row("Tiempo transcurrido " + str(0),
                         style="light_slate_blue")

    return tiempo_total

def mensaje_final() -> Table:
    mensaje = Table.grid(expand=True)
    mensaje.add_row("De ENTER para visualizar todos los procesos", style="light_slate_blue")

    return mensaje

def mensaje_final_vacio() -> Table:
    mensaje = Table.grid(expand=True)
    mensaje.add_row("", style="light_slate_blue")

    return mensaje

def nuevo_a_listo():
    # Seccion de llenado de procesos listos
    global listos, nuevos
    try:
        nuevos[0]["tiem_llegada"] = tiempo_global
        listos.append(nuevos[0])
        nuevos.pop(0)
    except:
        pass

def listo_a_bloqueado():
    # Seccion de interrupción
    global listos, bloqueados
    try:
        bloqueados.append(listos[0])
        listos.pop(0)
    except:
        pass

def bloqueado_a_listo():
    # Seccion de salida de bloqueados a hacia listos
    global listos, bloqueados
    bloqueados[0]["tiem_bloq"] = 0
    try:
        listos.append(bloqueados[0])
        bloqueados.pop(0)
    except:
        pass

def listo_a_terminado():
    # Seccion de llenado de procesos terminados para tabla final
    global listos, terminados
    try:
        listos[0]["tiem_finalizacion"] = tiempo_global
        terminados.append(listos[0])
        listos.pop(0)
    except:
        pass

for i in range (3):        
    nuevo_a_listo()

layout = make_layout()
layout["head"].update(Header())
layout["chest"].size = 10
layout["chest"]["izq"].update(tabla_listos(1,2))
layout["chest"]["izq"].ratio = 2
layout["chest"]["centro"].update(tabla_proceso_ejecucion())
layout["chest"]["centro"].ratio = 3
layout["chest"]["der"].update(tabla_bloqueados())
layout["chest"]["der"].ratio = 2
layout["leg"].size = 20
layout["leg"].update(table_terminados)
layout["foot"]["tiempo"].update(tabla_tiempo_global_inicial())
layout["foot"]["final"].update(mensaje_final_vacio())

    
with Live(layout, refresh_per_second=15) as live:
    procesos_finalizados = 0
    tiem_bloq_terminado = 0

    while procesos_finalizados != total_procesos:
        layout["chest"]["der"].update(tabla_bloqueados())
        layout["chest"]["izq"].update(tabla_listos(1,2))  
        
        if len(listos) > 0:
            layout["chest"]["centro"].update(tabla_proceso_ejecucion())

            if listos[proceso_ejecucion]["f_respuesta"] == 0:
                listos[proceso_ejecucion]["tiem_respuesta"] = tiempo_global - listos[proceso_ejecucion]["tiem_llegada"]
                listos[proceso_ejecucion]["f_respuesta"] = 1
            
            for j in range(listos[proceso_ejecucion]["tiem_rest"]):
                while pause == 1:
                    pass
                if werror == 1:
                    break
                if interrupcion == 1:
                    listo_a_bloqueado()
                    break

                sleep(1)

                listos[proceso_ejecucion]["tiem_trans"] += 1
                listos[proceso_ejecucion]["tiem_rest"] -= 1
                for proceso in bloqueados:
                    proceso["tiem_bloq"] += 1
                    if proceso["tiem_bloq"] == 7:
                        tiem_bloq_terminado = 1

                layout["chest"]["centro"].update(tabla_proceso_ejecucion())
                layout["chest"]["der"].update(tabla_bloqueados())
                layout["foot"]["tiempo"].update(tabla_tiempo_global())

                if tiem_bloq_terminado == 1:
                    tiem_bloq_terminado = 0
                    interrupcion = 1
                    bloqueado_a_listo()
                    break
        else:
            layout["chest"]["centro"].update(tabla_proceso_ejecucion_fin())
            for i in range(7):
                sleep(1)
                for proceso in bloqueados:
                    proceso["tiem_bloq"] += 1
                    if proceso["tiem_bloq"] == 7:
                        tiem_bloq_terminado = 1
                layout["chest"]["der"].update(tabla_bloqueados())
                layout["foot"]["tiempo"].update(tabla_tiempo_global())
                if tiem_bloq_terminado == 1:
                    tiem_bloq_terminado = 0
                    bloqueado_a_listo()
                    break
            interrupcion = 1

        if werror == 1:
            # Aqui se debe calcular el tiempo de servicio
            listos[proceso_ejecucion]["tiem_rest"] = 0
        
        if interrupcion == 1:
            interrupcion = 0
        else:
            #Agregar a la tabla los procesos que ya se finalizaron
            agregar_terminado()
            
            #Aumentar y mantener un control para los procesos
            procesos_finalizados += 1
            
            listo_a_terminado()
            nuevo_a_listo()
            layout["head"].update(Header())

    layout["chest"]["centro"].update(tabla_proceso_ejecucion_fin())
    layout["foot"]["final"].update(mensaje_final())

    input()
print(layout)

os.system ("cls")

def make_layout_final() -> Layout:
    """Define el layout final"""
    layout_final = Layout(name="root")

    layout_final.split(
        Layout(name="head")
    )

    return layout_final

"""Genera la tabla del procesos terminados"""
table_final = Table(title="Procesos")
table_final.add_column("Identificador",
                             justify="left",
                             style="bold blue")
table_final.add_column("Operacion", justify="left", style="bold blue")
table_final.add_column("Resultado", justify="left", style="bold blue")
table_final.add_column("TME", justify="left", style="bold blue")
table_final.add_column("Tiempo transcurrido", justify="left", style="bold blue")
table_final.add_column("Tiempo restante", justify="left", style="bold blue")
table_final.add_column("TLL", justify="left", style="bold blue")
table_final.add_column("TF", justify="left", style="bold blue")
table_final.add_column("TRET", justify="left", style="bold blue")
table_final.add_column("TRES", justify="left", style="bold blue")
table_final.add_column("TE", justify="left", style="bold blue")
table_final.add_column("TS", justify="left", style="bold blue")

for proceso in terminados:
    proceso["tiem_retorno"] = proceso["tiem_finalizacion"] - proceso["tiem_llegada"]
    proceso["tiem_espera"] = proceso["tiem_retorno"] - proceso["tiem_trans"]
    proceso["tiem_servicio"] = proceso["tiem_trans"]
    proceso["tiem_rest"] = proceso["tme"] - proceso["tiem_trans"]
    
    table_final.add_row(str(proceso["id"]),
                        str(proceso["operando1"]) + str(proceso["operacion"]) + str(proceso["operando2"]),
                        str(proceso["resultado"]),
                        str(proceso["tme"]),
                        str(proceso["tiem_trans"]),
                        str(proceso["tiem_rest"]),
                        str(proceso["tiem_llegada"]),
                        str(proceso["tiem_finalizacion"]),
                        str(proceso["tiem_retorno"]),
                        str(proceso["tiem_respuesta"]),
                        str(proceso["tiem_espera"]),
                        str(proceso["tiem_servicio"]),
                        style="grey63")

layout_final = make_layout_final()
layout_final["head"].update(table_final)

print(layout_final)