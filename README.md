# vidaa

`vidaa` es una aplicación que graba video desde la cámara predeterminada y guarda los archivos en formato AVI. La aplicación crea un nuevo archivo de video cada 2 minutos.

## Requisitos

- Python 3.x
- OpenCV

## Instalación

1. Instala OpenCV:
    ```bash
    pip install opencv-python
    ```

2. Clona este repositorio o descarga el archivo `vidaa.py`.

## Uso

Ejecuta el script `vidaa.py` para comenzar a grabar video:

```bash
python vidaa.py
```

La aplicación comenzará a grabar video y guardará los archivos en el mismo directorio con nombres basados en la fecha y hora actuales.

## Detener la grabación

Para detener la grabación, presiona `Ctrl+C` en la terminal. La aplicación guardará el archivo de video actual y liberará los recursos correctamente.

## Notas

- La aplicación usa la cámara predeterminada del sistema. Si deseas usar otra cámara, cambia el índice en la línea `camera = cv2.VideoCapture(0)`.
- Los archivos de video se guardan en formato AVI con el códec XVID.