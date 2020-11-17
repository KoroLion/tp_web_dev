from PIL import Image


def compress_image(img_path, w, h):
    img = Image.open(img_path)
    img.thumbnail((w, h))
    img = img.convert("RGB")
    img.save(img_path, "JPEG", quality=90)
