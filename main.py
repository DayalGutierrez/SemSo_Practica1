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
procesos_totales = total_procesos
cinta, lote, identificadores, tiempos = [], [], [], list()
n_lote, n_proceso, lotes_trabajados, proceso_trabajando, tiempo_trans, numero_proceso, procesos_finalizados = 0, 0, 0, 0, 0, 1, 0

while (total_procesos > 0):
    os.system("cls")

    operando1 = ran(-100, 100)
    operando2 = ran(-100, 100)
    n_operacion = ran(1, 6)
    operacion, operando1, operando2 = def_operacion(n_operacion, operando1,
                                                    operando2)

    tme = ran(6,16)
    tiem_trans = 0
    tiem_rest = tme
    tiempos.append(tme)
    proceso = [operando1, operando2, operacion, tme, numero_proceso, tiem_trans, tiem_rest]

    numero_proceso += 1

    if n_proceso == 0:
        cinta.append(lote)
        cinta[n_lote].append(proceso)
        n_proceso += 1
    elif n_proceso == 1:
        cinta[n_lote].append(proceso)
        n_proceso += 1
    else:
        cinta[n_lote].append(proceso)
        n_proceso = 0
        n_lote += 1
        lote = []
        
    total_procesos -= 1

os.system("cls")

#Verificacion para poder la cantidad correcta de lotes que se trabajaran
if procesos_totales % 3 == 0:
    pass
else:
    n_lote += 1

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
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(Layout(name="izq"), Layout(name="centro"),
                             Layout(name="der"))
    return layout


class Header:
    """Muestra el numero de lotes restantes"""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="right", ratio=1)
        grid.add_column(justify="left", ratio=1)
        if n_lote == 0:
            grid.add_row(
                "Lotes restantes: ",
                str(n_lote),
                style="grey3",
            )
        else:
             grid.add_row(
                "Lotes restantes: ",
                str(n_lote-1),
                style="grey3",
            )
        return Panel(grid, style="white on blue")


def tabla_lote_ejecucion(indice1, indice2) -> Table:
    """Genera la tabla del lote en ejecucion"""

    table = Table(title="Lote en ejecucion")
        
    table.add_column("Numero de proceso",
                     justify="left",
                     style="light_slate_blue")
    table.add_column("TME", justify="left", style="light_slate_blue")
    table.add_column("Tiempo transcurrido", justify="left", style="light_slate_blue")
    
    try:
        if cinta[lotes_trabajados][indice1][6] == 0:
            pass
        else:
            table.add_row(str(cinta[lotes_trabajados][indice1][4]),str(cinta[lotes_trabajados][indice1][3]),str(cinta[lotes_trabajados][indice1][5]))
    except:
        pass
    try:
        if cinta[lotes_trabajados][indice2][6] == 0:
            pass
        else:
            table.add_row(str(cinta[lotes_trabajados][indice2][4]),str(cinta[lotes_trabajados][indice2][3]),str(cinta[lotes_trabajados][indice2][5]))
    except:
        pass
    return table


def tabla_proceso_ejecucion(tiem_trans, tiem_restante) -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")

    table.add_row("Numero de programa: ",
                  str(cinta[lotes_trabajados][proceso_trabajando][4]),
                  style="grey63")
    table.add_row("Operacion: ",
                  str(cinta[lotes_trabajados][proceso_trabajando][0]) +
                  str(cinta[lotes_trabajados][proceso_trabajando][2]) +
                  str(cinta[lotes_trabajados][proceso_trabajando][1]),
                  style="medium_purple2")
    table.add_row("TME: ",
                  str(cinta[lotes_trabajados][proceso_trabajando][3]),
                  style="grey63")
    table.add_row("Tiempo transcurrido: ", str(tiem_trans), style="grey63")
    table.add_row("Tiempo restante: ",
                  str(tiem_restante),
                  style="medium_purple2")

    return table


def tabla_proceso_ejecucion_fin() -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")
    table.add_row("Numero de programa: ", style="grey63")
    table.add_row("Operacion: ", style="medium_purple2")
    table.add_row("TME: ", style="grey63")
    table.add_row("Tiempo transcurrido: ", style="medium_purple2")
    table.add_row("Tiempo restante: ", style="grey63")
    return table


"""Genera la tabla del procesos finalizados"""
table_finalizados = Table(title="Procesos finalizados")
table_finalizados.add_column("Nº de programa",
                             justify="left",
                             style="bold blue")
table_finalizados.add_column("Operacion", justify="left", style="bold blue")
table_finalizados.add_column("Resultado", justify="left", style="bold blue")
table_finalizados.add_column("Nº de lote", justify="left", style="bold blue")


def agregar_proceso_fin(color):
    global werror
    no_programa = cinta[lotes_trabajados][proceso_trabajando][4]
    operacion = str(cinta[lotes_trabajados][proceso_trabajando][0]
                    ) + cinta[lotes_trabajados][proceso_trabajando][2] + str(
                        cinta[lotes_trabajados][proceso_trabajando][1])

    if werror == 0:
        if cinta[lotes_trabajados][proceso_trabajando][2] == "+":
            resultado = cinta[lotes_trabajados][proceso_trabajando][0] + cinta[
                lotes_trabajados][proceso_trabajando][1]
        elif cinta[lotes_trabajados][proceso_trabajando][2] == "-":
            resultado = cinta[lotes_trabajados][proceso_trabajando][0] - cinta[
                lotes_trabajados][proceso_trabajando][1]
        elif cinta[lotes_trabajados][proceso_trabajando][2] == "*":
            resultado = cinta[lotes_trabajados][proceso_trabajando][0] * cinta[
                lotes_trabajados][proceso_trabajando][1]
        elif cinta[lotes_trabajados][proceso_trabajando][2] == "/":
            resultado = cinta[lotes_trabajados][proceso_trabajando][0] / cinta[
                lotes_trabajados][proceso_trabajando][1]
        elif cinta[lotes_trabajados][proceso_trabajando][2] == "%":
            resultado = cinta[lotes_trabajados][proceso_trabajando][0] % cinta[
                lotes_trabajados][proceso_trabajando][1]
        elif cinta[lotes_trabajados][proceso_trabajando][2] == "^":
            resultado = cinta[lotes_trabajados][proceso_trabajando][0]**cinta[
                lotes_trabajados][proceso_trabajando][1]
    else:
        resultado = "!Error"
        werror = 0

    table_finalizados.add_row(str(no_programa),
                              operacion,
                              str(resultado),
                              str(lotes_trabajados + 1),
                              style=color)


def tabla_tiempo_trans() -> Table:
    global tiempo_trans
    tiempo_total = Table.grid(expand=True)
    tiempo_total.add_row("Tiempo transcurrido " + str(tiempo_trans),
                         style="light_slate_blue")
    tiempo_trans += 1

    return tiempo_total

def control_proceso():
    global proceso_trabajando
    if proceso_trabajando != 2:
        proceso_trabajando += 1
    else:
        proceso_trabajando = 0

layout = make_layout()
layout["header"].update(Header())
layout["main"].size = 20
layout["main"]["izq"].update(tabla_lote_ejecucion(1,2))
layout["main"]["izq"].ratio = 2
layout["main"]["centro"].update(tabla_proceso_ejecucion(0, 0))
layout["main"]["centro"].ratio = 3
layout["main"]["der"].update(table_finalizados)
layout["main"]["der"].ratio = 4
layout["footer"].update(tabla_tiempo_trans())

with Live(layout, refresh_per_second=20) as live:
    contador_proceso = 1
    aumentar_lote = 0
    color = 0

    proceso_trabajando = 0
    
    while procesos_finalizados != numero_proceso - 1:
        #Apartado para lote en ejecucion
        try:
            while cinta[lotes_trabajados][proceso_trabajando][6] == 0:
                print("Bucle:",cinta[lotes_trabajados][proceso_trabajando][6] == 0)
                print("Proceso trabajando: ",str(proceso_trabajando))
                print("Contenido = ",str(cinta[lotes_trabajados][proceso_trabajando][6]))
                control_proceso()
        except:
            control_proceso()
            try:
                if cinta[lotes_trabajados][proceso_trabajando][6] == 0: control_proceso()
            except: control_proceso()

        if proceso_trabajando == 0:
            layout["main"]["izq"].update(tabla_lote_ejecucion(1,2))
        if proceso_trabajando == 1:
            layout["main"]["izq"].update(tabla_lote_ejecucion(2,0))
        if proceso_trabajando == 2:
            layout["main"]["izq"].update(tabla_lote_ejecucion(0,1))


        # if contador_proceso == 1:
        #     layout["main"]["izq"].update(
        #         tabla_lote_ejecucion(contador_proceso))
        #     contador_proceso += 1
        # elif contador_proceso == 2:
        #     layout["main"]["izq"].update(
        #         tabla_lote_ejecucion(contador_proceso))
        #     contador_proceso += 1
        # elif contador_proceso == 3:
        #     layout["main"]["izq"].update(
        #         tabla_lote_ejecucion(contador_proceso))
        #     contador_proceso = 1
        #     aumentar_lote = 1

        #Apartado de proceso en ejecucion
        c_tiem_trans = cinta[lotes_trabajados][proceso_trabajando][5]
        c_tiem_restante = cinta[lotes_trabajados][proceso_trabajando][6]

        layout["main"]["centro"].update(
            tabla_proceso_ejecucion(c_tiem_trans, c_tiem_restante))
        for j in range(c_tiem_restante):
            while pause == 1:
                pass
            if werror == 1:
                break
            if interrupcion == 1:
                break
            sleep(1)
            c_tiem_trans += 1
            c_tiem_restante -= 1
            layout["main"]["centro"].update(
                tabla_proceso_ejecucion(c_tiem_trans, c_tiem_restante))
            layout["footer"].update(tabla_tiempo_trans())
        
        if werror == 1:
            cinta[lotes_trabajados][proceso_trabajando][6] = 0
        else:
            cinta[lotes_trabajados][proceso_trabajando][6] = c_tiem_restante

        cinta[lotes_trabajados][proceso_trabajando][5] = c_tiem_trans

        if interrupcion == 1:
            control_proceso()
            interrupcion = 0
        else:
            #Agregar a la tabla los procesos que ya se finalizaron
            if color == 0:
                agregar_proceso_fin("grey63")
                color = 1
            else:
                agregar_proceso_fin("medium_purple2")
                color = 0
            
            #Aumentar y mantener un control para los procesos y lotes
            procesos_finalizados += 1
            if procesos_finalizados % 3 == 0:
                aumentar_lote = 1

            control_proceso()
        
            if aumentar_lote == 1:
                lotes_trabajados += 1
                if n_lote == 0:
                    pass
                else:
                    n_lote -= 1
                layout["header"].update(Header())
                aumentar_lote = 0

    layout["main"]["centro"].update(tabla_proceso_ejecucion_fin())

print(layout)