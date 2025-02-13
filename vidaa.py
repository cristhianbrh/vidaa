import cv2
import time
from datetime import datetime

camera = cv2.VideoCapture(0)  # Usa la cámara por defecto. Cambia el índice si usas otra.
fps = 20.0  # Fotogramas por segundo
frame_width = int(camera.get(3))  # Ancho de los fotogramas
frame_height = int(camera.get(4))  # Alto de los fotogramas
frame_size = (frame_width, frame_height)

# Función para generar nombres de archivo basados en la fecha y hora
def get_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"vidaa_{timestamp}.avi"

# Configuración inicial
start_time = time.time()  # Tiempo inicial
out = None  # Objeto para guardar el video

try:
    print("Grabando... Presiona Ctrl+C para detener.")
    while True:
        ret, frame = camera.read()  # Leer un cuadro de la cámara
        if not ret:
            print("Error al capturar el video.")
            break
        
        # Crear un nuevo archivo de video cada 2 minutos
        if time.time() - start_time >= 120 or out is None:
            if out is not None:  # Cierra el archivo anterior si existe
                out.release()
            
            filename = get_filename()
            print(f"Guardando nuevo archivo: {filename}")
            out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), fps, frame_size)
            start_time = time.time()  # Reinicia el temporizador

        out.write(frame)  # Escribir el cuadro en el archivo de 

except KeyboardInterrupt:
    print("\nDetenida por el usuario.")

finally:
    # Limpieza y guardado final
    if out is not None:
        print("Guardando archivo final.")
        out.release()
    camera.release()
    print("Recursos liberados correctamente.")
