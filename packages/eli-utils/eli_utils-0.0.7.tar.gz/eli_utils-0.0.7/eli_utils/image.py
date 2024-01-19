from PIL import Image

def resize_image(image: Image.Image, desired_size: int):
    width, height = image.size
    aspect_ratio = width / height

    if width > height:
        new_width = desired_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = desired_size
        new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height))
    return resized_image

