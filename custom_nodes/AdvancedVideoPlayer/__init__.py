import torch
import numpy as np
import cv2
import os

class AdvancedVideoPlayerBackend:
    # Caché estática para almacenar objetos VideoCapture y metadatos por ruta de archivo
    VIDEO_CACHE = {}

    def __init__(s):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_path": ("STRING", {"default": ""}),
                "command": (["get_info", "get_frame_at_time", "get_frame_at_percent"],),
                "timeline_percent": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 100.0, "step": 0.1, "display": "slider" }),
                "start_frame": ("INT", {"default": 0, "min": 0, "max": 999999, "display": "number"}),
                "end_frame": ("INT", {"default": 0, "min": 0, "max": 999999, "display": "number"}),
                "loop_video": ("BOOLEAN", {"default": False})
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "FLOAT", "INT", "FLOAT")
    RETURN_NAMES = ("frame_image", "info_text", "duration_seconds", "frame_count", "fps")

    FUNCTION = "execute"

    CATEGORY = "Video/Advanced"

    def execute(s, video_path, command, timeline_percent, loop_video, start_frame, end_frame):
        if not os.path.exists(video_path):
            error_msg = f"Error: Video file not found at {video_path}"
            blank_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
            return (blank_image, error_msg, 0.0, 0, 0.0)
        
        # --- Lógica de Caché y Apertura de Video ---
        if video_path not in AdvancedVideoPlayerBackend.VIDEO_CACHE:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                error_msg = f"Error: Could not open video file: {video_path}"
                blank_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
                return (blank_image, error_msg, 0.0, 0, 0.0)

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frame_count / fps if fps > 0 else 0.0
            
            AdvancedVideoPlayerBackend.VIDEO_CACHE[video_path] = {
                "cap": cap,
                "fps": fps,
                "total_frame_count": total_frame_count,
                "duration": duration
            }
        
        # Recuperar de la caché
        cache = AdvancedVideoPlayerBackend.VIDEO_CACHE[video_path]
        cap = cache["cap"]
        fps = cache["fps"]
        total_frame_count = cache["total_frame_count"]
        duration = cache["duration"]

        # --- Lógica de IN/OUT ---
        # Asegurar que end_frame no sea 0 y que no exceda el total
        if end_frame == 0 or end_frame > total_frame_count:
            end_frame = total_frame_count
        
        # El rango de frames a considerar
        start_frame = max(0, start_frame)
        
        # Duración del segmento (en frames)
        segment_frame_count = end_frame - start_frame
        segment_duration = segment_frame_count / fps if fps > 0 else 0.0

        info_text = f"Video Info:\nPath: {video_path}\nDuration: {duration:.2f}s (Total)\nFPS: {fps:.2f}\nFrames: {total_frame_count} (Total)\nLoop Enabled: {loop_video}\nSegment IN/OUT: {start_frame} - {end_frame} ({segment_frame_count} frames)"

        current_frame_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu") # Default blank image

        if command == "get_info":
            # No cerramos cap, ya que está en caché.
            return (current_frame_image, info_text, duration, total_frame_count, fps)

        frame_to_get = -1
        if command == "get_frame_at_time":
            # Calcula el frame absoluto basado en el tiempo, luego lo restringe al segmento
            absolute_frame = int(timeline_percent * fps)
            frame_to_get = max(start_frame, min(end_frame - 1, absolute_frame))
        elif command == "get_frame_at_percent":
            # Calcula el frame relativo al segmento
            relative_frame = int(segment_frame_count * (timeline_percent / 100.0))
            frame_to_get = start_frame + relative_frame
        
        if frame_to_get != -1:
            # Asegurarse de que el frame a obtener esté dentro de los límites del video
            frame_to_get = max(0, min(total_frame_count - 1, frame_to_get))

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_get)
            ret, frame = cap.read()
            # No cerramos cap, ya que está en caché.

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = np.array(frame).astype(np.float32) / 255.0
                current_frame_image = torch.from_numpy(image)[None,]
                info_text += f"\n\nCurrent Frame (Absolute): {frame_to_get}"
            else:
                info_text += "\nWarning: Could not read specified frame."
        else:
            info_text += "\nError: Invalid command for frame extraction."

        return (current_frame_image, info_text, duration, total_frame_count, fps)

NODE_CLASS_MAPPINGS = {
    "AdvancedVideoPlayerBackend": AdvancedVideoPlayerBackend
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedVideoPlayerBackend": "Advanced Video Player Backend"
}
