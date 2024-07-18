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
        
        # Detener el listener después de dos clics
        if len(clics) == 2:
            print(f"Posición del primer clic: {clics[0]}")
            print(f"Posición del segundo clic: {clics[1]}")

            # Calcula la distancia
            distancia = calcular_distancia(clics[0], clics[1])
            print(f"La distancia entre los puntos es: {distancia} píxeles")
            
            # Muestra la distancia en la ventana de Tkinter
            mostrar_distancia(distancia)
            
            # Termina el listener
            return False

def mostrar_distancia(distancia):
    
    ventana = tk.Tk()
    ventana.title("Distancia")
    ventana.geometry("200x100")
    
    # Hace que la ventana esté siempre encima de otras ventanas
    ventana.attributes("-topmost", True)
    
    etiqueta = tk.Label(ventana, text=f"Distancia: {distancia:.2f} píxeles", font=("Arial", 14))
    etiqueta.pack(expand=True)
    
    # Botón para cerrar la ventana
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack()

    ventana.mainloop()

# Configurar el listener para el ratón
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

    
# Calcula la distancia
distancia = calcular_distancia(clics[0], clics[1])
print(f"La distancia entre los puntos es: {distancia} píxeles")



