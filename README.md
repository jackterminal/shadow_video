# ComfyUI-ShadowVideo: Advanced Video Tools

Este repositorio contiene un conjunto de herramientas avanzadas para el procesamiento y control de video dentro de ComfyUI. El primer nodo implementado es el `Advanced Video Player Backend`.

## Nodos Incluidos

*   **`Advanced Video Player Backend`**: Un nodo de backend que permite extraer un frame específico de un video basándose en un porcentaje de tiempo (simulando un *timeline* controlable) y obtener metadatos detallados.

## Instalación

La forma más sencilla de instalar este custom node es a través del **ComfyUI Manager**.

### Instalación Manual (Recomendada)

Sigue estos pasos para instalar el custom node en tu entorno de ComfyUI.

1.  **Clonar el Repositorio:**
    Abre tu terminal y navega al directorio `ComfyUI/custom_nodes/` de tu instalación de ComfyUI. Luego, ejecuta el siguiente comando:
    ```bash
    git clone https://github.com/jackterminal/shadow_video
    ```

2.  **Instalar Dependencias:**
    **¡ATENCIÓN!** Este es el paso donde los principiantes suelen cometer un error. **Debes asegurarte de instalar estas dependencias en el entorno Python que utiliza tu instalación de ComfyUI**, no en el entorno Python de tu sistema.

    Navega al directorio principal del repositorio que acabas de clonar y ejecuta el script `install.py` con el intérprete de Python de ComfyUI:
    ```bash
    cd shadow_video
    # Usa el python de tu entorno ComfyUI. Ejemplo:
    # /ruta/a/tu/comfyui/venv/bin/python install.py
    python install.py
    ```

3.  **Reiniciar ComfyUI:**
    Reinicia ComfyUI. El nuevo nodo `Advanced Video Player Backend` estará disponible en la categoría `Video/Advanced`.

## Uso del Nodo `Advanced Video Player Backend`

Este nodo simula la funcionalidad de un reproductor avanzado:

*   **Timeline (Barra de Tiempo):** El widget `timeline_percent` (un slider) actúa como tu barra de tiempo. Al mover el slider, seleccionas un porcentaje del video (0% al 100%).
*   **Pausa/Stop:** El nodo extrae el frame estático en el punto de tiempo seleccionado, simulando una "pausa" o "stop" en ese momento.
*   **IN/OUT (Selección de Segmento):** Las entradas `start_frame` y `end_frame` permiten definir el segmento de video a procesar.

### Estructura del Repositorio

```
shadow_video/
├── custom_nodes/
│   └── AdvancedVideoPlayer/
│       └── __init__.py  <-- El código del nodo
├── workflows/
│   └── advanced_video_player_simple.json  <-- Workflow de ejemplo
├── requirements.txt  <-- Dependencias de Python
├── install.py  <-- Script de instalación de dependencias
└── README.md
```
