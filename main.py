import os
from statistics import quantiles
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

pause, werror, interrupcion, nuevo, bcp, tab_paginacion = 0,0,0,0,0,0

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
quantum = int(input("Ingrese el quantum del procesador: "))

quantum_control = 0

nuevos, listos, bloqueados, terminados, memoria = list(), list(), list(), list(), list()
proceso_ejecucion = 0
tiempo_global = 0
idx_id = 1

for i in range(40):
    pagina = ["0/5","N/A","N/A"]
    memoria.append(pagina)
for i in range(4):
    pagina = ["5/5", "SO", "SO"]
    memoria.append(pagina)

def nuevo_proceso():
    global idx_id
    operando1 = ran(-100, 100)
    operando2 = ran(-100, 100)
    n_operacion = ran(1, 6)
    operacion, operando1, operando2 = def_operacion(n_operacion, operando1,
                                                    operando2)

    tme = ran(6, 16)
    tiem_trans = 0
    tiem_rest = tme
    tamanio = ran(6,28)
    
    proceso = {
        "id":idx_id, 
        "operando1":operando1,
        "operando2":operando2, 
        "operacion":operacion,
        "resultado":"N/A",
        "tme":tme, 
        "tiem_trans":tiem_trans,
        "tiem_rest":tiem_rest,
        "f_respuesta":0,
        "tiem_bloq":0,
        "tiem_llegada":"N/A",
        "tiem_finalizacion":"N/A",
        "tiem_retorno":"N/A",
        "tiem_respuesta":"N/A",
        "tiem_espera":"N/A",
        "tiem_servicio":"N/A",
        "tamanio":tamanio,
        "estado": "Nuevo"
        }
    idx_id += 1
    return proceso

for i in range(total_procesos):
    os.system("cls")

    nuevos.append(nuevo_proceso())

os.system("cls")

def pulsa(tecla):
    global pause, werror, interrupcion, nuevo, bcp, tab_paginacion
    if pause == 1 or bcp == 1 or tab_paginacion == 1:
        if tecla == kb.KeyCode.from_char('c'):
            pause = 0
            bcp = 0
            tab_paginacion = 0
    else:
        if tecla == kb.KeyCode.from_char('p'):
            pause = 1
        if tecla == kb.KeyCode.from_char('w'):
            werror = 1
        if tecla == kb.KeyCode.from_char('e'):
            interrupcion = 1
        if tecla == kb.KeyCode.from_char('n'):
            nuevo = 1
        if tecla == kb.KeyCode.from_char('b'):
            bcp = 1
        if tecla == kb.KeyCode.from_char('t'):
            tab_paginacion = 1

    

escuchador = kb.Listener(pulsa)
escuchador.start()

def make_layout() -> Layout:
    """Define el layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="head", size=3),
        Layout(name="chest", size=12),
        Layout(name="leg", size=30),
        Layout(name="foot", size=3),
    )
    layout["chest"].split_row(Layout(name="izq"), Layout(name="centro"),
                             Layout(name="der"))
    layout["leg"].split_row(Layout(name="left"), Layout(name="right"))
    layout["foot"].split_row(Layout(name="tiempo"), Layout(name="final"))
    return layout


class Header:
    """Muestra el numero de procesos restantes"""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="right", ratio=1)
        grid.add_column(justify="left", ratio=1)
        try:
            grid.add_row(
                "Procesos restantes: ",
                str(len(nuevos)) + "        Quantum: " + str(quantum) + "        Siguiente: " + str(nuevos[0]["id"]) + ", tamaño: " + str(nuevos[0]["tamanio"]),
                style="grey3",
            )
        except:
            grid.add_row(
                "Procesos restantes: ",
                str(len(nuevos)) + "        Quantum: " + str(quantum),
                style="grey3",
            )

        return Panel(grid, style="white on blue")

def tabla_listos() -> Table:
    """Genera la tabla de listos"""

    table = Table(title="Procesos listos")
        
    table.add_column("Identificador",
                     justify="left",
                     style="light_slate_blue")
    table.add_column("TME", justify="left", style="light_slate_blue")
    table.add_column("Tiempo transcurrido", justify="left", style="light_slate_blue")
    
    for i in range(1,len(listos)):        
        table.add_row(str(listos[i]["id"]),str(listos[i]["tme"]),str(listos[i]["tiem_trans"]))
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
                  style="grey63")
    table.add_row("TME: ",
                  str(listos[proceso_ejecucion]["tme"]),
                  style="grey63")
    table.add_row("Tiempo transcurrido: ", str(listos[proceso_ejecucion]["tiem_trans"]), style="grey63")
    table.add_row("Tiempo restante: ",
                  str(listos[proceso_ejecucion]["tiem_rest"]),
                  style="grey63")
    table.add_row("Quantum transcurrido: ", str(quantum_control), style="grey63")

    return table

def tabla_proceso_ejecucion_fin() -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")
    table.add_row("Identificador: ", style="grey63")
    table.add_row("Operacion: ", style="grey63")
    table.add_row("TME: ", style="grey63")
    table.add_row("Tiempo transcurrido: ", style="grey63")
    table.add_row("Tiempo restante: ", style="grey63")
    table.add_row("Quantum transcurrido: ", style="grey63")
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

def tabla_memoria() ->Table:
    tabla_memoria = Table(title="Memoria")
    tabla_memoria.add_column("No. Marco", justify="left", style="light_slate_blue")
    tabla_memoria.add_column("ESP  ID   EST", justify="left", style="light_slate_blue")
    tabla_memoria.add_column("No. Marco", justify="left", style="light_slate_blue")
    tabla_memoria.add_column("ESP  ID   EST", justify="left", style="light_slate_blue")
    for i in range(0,44,2):
        tabla_memoria.add_row(str(i), str(str(memoria[i][0]) + "  " + memoria[i][1]+ "  " + memoria[i][2]), str(i+1), str(str(memoria[i+1][0]) + "  " + memoria[i+1][1] + "  " + memoria[i+1][2]))

    return tabla_memoria

def nuevo_a_listo_inicial():
    # Seccion de llenado de procesos listos
    global listos, nuevos, memoria
    for i in range(len(nuevos)):
        espacio_memoria = 0
        for frame in memoria:
            if frame[0] == "0/5":
                espacio_memoria += 1
        if espacio_memoria >= nuevos[0]["tamanio"]/5:
            tamanio = nuevos[0]["tamanio"]
            if i == 0:
                nuevos[0]["estado"] = "Ejecucion"
            else:
                nuevos[0]["estado"] = "Listo"

            for frame in memoria:
                if frame[0] == "0/5" and tamanio > 0:
                    if tamanio/5 > 1:
                        frame[0] = "5/5"
                        frame[1] = str(nuevos[0]["id"])
                        frame[2] = nuevos[0]["estado"]
                        tamanio -= 5
                    else:
                        frame[0] = str(tamanio) + "/5"
                        frame[1] = str(nuevos[0]["id"])
                        frame[2] = nuevos[0]["estado"]
                        tamanio = 0
                if tamanio == 0:
                    break
            nuevos[0]["tiem_llegada"] = tiempo_global
            nuevos[0]["tiem_espera"] = 0
            listos.append(nuevos[0])
            nuevos.pop(0)
        else:
            break
        
def nuevo_a_listo():
    # Seccion de llenado de procesos listos
    global listos, nuevos, memoria
    for i in range(len(nuevos)):
        espacio_memoria = 0
        for frame in memoria:
            if frame[0] == "0/5":
                espacio_memoria += 1
        if espacio_memoria >= nuevos[0]["tamanio"]/5:
            tamanio = nuevos[0]["tamanio"]
            if len(listos)==0:
                nuevos[0]["estado"] = "Ejecucion"
            else:
                nuevos[0]["estado"] = "Listo"

            for frame in memoria:
                if frame[0] == "0/5" and tamanio > 0:
                    if tamanio/5 > 1:
                        frame[0] = "5/5"
                        frame[1] = str(nuevos[0]["id"])
                        frame[2] = nuevos[0]["estado"]
                        tamanio -= 5
                    else:
                        frame[0] = str(tamanio) + "/5"
                        frame[1] = str(nuevos[0]["id"])
                        frame[2] = nuevos[0]["estado"]
                        tamanio = 0
                if tamanio == 0:
                    break
            nuevos[0]["tiem_llegada"] = tiempo_global - 1
            nuevos[0]["tiem_espera"] = 0
            listos.append(nuevos[0])
            nuevos.pop(0)
        else:
            break

def listo_a_bloqueado():
    # Seccion de interrupción
    global listos, bloqueados
    try:
        for i in range(len(memoria)):
            if memoria[i][1] == str(listos[0]["id"]):
                memoria[i][2] = "Bloqueado"
        bloqueados.append(listos[0])
        listos.pop(0)
        for i in range(len(memoria)):
            if memoria[i][1] == str(listos[0]["id"]):
                memoria[i][2] = "Ejecucion"
    except:
        pass

def bloqueado_a_listo():
    # Seccion de salida de bloqueados a hacia listos
    global listos, bloqueados
    bloqueados[0]["tiem_bloq"] = 0
    try:
        for i in range(len(memoria)):
            if memoria[i][1] == str(bloqueados[0]["id"]):
                memoria[i][2] = "Listo"
        listos.append(bloqueados[0])
        bloqueados.pop(0)
    except:
        pass

def listo_a_terminado():
    # Seccion de llenado de procesos terminados para tabla final
    global listos, terminados
    try:
        listos[0]["tiem_finalizacion"] = tiempo_global
        listos[0]["estado"] = "Terminado"
        for i in range(len(memoria)):
            if memoria[i][1] == str(listos[0]["id"]):
                memoria[i] = ["0/5","N/A","N/A"]
        
        terminados.append(listos[0])
        listos.pop(0)
        for i in range(len(memoria)):
            if memoria[i][1] == str(listos[0]["id"]):
                memoria[i][2] = "Ejecucion"
    except:
        pass

def ejecucion_a_listo():
    global listos
    try:
        for i in range(len(memoria)):
            if memoria[i][1] == str(listos[0]["id"]):
                memoria[i][2] = "Listo"
        p_ejecucion = listos[0]
        listos.pop(0)
        listos.append(p_ejecucion)
        for i in range(len(memoria)):
            if memoria[i][1] == str(listos[0]["id"]):
                memoria[i][2] = "Ejecucion"
    except:
        pass

nuevo_a_listo_inicial()

layout = make_layout()
layout["head"].update(Header())
layout["chest"].size = 20
layout["chest"]["izq"].update(tabla_listos())
layout["chest"]["izq"].ratio = 2
layout["chest"]["centro"].update(tabla_proceso_ejecucion())
layout["chest"]["centro"].ratio = 3
layout["chest"]["der"].update(tabla_bloqueados())
layout["chest"]["der"].ratio = 2
layout["leg"].size = 30
layout["leg"]["left"].update(table_terminados)
layout["leg"]["right"].update(tabla_memoria())
layout["foot"]["tiempo"].update(tabla_tiempo_global())
layout["foot"]["final"].update(mensaje_final_vacio())

#Seccion del layout de bcp
def make_layout_bcp() -> Layout:
    """Define el layout de bcp"""
    layout_bcp = Layout(name="root")

    layout_bcp.split(
        Layout(name="head")
    )

    return layout_bcp

def make_table_bcp() -> Table:
    """Genera la tabla de procesos bcp"""
    table_bcp = Table(title="Procesos")
    table_bcp.add_column("Identificador",
                                justify="left",
                                style="bold blue")
    table_bcp.add_column("Estado", justify="left", style="bold blue")                            
    table_bcp.add_column("Operacion", justify="left", style="bold blue")
    table_bcp.add_column("Resultado", justify="left", style="bold blue")
    table_bcp.add_column("TLL", justify="left", style="bold blue")
    table_bcp.add_column("TF", justify="left", style="bold blue")
    table_bcp.add_column("TRET", justify="left", style="bold blue")
    table_bcp.add_column("TE", justify="left", style="bold blue")
    table_bcp.add_column("TS", justify="left", style="bold blue")
    table_bcp.add_column("Tiempo restante", justify="left", style="bold blue")
    table_bcp.add_column("TRES", justify="left", style="bold blue")

    return table_bcp

def agregar_proceso_bcp(procesos, estado):
    
    for proceso in procesos:
        try:
            proceso["tiem_retorno"] = proceso["tiem_finalizacion"] - proceso["tiem_llegada"] - 1
        except:
            proceso["tiem_retorno"] = "N/A"
        
        proceso["tiem_servicio"] = proceso["tiem_trans"]
        proceso["tiem_rest"] = proceso["tme"] - proceso["tiem_trans"]
        
        table_bcp.add_row(str(proceso["id"]),
                            estado,
                            str(proceso["operando1"]) + str(proceso["operacion"]) + str(proceso["operando2"]),
                            str(proceso["resultado"]),
                            str(proceso["tiem_llegada"]),
                            str(proceso["tiem_finalizacion"]),
                            str(proceso["tiem_retorno"]),
                            str(proceso["tiem_espera"]),
                            str(proceso["tiem_servicio"]),
                            str(proceso["tiem_rest"]),
                            str(proceso["tiem_respuesta"]),
                            style="grey63")

#Fin de la seccion del layout de bcp
    
with Live(layout, refresh_per_second=20) as live:
    procesos_finalizados = 0
    tiem_bloq_terminado = 0
    f_bcp = 0

    while procesos_finalizados != total_procesos:
        layout["chest"]["der"].update(tabla_bloqueados())
        layout["chest"]["izq"].update(tabla_listos())
        layout["leg"]["right"].update(tabla_memoria())  
        
        if len(listos) > 0:
            layout["chest"]["centro"].update(tabla_proceso_ejecucion())

            if listos[proceso_ejecucion]["f_respuesta"] == 0:
                if listos[proceso_ejecucion]["id"] != 1:
                    listos[proceso_ejecucion]["tiem_respuesta"] = tiempo_global - listos[proceso_ejecucion]["tiem_llegada"]
                    listos[proceso_ejecucion]["f_respuesta"] = 1
                else:
                    listos[proceso_ejecucion]["tiem_respuesta"] = 0
                    listos[proceso_ejecucion]["f_respuesta"] = 1

            
            while quantum_control < quantum:
                while pause == 1 or tab_paginacion == 1:
                    pass
                if bcp == 1:
                    ejecucion = list()
                    try:
                        ejecucion.append(listos[0])
                        listos.pop(0)
                    except:
                        pass
                    f_bcp = 1
                while bcp == 1:
                    layout["head"].visible=False
                    layout["chest"].visible=False
                    layout["leg"]["right"].visible=False
                    table_bcp = make_table_bcp()
                    agregar_proceso_bcp(nuevos,"Nuevo")
                    agregar_proceso_bcp(ejecucion,"Ejecucion")
                    agregar_proceso_bcp(listos,"Listo")
                    agregar_proceso_bcp(bloqueados,"Bloqueado")
                    agregar_proceso_bcp(terminados,"Finalizado")
                    while bcp == 1:
                        layout["leg"]["left"].update(table_bcp)
                
                if f_bcp == 1:
                    try:
                        listos.insert(0,ejecucion[0])
                        ejecucion.pop(0)
                    except:
                        pass
                    break
                if werror == 1:
                    quantum_control = 0
                    break
                if interrupcion == 1:
                    quantum_control = 0
                    listo_a_bloqueado()
                    break
                if nuevo == 1:
                    break
                if listos[proceso_ejecucion]["tiem_rest"] == 0:
                    break
                sleep(1)

                listos[proceso_ejecucion]["tiem_trans"] += 1
                listos[proceso_ejecucion]["tiem_rest"] -= 1
                
                quantum_control += 1

                for i in range (1,len(listos)):
                    try:
                        listos[i]["tiem_espera"] += 1
                    except:
                        pass                

                for proceso in bloqueados:
                    proceso["tiem_espera"] += 1
                    proceso["tiem_bloq"] += 1
                    if proceso["tiem_bloq"] == 8:
                        tiem_bloq_terminado = 1

                layout["chest"]["centro"].update(tabla_proceso_ejecucion())
                layout["chest"]["der"].update(tabla_bloqueados())
                layout["foot"]["tiempo"].update(tabla_tiempo_global())

                if tiem_bloq_terminado == 1:
                    tiem_bloq_terminado = 0
                    interrupcion = 1
                    bloqueado_a_listo()
                    break

                if listos[proceso_ejecucion]["tiem_rest"] == 0:
                    break
            
        else:
            quantum_control = 0
            layout["chest"]["centro"].update(tabla_proceso_ejecucion_fin())
            for i in range(8):
                while pause == 1 or tab_paginacion == 1:
                    pass
                if bcp == 1:
                    f_bcp = 1
                while bcp == 1:
                    layout["head"].visible=False
                    layout["chest"].visible=False
                    layout["leg"]["right"].visible=False
                    table_bcp = make_table_bcp()
                    agregar_proceso_bcp(nuevos,"Nuevo")
                    agregar_proceso_bcp(listos,"Listo")
                    agregar_proceso_bcp(bloqueados,"Bloqueado")
                    agregar_proceso_bcp(terminados,"Finalizado")
                    while bcp == 1:
                        layout["leg"]["left"].update(table_bcp)
                if f_bcp == 1:
                    break
                
                if nuevo == 1:
                    break

                sleep(1)
                for proceso in bloqueados:
                    proceso["tiem_espera"] += 1
                    proceso["tiem_bloq"] += 1
                    if proceso["tiem_bloq"] == 8:
                        tiem_bloq_terminado = 1
                        
                layout["chest"]["der"].update(tabla_bloqueados())
                layout["foot"]["tiempo"].update(tabla_tiempo_global())

                if tiem_bloq_terminado == 1:
                    tiem_bloq_terminado = 0
                    bloqueado_a_listo()
                    break
            if f_bcp == 1:
                pass
            elif nuevo == 1:
                pass
            else:
                interrupcion = 1

        if werror == 1:
            listos[proceso_ejecucion]["tiem_rest"] = 0
        
        if interrupcion == 1:
            interrupcion = 0
        elif nuevo == 1:
            nuevo = 0
            # if  len(listos) + len(bloqueados) < 3:
            #     new_proceso = nuevo_proceso()
            #     new_proceso["tiem_llegada"] = tiempo_global - 1
            #     new_proceso["tiem_espera"] = 0
            #     listos.append(new_proceso)
            # else:
            new_proceso = nuevo_proceso()
            new_proceso["tiem_llegada"] = tiempo_global - 1
            new_proceso["tiem_espera"] = 0
            nuevos.append(new_proceso)
            nuevo_a_listo()
            total_procesos += 1
            layout["head"].update(Header())
        elif f_bcp == 1:
            layout["head"].visible=True
            layout["chest"].visible=True
            layout["leg"]["right"].visible=True
            layout["leg"]["left"].update(table_terminados)
            f_bcp = 0
        elif listos[proceso_ejecucion]["tiem_rest"] != 0 and quantum_control == quantum:
            quantum_control = 0
            ejecucion_a_listo()
        else:
            quantum_control = 0
            #Agregar a la tabla los procesos que ya se finalizaron
            agregar_terminado()
            
            #Aumentar y mantener un control para los procesos
            procesos_finalizados += 1
            
            listo_a_terminado()
            nuevo_a_listo()
            layout["head"].update(Header())

    layout["chest"]["centro"].update(tabla_proceso_ejecucion_fin())
    for frame in memoria:
        frame[0] = "0/5"
        frame[1] = "N/A"
        frame[2] = "N/A"
    layout["leg"]["right"].update(tabla_memoria())
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
    proceso["tiem_retorno"] = proceso["tiem_finalizacion"] - proceso["tiem_llegada"] - 1
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