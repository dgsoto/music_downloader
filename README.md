# Music Downloader CLI

Bienvenido a Music Downloader CLI, una herramienta profesional de línea de comandos para descargar, convertir y gestionar música.



## Características

* **Arquitectura Modular y Escalable:** El proyecto está diseñado con módulos separados para fuentes (`sources`), metadatos (`metadata`) y conversión (`converters`), lo que permite una fácil expansión.
* **Interfaz de Usuario Afectiva:** Utiliza la librería `rich` para una experiencia de usuario atractiva y profesional con colores, tablas y animaciones.
* **Descarga por Lotes y Listas de Reproducción:** Descarga múltiples URLs o listas de reproducción completas con un solo comando.
* **Etiquetado Automático de Metadatos:** La herramienta busca y aplica automáticamente las etiquetas de metadatos (título, artista) a los archivos descargados.
* **Búsqueda Integrada:** Busca música directamente desde la CLI en las fuentes compatibles.
* **Modo Interactivo:** Guía a los nuevos usuarios a través de un flujo intuitivo, sin necesidad de recordar comandos.

## Requisitos

Asegúrate de tener Python 3.7 o superior instalado.

**Requisito adicional para la conversión (`convert`):**
Debes tener **FFmpeg** instalado y accesible en tu PATH. Puedes descargarlo desde [ffmpeg.org](https://ffmpeg.org/). 

## Instalación

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/dgsoto/music_downloader.git](https://github.com/dgsoto/music_downloader.git)
    cd music_downloader
    ```

2.  **Crea y activa un entorno virtual (recomendado):**
    ```bash
    # Crea el entorno virtual
    python -m venv venv

    # Activa el entorno virtual
    # En macOS/Linux:
    source venv/bin/activate
    # En Windows:
    venv\Scripts\activate
    ```

3.  **Instala las dependencias del proyecto:**
    ```bash
    pip install -r requirements.txt
    ```

## Uso

El comando principal es `python src/cli.py`.

### 1. Descargar Música

Descarga una o varias URLs de canciones o listas de reproducción.
```bash
# Descarga una sola canción
python src/cli.py download <URL_DE_LA_CANCION>

# Descarga múltiples canciones
python src/cli.py download <URL_1> <URL_2>

# Descarga una lista de reproducción completa
python src/cli.py download <URL_DE_LA_PLAYLIST>