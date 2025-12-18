total = float(input("Ingresa el total: "))
parte = float(input("Ingresa la parte que quieres calcular: "))
porcentaje = (parte / total) * 100

opcion = int(input("¿Quieres decimales? (1 = sí, 2 = no): "))

match opcion:
    case 1:
        decimales = int(input("¿Cuántos decimales quieres mostrar?: "))
        print(f"El porcentaje es: {porcentaje:.{decimales}f}%")
    case 2:
        print(f"El porcentaje es: {int(porcentaje)}%")
    case _:
        print("Opción no válida.")
