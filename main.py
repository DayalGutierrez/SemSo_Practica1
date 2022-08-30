import os
from time import sleep
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

console = Console()
def def_operacion(n_operacion,operando1, operando2):
    if n_operacion == 1:
        operacion = "+"
    elif n_operacion == 2:
        operacion = "-"
    elif n_operacion == 3:
        operacion = "*"
    elif n_operacion == 4:
        operacion = "/"
        while operando2 == 0:
            console.print("0 no es un divisor valido. Introduzca uno valido: ", style="bold red", end="") 
            operando2 = int(input())
    elif n_operacion == 5:
        operacion = "%"
        while operando2 == 0:
            console.print("0 no es un divisor valido. Introduzca uno valido: ", style="bold red", end="") 
            operando2 = int(input())
    elif n_operacion == 6:
        operacion = "^"
        while operando1 == 0 and operando2 == 0:
            console.print("La potencia de 0^0 no es una operacion valida", style="bold red")
            operando1 = int(input("Ingrese un valor valido para la base: "))
            operando2 = int(input("Ingrese un valor valido para el exponente: "))
    else:
        console.print("Numero de opcion no valido. Ingrese el numero valido de la operacion a realizar: ", style="bold red", end="")
        n_operacion = int(input(""))
        operacion,operando1,operando2 = def_operacion(n_operacion,operando1,operando2)
    return operacion,operando1,operando2
    
total_procesos = int(input("Ingrese el numero de procesos: "))
procesos_totales = total_procesos
cinta, lote, identificadores, tiempos = [], [], [], list()
n_lote, n_proceso,  lotes_trabajados, procesos_trabajados, tiempo_trans, numero_proceso = 0, 0, 0, 0, 0, 1

while(total_procesos > 0):
    os.system("cls")
    nombre = input("Ingrese su nombre: ")
    print("Menu de operaciones")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicacion")
    print("4. Division")
    print("5. Residuo")
    print("6. Potencia")

    print("El primer operando es minuendo en la resta, el dividendo en la division y el residuo y la base en la potenicia")
    operando1 = int(input("Ingrese el primer operando: "))
    operando2 = int(input("Ingrese el segundo operando: "))
    n_operacion = int(input("Ingrese el numero de la operacion a realizar: "))
    operacion, operando1, operando2 = def_operacion(n_operacion, operando1, operando2)
    
    tme = int(input("Introduzca el tiempo maximo estimado: "))
    while(tme <= 0):
        console.print("El tme debe de ser mayor a 0. Introduzca un tiempo maximo estimado valido: ", style="bold red", end="")
        tme = int(input())
    
    iden = input("Introduzca un identificador: ")
    while iden in identificadores:
        console.print("Identificador ya existente. Introduzca un identificador nuevo: ", style="bold red", end="")
        iden = input()
    identificadores.append(iden)

    tiempos.append(tme)
    proceso = (nombre, operando1, operando2, operacion, tme, iden, numero_proceso)

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

def make_layout() -> Layout:
    """Define el layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="izq"),
        Layout(name="centro"),
        Layout(name="der")
    )
    return layout

class Header:
    """Muestra el numero de lotes restantes"""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="right", ratio=1)
        grid.add_column(justify="left", ratio=1)
        grid.add_row(
            "Lotes restantes: ", str(n_lote-1), style="grey3",
        )
        return Panel(grid, style="white on blue")

def tabla_lote_ejecucion(limite) -> Table:
    """Genera la tabla del lote en ejecucion"""

    table = Table(title ="Lote en ejecucion")
    table.add_column("Nombre de programador", justify="left", style="light_slate_blue")
    table.add_column("TME", justify="left", style="light_slate_blue")
    
    for row in range(limite,3):
        try:
            
            table.add_row(
                cinta[lotes_trabajados][row][0],str(cinta[lotes_trabajados][row][4])
                )
        except:
            pass
    return table
        
def tabla_proceso_ejecucion(tiem_trans, tiem_restante) -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title ="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")
    
    table.add_row(
                "Nombre del programador: ",str(cinta[lotes_trabajados][procesos_trabajados][0]),style="grey63"
            )
    table.add_row(
                "Operacion: ",str(cinta[lotes_trabajados][procesos_trabajados][1]) + str(cinta[lotes_trabajados][procesos_trabajados][3]) + str(cinta[lotes_trabajados][procesos_trabajados][2]), style="medium_purple2"
            )
    table.add_row(
                "TME: ",str(cinta[lotes_trabajados][procesos_trabajados][4]), style="grey63"
            )
    table.add_row(
                "Numero de programa: ", str(cinta[lotes_trabajados][procesos_trabajados][6]), style="medium_purple2"
            )
    table.add_row(
                "Tiempo transcurrido: ", str(tiem_trans), style="grey63"
            )
    table.add_row(
                "Tiempo restante: ", str(tiem_restante), style="medium_purple2"
            )

    return table

def tabla_proceso_ejecucion_fin() -> Table:
    """Genera la tabla del proceso en ejecucion"""
    table = Table(title ="Proceso en ejecucion")
    table.add_column("Datos", justify="left", style="bold blue")
    table.add_column("Informacion", justify="left", style="bold blue")
    table.add_row(
                "Nombre del programador: ", style="grey63"
            )
    table.add_row(
                "Operacion: ", style="medium_purple2"
            )
    table.add_row(
                "TME: ", style="grey63"
            )
    table.add_row(
                "Numero de programa: ",  style="medium_purple2"
            )
    table.add_row(
                "Tiempo transcurrido: ", style="grey63"
            )
    table.add_row(
                "Tiempo restante: ",  style="medium_purple2"
            )
    return table

"""Genera la tabla del procesos finalizados"""
table_finalizados = Table(title ="Procesos finalizados")
table_finalizados.add_column("Nº de programa", justify="left", style="bold blue")
table_finalizados.add_column("Operacion", justify="left", style="bold blue")
table_finalizados.add_column("Resultado", justify="left", style="bold blue")
table_finalizados.add_column("Nº de lote", justify="left", style="bold blue")

def agregar_proceso_fin(color):
    no_programa = cinta[lotes_trabajados][procesos_trabajados][6]
    operacion = str(cinta[lotes_trabajados][procesos_trabajados][1]) + cinta[lotes_trabajados][procesos_trabajados][3] + str(cinta[lotes_trabajados][procesos_trabajados][2])
    
    if cinta[lotes_trabajados][procesos_trabajados][3] == "+":
        resultado = cinta[lotes_trabajados][procesos_trabajados][1] + cinta[lotes_trabajados][procesos_trabajados][2]
    elif cinta[lotes_trabajados][procesos_trabajados][3] == "-":
        resultado = cinta[lotes_trabajados][procesos_trabajados][1] - cinta[lotes_trabajados][procesos_trabajados][2]
    elif cinta[lotes_trabajados][procesos_trabajados][3] == "*":
        resultado = cinta[lotes_trabajados][procesos_trabajados][1] * cinta[lotes_trabajados][procesos_trabajados][2]
    elif cinta[lotes_trabajados][procesos_trabajados][3] == "/":
        resultado = cinta[lotes_trabajados][procesos_trabajados][1] / cinta[lotes_trabajados][procesos_trabajados][2]
    elif cinta[lotes_trabajados][procesos_trabajados][3] == "%":
        resultado = cinta[lotes_trabajados][procesos_trabajados][1] % cinta[lotes_trabajados][procesos_trabajados][2]
    elif cinta[lotes_trabajados][procesos_trabajados][3] == "^":
        resultado = cinta[lotes_trabajados][procesos_trabajados][1] ** cinta[lotes_trabajados][procesos_trabajados][2]
        
    table_finalizados.add_row(str(no_programa),operacion,str(resultado),str(lotes_trabajados+1), style=color)
    

def tabla_tiempo_trans() -> Table:
    global tiempo_trans
    tiempo_total = Table.grid(expand=True)
    tiempo_total.add_row(
        "Tiempo transcurrido " + str(tiempo_trans), style="light_slate_blue"
    )
    tiempo_trans += 1
    
    return tiempo_total



layout = make_layout()
layout["header"].update(Header())
layout["main"].size = 20
layout["main"]["izq"].update(tabla_lote_ejecucion(1))
layout["main"]["izq"].ratio = 2
layout["main"]["centro"].update(tabla_proceso_ejecucion(0,0))
layout["main"]["centro"].ratio = 3
layout["main"]["der"].update(table_finalizados)
layout["main"]["der"].ratio = 4
layout["footer"].update(tabla_tiempo_trans())

with Live(layout, refresh_per_second=10) as live:
    contador_proceso = 1
    aumentar_lote = 0
    color = 0
    for i in range(numero_proceso-1):
        #Apartado para lote en ejecucion
        if contador_proceso == 1:
            layout["main"]["izq"].update(tabla_lote_ejecucion(contador_proceso))
            contador_proceso += 1
        elif contador_proceso == 2:
            layout["main"]["izq"].update(tabla_lote_ejecucion(contador_proceso))
            contador_proceso += 1
        elif contador_proceso == 3:
            layout["main"]["izq"].update(tabla_lote_ejecucion(contador_proceso))
            contador_proceso = 1
            aumentar_lote = 1

        #Apartado de proceso en ejecucion
        c_tiem_trans = 0
        c_tiem_restante = tiempos[i]

    
        
        layout["main"]["centro"].update(tabla_proceso_ejecucion(c_tiem_trans,c_tiem_restante))
        for j in range(tiempos[i]):
            sleep(1)
            c_tiem_trans += 1
            c_tiem_restante -= 1
            layout["main"]["centro"].update(tabla_proceso_ejecucion(c_tiem_trans,c_tiem_restante))
            layout["footer"].update(tabla_tiempo_trans())

        
        #Agregar a la tabla los procesos que ya se finalizaron
        if color == 0:
            agregar_proceso_fin("grey63")
            color = 1
        else:
            agregar_proceso_fin("medium_purple2")
            color = 0
            
        #Aumentar y mantener un control para los procesos y lotes
        if procesos_trabajados == 2:
            procesos_trabajados = -1
        procesos_trabajados += 1 
        
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