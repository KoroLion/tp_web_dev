from PIL import Image


def compress_image(img_path, w, h, keep_aspect_ratio=True):
    img = Image.open(img_path)
    if keep_aspect_ratio:
        img.thumbnail((w, h))
    else:
       img = img.resize((w, h))
    img = img.convert("RGB")
    img.save(img_path, "JPEG", quality=90)
