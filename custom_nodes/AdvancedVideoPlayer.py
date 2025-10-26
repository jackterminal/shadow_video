import torch
import numpy as np
import cv2
import os

class AdvancedVideoPlayerBackend:
    def __init__(s):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_path": ("STRING", {"default": ""}),
                "command": (["get_info", "get_frame_at_time", "get_frame_at_percent"],),
                "timeline_percent": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 100.0, "step": 0.1, "display": "slider" }),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "FLOAT", "INT", "FLOAT")
    RETURN_NAMES = ("frame_image", "info_text", "duration_seconds", "frame_count", "fps")

    FUNCTION = "execute"

    CATEGORY = "Video/Advanced"

    def execute(s, video_path, command, timeline_percent):
        if not os.path.exists(video_path):
            error_msg = f"Error: Video file not found at {video_path}"
            blank_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
            return (blank_image, error_msg, 0.0, 0, 0.0)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            error_msg = f"Error: Could not open video file: {video_path}"
            blank_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
            return (blank_image, error_msg, 0.0, 0, 0.0)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0.0

        info_text = f"Video Info:\nPath: {video_path}\nDuration: {duration:.2f}s\nFPS: {fps:.2f}\nFrames: {frame_count}"

        current_frame_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu") # Default blank image

        if command == "get_info":
            cap.release()
            return (current_frame_image, info_text, duration, frame_count, fps)

        frame_to_get = -1
        if command == "get_frame_at_time":
            frame_to_get = int(timeline_percent * fps)
        elif command == "get_frame_at_percent":
            frame_to_get = int(frame_count * (timeline_percent / 100.0))
        
        if frame_to_get != -1:
            if frame_to_get < 0:
                frame_to_get = 0
            if frame_to_get >= frame_count:
                frame_to_get = frame_count - 1

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_get)
            ret, frame = cap.read()
            cap.release()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = np.array(frame).astype(np.float32) / 255.0
                current_frame_image = torch.from_numpy(image)[None,]
                info_text += f"\n\nCurrent Frame: {frame_to_get}"
            else:
                info_text += "\nWarning: Could not read specified frame."
        else:
            info_text += "\nError: Invalid command for frame extraction."

        return (current_frame_image, info_text, duration, frame_count, fps)

NODE_CLASS_MAPPINGS = {
    "AdvancedVideoPlayerBackend": AdvancedVideoPlayerBackend
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedVideoPlayerBackend": "Advanced Video Player Backend"
}
