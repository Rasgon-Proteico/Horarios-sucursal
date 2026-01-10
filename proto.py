import random
import sys
import os


# <--- Colores ---->
def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

RESET = "\033[0m"
BOLD = "\033[1m"

PURPLE = rgb(212, 115, 246,)            
RED = rgb(231,20,20)
CYAN = rgb(12,215,217)                   
WHITE = rgb(255,255,255)                 

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def colorear_celda(texto):
    ancho = 16 
    
    if "DESCANSO" in texto:
        # Primero al centro y luego a colorear
        colorido = f"{texto:^11}" 
        return f"{PURPLE}{colorido}{RESET}"
   
    else:
        # Para los demás turnos 
        return f"{texto:^11}"

limpiar()

def capturar_nombres():
    lista = []
    print(f"{CYAN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║ {RED}                                         {BOLD} Bienvenido a tu creador de horarios                                     {CYAN}║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    
    while True:
        nombre = input(f"Nombre del trabajador {len(lista) + 1}: ")
        if nombre == "":
            break
        lista.append(nombre)
    return lista

mis_trabajadores = capturar_nombres()

# Creamos un diccionario donde todos empiezan con 48 horas por defecto
horas_por_trabajador = {nombre: 48 for nombre in mis_trabajadores}

print("\n¿Todos trabajarán las mismas horas (48h)?")
print(" 1. Si              2. No")
siono = input() 

if siono == "2":
    print("\nIntroduce el nombre de quién tiene horas diferentes y luego sus horas.")
    print("Presiona ENTER en blanco cuando termines.")
    while True:
        quien = input("¿Quién tiene horas diferentes?: ")
        if quien == "":
            break
        
        # Verifica si el nombre existe en nuestra lista original
        if quien in horas_por_trabajador:
            cuantas = int(input(f"¿Cuántas horas totales trabajará {quien}?: "))
            horas_por_trabajador[quien] = cuantas
        else:
            print("Ese nombre no está en la lista de trabajadores. Intenta de nuevo.")


horario = {}
for i, trabajador in enumerate(mis_trabajadores):
    semana = ["-----------"] * 7
    dia_descanso = i % 7
    semana[dia_descanso] = f" DESCANSO  " 
    horario[trabajador] = semana

# Por si falta banda en los turnos
for dia in range(7):
    disponibles = []
    for t in mis_trabajadores:
        if horario[t][dia] == "-----------":
             disponibles.append(t)
    
    random.shuffle(disponibles)
    #Aquí lo mueves en múltiplos de 2, uno apertura y cierre que le damos prioridad
    if len(disponibles) >= 4:            
        horario[disponibles[0]][dia] = "7:00-15:00 "
        horario[disponibles[1]][dia] = "7:00-15:00 "

        horario[disponibles[2]][dia] = "14:00-22:00"
        horario[disponibles[3]][dia] = "14:00-22:00"
        # Si hay más, van a intermedio
        for i in range(4, len(disponibles)):
            horario[disponibles[i]][dia] = "11:00-19:00"

 

# Este será el formato en el que se muestra la tabla
print("\n" + "="*143)
print(f"{'Nombre':<15} | {'Lun':^11} | {'Mar':^11} | {'Mie':^11} | {'Jue':^11} | {'Vie':^11} | {'Sab':^11} | {'Dom':^11} | {'Total':>11}")
print("=" * 143)

for trabajador in mis_trabajadores:
    d = horario[trabajador]

    d_color = [colorear_celda(dia) for dia in d]
    
    # Calcular horas reales trabajadas (8h por cada turno que no sea DESC)
    horas_reales = sum(8 for turno in d if turno in ["7:00-15:00 ", "14:00-22:00", "11:00-19:00"])
    
    print(f"{trabajador:<15} | {d_color[0]} | {d_color[1]} | {d_color[2]} | {d_color[3]} | {d_color[4]} | {d_color[5]} | {d_color[6]} | {WHITE}{horas_reales:>8}h{RESET}")



print("="*143)
