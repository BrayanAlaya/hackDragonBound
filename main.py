import tkinter as tk
import math
from pynput import mouse
import numpy as np

# Lista para almacenar clics
clics = []
distancia_calculada = 0
distance_calculated = False  # Flag to track if the distance is already calculated

# Archivo y hoja de Excel
excel_file = "calculos.xlsx"
sheet_name = "Hoja1"

def on_click(x, y, button, pressed):
    global distance_calculated

    if pressed and not distance_calculated:
        clics.append((x, y))
        print(f"Clic en: ({x}, {y})")
        
        # Calcular y actualizar la distancia después de cada dos clics
        if len(clics) == 2:
            print(f"Posición del primer clic: {clics[0]}")
            print(f"Posición del segundo clic: {clics[1]}")

            # Calcula la distancia
            global distancia_calculada
            distancia_calculada = calcular_distancia(clics[0], clics[1])
            print(f"La distancia entre los puntos es: {distancia_calculada} píxeles")
            
            # Actualiza la etiqueta de la ventana con la nueva distancia
            etiqueta.config(text=f"Distancia: {distancia_calculada:.2f} píxeles")
            
            # Marcar la distancia como calculada para evitar más cambios
            distance_calculated = True
            
            # Restablece la lista de clics
            clics.clear()

def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def reset_distance():
    global distance_calculated
    distance_calculated = False
    etiqueta.config(text="Distancia: -- píxeles")
    print("Distancia restablecida. Puedes hacer clic de nuevo para medir.")


# Definir constantes globales
g = 0.43
K = 0.0039

def calcular():
    global V
    try:
        # jugador
        # entry_alpha.get()
        
        # viento
        # entry_beta.get()
        
        
        # distancia_calculada
        
        gravedad = 0.43
        
        # entry_velocidad_viento.get()
        factorK = 0.0039
        vientoCalculo = factorK * 22
        
        # entry_beta.get()
        vientoGradosRad = math.radians(226)
       
        # entry_alpha.get()
        jugadorGradosRad = math.radians(51)
        
        vBarra = 0
        
        tabla = []
        
        # t2t1                      5000
        # vBarra                    0 0.5 1 ... 40
        # t2                        0
        # t2rad                     0
        # 2*v*cos(jugadorGradosRad) 0
        # raiz                      0
        # t1                        0
        # t1rad                     0
        
        for i in range(81):
            
            t2 = (-vBarra * math.sin(jugadorGradosRad))/ vientoCalculo * math.sin(vientoGradosRad) - gravedad
            t2Red = +round(t2,2)
            
            vcos = round(2 * vBarra * math.cos(jugadorGradosRad),2)
            
            raiz = round(vcos*vcos , 2)  - (4 * (2 * vientoCalculo * math.cos(vientoGradosRad)) * 490)  
            if(raiz < 0):
                raiz = 0
            
            t1 = (-vcos + math.sqrt(raiz)) / 2 * ( 2 * vientoCalculo * math.cos(vientoGradosRad)) 
            t1Red = +round(t1,2)
            
            t2t1 = 5000
            if(raiz != 0):
                t2t1 = abs(t1Red - t2Red) 
            
            tabla.append([t2t1,vBarra,t2,t2Red,vcos,raiz,t1,t1Red])
            
            vBarra+=0.5
            
            defVarible = tabla[0][0];
            
        for i in range(80):
            print(tabla[i][1], " ")
            if(defVarible >= tabla[i][0]):
                
                defVarible = tabla[i][0]
        
       
        t1Table = 0;
        
        print(defVarible)
        
        v = (-gravedad + vientoCalculo * math.sin(vientoGradosRad))         
       
    except ValueError:
        result_text.set("Por favor, ingrese valores válidos.")

def mostrar_distancia():
    global entry_alpha, entry_beta, entry_velocidad_viento, result_text, etiqueta
    
    ventana = tk.Tk()
    ventana.title("Cálculos de Proyectiles")
    ventana.geometry("380x350")

    labels = ["Ángulo Disparo (grados)", "Ángulo Viento (grados)", "Velocidad de Viento"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(ventana, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(ventana)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    entry_alpha, entry_beta, entry_velocidad_viento = entries

    tk.Button(ventana, text="Calcular", command=calcular).grid(row=len(labels), column=0, columnspan=2, pady=10)

    result_text = tk.StringVar()
    result_label = tk.Label(ventana, textvariable=result_text, font=("Arial", 14))
    result_label.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

    # Configuración de la ventana para mostrar la distancia
    etiqueta = tk.Label(ventana, text="Distancia: -- píxeles", font=("Arial", 12), bg="lightgray", fg="black")
    etiqueta.grid(row=len(labels) + 2, column=0, columnspan=2, pady=10)

    # Botón para restablecer la distancia
    tk.Button(ventana, text="Restablecer Distancia", command=reset_distance).grid(row=len(labels) + 3, column=0, columnspan=2, pady=10)

    ventana.mainloop()

# Configurar el listener para el ratón
with mouse.Listener(on_click=on_click) as listener:
    # Ejecutar la ventana de cálculo en un hilo separado
    import threading
    hilo_ventana = threading.Thread(target=mostrar_distancia)
    hilo_ventana.start()
    
    # Comenzar a escuchar los clics
    listener.join()
