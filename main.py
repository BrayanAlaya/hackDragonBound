from PIL import Image
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

            # Termina el listener
            return False

# Configurar el listener para el ratón
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

    
# Calcula la distancia
distancia = calcular_distancia(clics[0], clics[1])
print(f"La distancia entre los puntos es: {distancia} píxeles")



