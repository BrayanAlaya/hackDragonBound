import tkinter as tk
import math
from pynput import mouse

def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

clics = []

def on_click(x, y, button, pressed):
    if pressed:
        # Almacena la posición del clic
        clics.append((x, y))
        print(f"Clic en: ({x}, {y})")
        
        # Calcular y actualizar la distancia después de cada dos clics
        if len(clics) == 2:
            print(f"Posición del primer clic: {clics[0]}")
            print(f"Posición del segundo clic: {clics[1]}")

            # Calcula la distancia
            distancia = calcular_distancia(clics[0], clics[1])
            print(f"La distancia entre los puntos es: {distancia} píxeles")
            
            # Actualiza la etiqueta de la ventana con la nueva distancia
            etiqueta.config(text=f"Distancia: {distancia:.2f} píxeles")
            
            # Restablece la lista de clics
            clics.clear()

def mostrar_distancia():
    """
    Crea una ventana sin bordes para mostrar la distancia.
    """
    ventana = tk.Tk()
    ventana.title("Distancia")
    
    # Establece la ventana sin bordes
    ventana.overrideredirect(True)
    
    # Hace que la ventana esté siempre encima de otras ventanas
    ventana.attributes("-topmost", True)
    
    # Hace que la ventana sea parcialmente transparente
    ventana.attributes("-alpha", 0.7)

    # Ajusta el tamaño y la posición de la ventana
    ventana.geometry("300x90+100+100")
    
    global etiqueta
    etiqueta = tk.Label(ventana, text="Distancia: -- píxeles", font=("Arial", 14), bg="lightgray", fg="black")
    etiqueta.pack(expand=True, fill="both")

    ventana.mainloop()

# Configurar el listener para el ratón
with mouse.Listener(on_click=on_click) as listener:
    # Ejecutar la ventana de distancia en un hilo separado
    import threading
    hilo_ventana = threading.Thread(target=mostrar_distancia)
    hilo_ventana.start()
    
    # Comenzar a escuchar los clics
    listener.join()
