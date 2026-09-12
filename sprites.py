"""
Fast cached Monster GIF animation loader.

- Uses one fixed crop for each animation.
- Caches decoded/cropped GIF frames.
- Caches resized Tkinter PhotoImages by monster and size.
- Revisiting monsters is much faster.
"""

import os
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence, ImageChops

MONSTER_IMAGES = {
    "Leafling": "assets/monsters/test.gif",
    "Flameling": "assets/monsters/test2.gif",
    "Aquafin": "assets/monsters/test3.gif",
    "Voltwing": "assets/monsters/test4.gif",
    "Rockhorn": "assets/monsters/test5.gif",
    "Shadowfang": "assets/monsters/test6.gif",
    "Sandcoil": "assets/monsters/test7.gif",
    "Frostail": "assets/monsters/test8.gif",
    "Stormtail": "assets/monsters/test9.gif",
}

DEFAULT_MONSTER_SIZE = 300
REMOVE_BLACK_BACKGROUND = True
BLACK_THRESHOLD = 30
MIN_FRAME_DELAY = 25
DEFAULT_FRAME_DELAY = 100
MONSTER_PADDING = 6

_gif_states = {}
_raw_animation_cache = {}
_photo_animation_cache = {}

def remove_black_background(image):
    image = image.convert("RGBA")
    red, green, blue, original_alpha = image.split()
    brightness = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    alpha_mask = brightness.point(lambda value: 0 if value <= BLACK_THRESHOLD else 255)
    final_alpha = ImageChops.multiply(original_alpha, alpha_mask)
    image.putalpha(final_alpha)
    return image

def stop_monster_video(canvas):
    state = _gif_states.get(canvas)
    if state is None:
        return
    state["playing"] = False
    after_id = state.get("after_id")
    if after_id is not None:
        try:
            canvas.after_cancel(after_id)
        except tk.TclError:
            pass
    _gif_states.pop(canvas, None)

def show_gif_error(canvas, message):
    canvas.delete("all")
    canvas.update_idletasks()
    width = canvas.winfo_width() if canvas.winfo_width() > 1 else 300
    height = canvas.winfo_height() if canvas.winfo_height() > 1 else 300
    canvas.create_text(
        width // 2,
        height // 2,
        text=message,
        fill="white",
        font=("Arial", 10, "bold")
    )

def get_animation_bbox(frames):
    if not frames:
        return None
    left_min = top_min = right_max = bottom_max = None
    for frame in frames:
        bbox = frame.getchannel("A").getbbox()
        if bbox is None:
            continue
        left, top, right, bottom = bbox
        if left_min is None:
            left_min, top_min, right_max, bottom_max = left, top, right, bottom
        else:
            left_min = min(left_min, left)
            top_min = min(top_min, top)
            right_max = max(right_max, right)
            bottom_max = max(bottom_max, bottom)
    if left_min is None:
        return None
    return (
        max(0, left_min - MONSTER_PADDING),
        max(0, top_min - MONSTER_PADDING),
        min(frames[0].width, right_max + MONSTER_PADDING),
        min(frames[0].height, bottom_max + MONSTER_PADDING),
    )

def load_raw_animation(gif_path):
    cached = _raw_animation_cache.get(gif_path)
    if cached is not None:
        return cached

    gif = Image.open(gif_path)
    raw_frames = []
    durations = []
    default_duration = gif.info.get("duration", DEFAULT_FRAME_DELAY)

    for source_frame in ImageSequence.Iterator(gif):
        frame = source_frame.copy().convert("RGBA")
        if REMOVE_BLACK_BACKGROUND:
            frame = remove_black_background(frame)
        raw_frames.append(frame)

        duration = source_frame.info.get("duration", default_duration)
        if not duration or duration <= 0:
            duration = DEFAULT_FRAME_DELAY
        durations.append(max(MIN_FRAME_DELAY, duration))

    gif.close()

    if not raw_frames:
        result = ([], [])
        _raw_animation_cache[gif_path] = result
        return result

    bbox = get_animation_bbox(raw_frames)
    if bbox is None:
        result = ([], [])
        _raw_animation_cache[gif_path] = result
        return result

    cropped_frames = [frame.crop(bbox) for frame in raw_frames]
    result = (cropped_frames, durations)
    _raw_animation_cache[gif_path] = result
    return result

def load_gif_frames(gif_path, size):
    size = max(1, int(size))
    cache_key = (gif_path, size)
    cached = _photo_animation_cache.get(cache_key)
    if cached is not None:
        return cached

    raw_frames, durations = load_raw_animation(gif_path)
    if not raw_frames:
        return [], []

    crop_width = raw_frames[0].width
    crop_height = raw_frames[0].height
    scale = min(size / crop_width, size / crop_height)
    new_width = max(1, int(crop_width * scale))
    new_height = max(1, int(crop_height * scale))

    photos = []
    for frame in raw_frames:
        resized = frame.resize((new_width, new_height), Image.Resampling.NEAREST)
        photos.append(ImageTk.PhotoImage(resized))

    result = (photos, durations)
    _photo_animation_cache[cache_key] = result
    return result

def play_monster_video(canvas, name, size):
    gif_path = MONSTER_IMAGES.get(name)
    if gif_path is None:
        print(f"[GIF ERROR] No GIF configured for: {name}")
        show_gif_error(canvas, "NO GIF")
        return
    if not os.path.exists(gif_path):
        print(f"[GIF ERROR] File not found: {os.path.abspath(gif_path)}")
        show_gif_error(canvas, "NO GIF")
        return

    try:
        frames, durations = load_gif_frames(gif_path, size)
    except Exception as error:
        print(f"[GIF ERROR] Could not load {gif_path}")
        print(error)
        show_gif_error(canvas, "GIF ERROR")
        return

    if not frames:
        show_gif_error(canvas, "GIF ERROR")
        return

    canvas.update_idletasks()
    canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else size
    canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else size
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    image_id = canvas.create_image(
        center_x,
        center_y,
        anchor="center",
        image=frames[0]
    )

    state = {
        "playing": True,
        "frames": frames,
        "durations": durations,
        "frame_index": 0,
        "image_id": image_id,
        "after_id": None,
    }
    _gif_states[canvas] = state

    def update_frame():
        current_state = _gif_states.get(canvas)
        if current_state is not state or not state["playing"]:
            return

        frame_index = state["frame_index"]
        try:
            canvas.itemconfig(state["image_id"], image=frames[frame_index])
        except tk.TclError:
            stop_monster_video(canvas)
            return

        delay = durations[frame_index]
        state["frame_index"] = (frame_index + 1) % len(frames)
        state["after_id"] = canvas.after(delay, update_frame)

    update_frame()

def draw_monster(canvas, name, size=DEFAULT_MONSTER_SIZE):
    stop_monster_video(canvas)
    canvas.delete("all")
    play_monster_video(canvas, name, size)

def clear_monster_cache():
    _raw_animation_cache.clear()
    _photo_animation_cache.clear()
