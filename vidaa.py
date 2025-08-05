import cv2
import time
import numpy as np
from datetime import datetime
import os

# Configuración de la cámara
camera = cv2.VideoCapture(0)  # Usa la cámara por defecto.
fps = 20.0  # Fotogramas por segundo
frame_width = 640  # Ancho de la resolución
frame_height = 480  # Alto de la resolución
camera.set(3, frame_width)  # Establecer el ancho
camera.set(4, frame_height)  # Establecer el alto
frame_size = (frame_width, frame_height)

# Configuración de grabación
record_interval = 120  # Intervalo de grabación en segundos
motion_detection = False  # Activar o desactivar la detección de movimiento
motion_threshold = 500  # Umbral para detectar el movimiento (ajustar según necesidad)

# Función para generar nombres de archivo basados en la fecha y hora
def get_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"vidaa_{timestamp}.avi"

# Función para calcular la diferencia entre dos imágenes (detecta el movimiento)
def detect_motion(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(thresh)

# Función para simular un error en la memoria
def memory_error_simulation():
    data = np.zeros((10000, 10000), dtype=np.uint8)
    data[0] = 255
    return data

# Configuración inicial
start_time = time.time()  # Tiempo inicial
out = None  # Objeto para guardar el video
prev_frame = None  # Variable para almacenar el cuadro anterior

# Directorio para guardar los archivos
output_dir = "videos"
os.makedirs(output_dir, exist_ok=True)

try:
    print("Grabando... Presiona Ctrl+C para detener.")
    while True:
        ret, frame = camera.read()  # Leer un cuadro de la cámara
        if not ret:
            print("Error al capturar el video.")
            break

        # Mostrar el contador de tiempo en la pantalla
        elapsed = time.time() - start_time #Error encontrado
        minutes = str(elapsed // 600)
        seconds = str(elapsed % 600)
        timer_text = f"{minutes:02}:{seconds:02}"

        # Intentar simular un error de memoria
        try:
            memory_error_simulation()
        except MemoryError:
            print("Error de memoria detectado: no se puede asignar memoria suficiente.")
            break

        # Detectar movimiento si está habilitado
        if motion_detection and prev_frame is not None:
            motion = detect_motion(prev_frame, frame)
            if motion > motion_threshold:  # Si hay movimiento
                print("Movimiento detectado.")
                if out is None:  # Si no hay grabación en curso, iniciar una nueva
                    filename = get_filename()
                    filepath = os.path.join(output_dir, filename)
                    out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
                    print(f"Comenzando a grabar en {filepath}")

        if not motion_detection or (motion_detection and motion > motion_threshold):
            if time.time() - start_time >= record_interval or out is None:
                if out is not None:  # Cierra el archivo anterior si existe
                    out.release()
                filename = get_filename()
                filepath = os.path.join(output_dir, filename)
                out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
                start_time = time.time()  # Reinicia el temporizador
                print(f"Nuevo archivo guardado: {filepath}")

            # Escribir el cuadro en el archivo de video
            out.write(frame)

        # Mostrar el contador de tiempo en la imagen
        cv2.putText(frame, f"Tiempo: {timer_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar la imagen con el contador
        cv2.imshow("Grabando...", frame)

        # Establecer el cuadro anterior
        prev_frame = frame

        # Esperar una tecla para salir (tecla 'q' para salir)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except cv2.error as e:
    print(f"\nError de OpenCV: {e}")

except MemoryError as e:
    print(f"\nError de Memoria: {e}")

except Exception as e:
    print(f"\nError inesperado: {e}")

finally:
    # Limpieza y guardado final
    if out is not None:
        print("Guardando archivo final.")
        out.release()
    camera.release()
    cv2.destroyAllWindows()  # Cierra la ventana de OpenCV
    print("Recursos liberados correctamente.")
