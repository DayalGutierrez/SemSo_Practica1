total_procesos = int(input("Ingrese el numero de procesos: "))
cinta, lote, identificadores = [], [], []
n_lote, n_proceso = 0, 0
while(total_procesos > 0):
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
    if n_operacion == 1:
        operacion = "+"
    elif n_operacion == 2:
        operacion = "-"
    elif n_operacion == 3:
        operacion = "*"
    elif n_operacion == 4:
        operacion = "/"
        while operando2 == 0:
            operando2 = int(input("0 no es un divisor valido. Introduzca uno valido: "))
    elif n_operacion == 5:
        operacion = "%"
        while operando2 == 0:
            operando2 = int(input("0 no es un divisor valido. Introduzca uno valido: "))
    elif n_operacion == 6:
        operacion = "^"
        while operando1 == 0 and operando2 == 0:
            print("La potencia de 0^0 no es una operacion valida")
            operando1 = int(input("Ingrese un valor valido para la base: "))
            operando2 = int(input("Ingrese un valor valido para el exponente: "))
    else:
        while(n_operacion > 6 or n_operacion < 1):
            n_operacion = int(input("Numero de opcion no valido. Ingrese el numero valido de la operacion a realizar: "))
            if n_operacion == 1:
                operacion = "+"
            elif n_operacion == 2:
                operacion = "-"
            elif n_operacion == 3:
                operacion = "*"
            elif n_operacion == 4:
                operacion = "/"
                while operando2 == 0:
                    operando2 = int(input("0 no es un divisor valido. Introduzca uno valido: "))
            elif n_operacion == 5:
                operacion = "%"
                while operando2 == 0:
                    operando2 = int(input("0 no es un divisor valido. Introduzca uno valido: "))
            elif n_operacion == 6:
                operacion = "^"
                while operando1 == 0 and operando2 == 0:
                    print("La potencia de 0^0 no es una operacion valida")
                    operando1 = int(input("Ingrese un valor valido para la base: "))
                    operando2 = int(input("Ingrese un valor valido para el exponente: "))
    
    tme = int(input("Introduzca el tiempo maximo estimado: "))
    while(tme <= 0):
        tme = int(input("El tme debe de ser mayor a 0. Introduzca un tiempo maximo estimado valido: "))
    
    iden = input("Introduzca un identificador: ")
    while iden in identificadores:
        iden = input("Identificador ya existente. Introduzca un identificador nuevo:")
    identificadores.append(iden)
    
    proceso = (nombre, operacion, tme, iden)
    if n_proceso == 0:
        print("Proceso n0")
        cinta.append(lote)
        cinta[n_lote].append(proceso)
        n_proceso += 1
    elif n_proceso == 1:
        print("Proceso n1")
        cinta[n_lote].append(proceso)
        n_proceso += 1
    else:
        print("Proceso n2")
        cinta[n_lote].append(proceso)
        n_proceso = 0
        n_lote += 1

    total_procesos -= 1

print(cinta)

