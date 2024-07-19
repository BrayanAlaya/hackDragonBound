import tkinter as tk
import math
from pynput import mouse

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
        # Obtener los valores de entrada
        alpha_degrees = int(entry_alpha.get())
        beta_degrees = int(entry_beta.get())
        velocidad_viento = int(entry_velocidad_viento.get())

        a_ju = velocidad_viento
        a_v = a_ju * K
        # Convertir ángulos de grados a radianes
        alpha = math.radians(alpha_degrees)
        beta = math.radians(beta_degrees)

        # Usar la distancia calculada previamente
        d = distancia_calculada

        # Crear un diccionario para almacenar las diferencias y los valores de V_barra
        diferencias = {}

        # Inicializar V_barra
        V_barra = 0.00
        
        # Valor predeterminado similar a 0.5000 en Excel
        valor_predeterminado = 0.5000
        
        # Iterar sobre el rango de V_barra con pasos de 0.05
        while V_barra <= 40.00:
            # Calcular t2
            t2 = (V_barra * math.sin(alpha)) / (a_v * math.sin(beta) + g)
            t2 = round(t2, 2)  # Redondear t2 a dos decimales

            # Calcular t1 usando la fórmula
            t1_numerator = -2 * V_barra * math.cos(alpha)
            t1_sqrt_part = math.sqrt((2 * V_barra * math.cos(alpha))**2 - 4 * (2 * a_v * math.cos(beta)) * (-d))
            t1_denominator = 4 * a_v * math.cos(beta)
            t1 = (t1_numerator + t1_sqrt_part) / t1_denominator
            t1 = round(t1, 2)  # Redondear t1 a dos decimales

            # Calcular la diferencia entre t1 y t2
            diferencia = t1 - t2

            # Aplicar la lógica condicional similar a Excel
            if V_barra == 0:  # Condición similar a T10 == 0
                diferencia = valor_predeterminado
            else:
                diferencia = abs(diferencia)  # Diferencia absoluta

            # Mostrar resultados de cada iteración
            print(f"V_barra: {V_barra:.2f}, t1: {t1:.2f}, t2: {t2:.2f}, Diferencia: {diferencia:.2f}")

            # Guardar la diferencia en el diccionario
            diferencias[V_barra] = diferencia

            # Incrementar V_barra en 0.05
            V_barra += 0.05

        # Encontrar el valor de V_barra con la menor diferencia
        V_barra_menor_diferencia = min(diferencias, key=diferencias.get)
        menor_diferencia = diferencias[V_barra_menor_diferencia]

        # Mostrar el resultado
        print(f"V_barra con menor diferencia: {V_barra_menor_diferencia:.2f} (Diferencia: {menor_diferencia:.2f})")
        result_text.set(round(V_barra_menor_diferencia,2))
    except ValueError:
        result_text.set("Por favor, ingrese valores válidos.")

def mostrar_distancia():
    global entry_alpha, entry_beta, entry_velocidad_viento, result_text, etiqueta
    
    ventana = tk.Tk()
    ventana.title("Cálculos de Proyectiles")
    ventana.geometry("300x350")

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
