"""
Monster sprite image loader.

Each monster uses its own pixel-art PNG image
stored inside assets/monsters/.

The images are resized using NEAREST so the
pixel-art style stays sharp.
"""

from PIL import Image, ImageTk


# =========================================================
# MONSTER IMAGE PATHS
# =========================================================

MONSTER_IMAGES = {
    "Leafling": "assets/monsters/m1.png",
    "Flameling": "assets/monsters/m2.png",
    "Aquafin": "assets/monsters/m3.png",
    "Voltwing": "assets/monsters/m4.png",
    "Rockhorn": "assets/monsters/m5.png",
    "Shadowfang": "assets/monsters/m6.png",
    "Sandcoil": "assets/monsters/m7.png",
    "Frostail": "assets/monsters/m8.png",
    "Stormtail": "assets/monsters/m9.png",
}


# =========================================================
# LOAD MONSTER IMAGE
# =========================================================

def load_monster_image(name, size):
    """
    Load a monster PNG and resize it while preserving
    its aspect ratio.

    Returns an ImageTk.PhotoImage.
    """

    image_path = MONSTER_IMAGES.get(name)

    if image_path is None:
        return None

    try:
        image = Image.open(image_path).convert("RGBA")

    except FileNotFoundError:
        print(
            f"Monster image not found: {image_path}"
        )
        return None

    # -----------------------------------------------------
    # PRESERVE ASPECT RATIO
    # -----------------------------------------------------

    original_width, original_height = image.size

    if original_width <= 0 or original_height <= 0:
        return None

    scale = min(
        size / original_width,
        size / original_height
    )

    new_width = max(
        1,
        int(original_width * scale)
    )

    new_height = max(
        1,
        int(original_height * scale)
    )

    # NEAREST keeps pixel art sharp
    image = image.resize(
        (new_width, new_height),
        Image.Resampling.NEAREST
    )

    return ImageTk.PhotoImage(image)


# =========================================================
# DRAW MONSTER
# =========================================================

def draw_monster(canvas, name, size=144):
    """
    Draw a monster image centered on the given canvas.
    """

    canvas.delete("all")

    photo = load_monster_image(
        name,
        size
    )

    if photo is None:

        # Fallback message if image is missing
        canvas.create_text(
            size // 2,
            size // 2,
            text="NO IMAGE",
            fill="white",
            font=("Arial", 10, "bold")
        )

        return

    # -----------------------------------------------------
    # CENTER IMAGE
    # -----------------------------------------------------

    canvas.create_image(
        size // 2,
        size // 2,
        image=photo,
        anchor="center"
    )

    # VERY IMPORTANT:
    # Keep a reference or Tkinter may delete the image.
    canvas.monster_photo = photo