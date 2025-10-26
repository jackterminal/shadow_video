# ComfyUI-ShadowVideo: Advanced Video Tools

Este repositorio contiene un conjunto de herramientas avanzadas para el procesamiento y control de video dentro de ComfyUI. El primer nodo implementado es el `Advanced Video Player Backend`, diseñado para simular los controles de un reproductor de video avanzado (timeline, pausa) a través de la interfaz de nodos de ComfyUI.

## Nodos Incluidos

*   **`Advanced Video Player Backend`**: Un nodo de backend que permite extraer un frame específico de un video basándose en un porcentaje de tiempo (simulando un *timeline* controlable) y obtener metadatos detallados.

## Instalación Manual en ComfyUI (Recomendada)

Sigue estos pasos para instalar el custom node en tu entorno de ComfyUI.

1.  **Clonar el Repositorio:**
    Abre tu terminal y navega al directorio `ComfyUI/custom_nodes/` de tu instalación de ComfyUI. Luego, ejecuta el siguiente comando:
    ```bash
    git clone https://github.com/jackterminal/shadow_video
    ```

2.  **Instalar Dependencias:**
    **¡ATENCIÓN!** Este es el paso donde los principiantes suelen cometer un error. **Debes asegurarte de instalar estas dependencias en el entorno Python que utiliza tu instalación de ComfyUI**, no en el entorno Python de tu sistema.

    Navega al directorio principal del repositorio que acabas de clonar y usa el `pip` asociado a tu ComfyUI (a menudo se encuentra en el subdirectorio `venv` o `python_embeded` de tu instalación):
    ```bash
    cd shadow_video
    # Ejemplo de instalación en el entorno de ComfyUI (puede variar según tu instalación)
    # /ruta/a/tu/comfyui/venv/bin/pip install -r requirements.txt
    pip install -r requirements.txt
    ```
    El archivo `requirements.txt` se encuentra en el directorio principal de este repositorio.

3.  **Reiniciar ComfyUI:**
    Reinicia ComfyUI. El nuevo nodo `Advanced Video Player Backend` estará disponible en la categoría `Video/Advanced`.

## Uso del Nodo `Advanced Video Player Backend`

Este nodo simula la funcionalidad de un reproductor avanzado:

*   **Timeline (Barra de Tiempo):** El widget `timeline_percent` (un slider) actúa como tu barra de tiempo. Al mover el slider, seleccionas un porcentaje del video (0% al 100%).
*   **Pausa:** El nodo extrae el frame estático en el punto de tiempo seleccionado, simulando una "pausa" en ese momento.
*   **Play/Pause y Mute:** **Advertencia:** Este nodo es de backend. No incluye botones interactivos de Play/Pause o Mute, ya que esto requiere desarrollo de frontend (JavaScript) que no se puede incluir en este archivo Python. La funcionalidad de "pausa" se logra al seleccionar un frame estático.

### Conexiones

| Entrada/Salida | Tipo | Descripción |
| :--- | :--- | :--- |
| **video_path** (Entrada) | `STRING` | Ruta completa al archivo de video. |
| **command** (Entrada) | `STRING` | Acción a realizar (`get_info`, `get_frame_at_time`, `get_frame_at_percent`). |
| **timeline_percent** (Entrada) | `FLOAT` | Posición en el video (0.0 a 100.0) para extraer el frame. |
| **frame_image** (Salida) | `IMAGE` | El frame extraído en el punto del timeline. Conéctalo a un `PreviewImage`. |
| **info_text** (Salida) | `STRING` | Metadatos del video (duración, FPS, frames). |
| **duration_seconds** (Salida) | `FLOAT` | Duración total del video en segundos. |
| **frame_count** (Salida) | `INT` | Número total de fotogramas. |
| **fps** (Salida) | `FLOAT` | Fotogramas por segundo del video. |

## Estructura del Repositorio

El repositorio está organizado de forma profesional para facilitar la expansión futura:

```
shadow_video/
├── custom_nodes/
│   └── AdvancedVideoPlayer.py  <-- El código del nodo
├── workflows/
│   └── advanced_video_player_simple.json  <-- Workflow de ejemplo
├── requirements.txt  <-- Dependencias de Python
└── README.md
```
