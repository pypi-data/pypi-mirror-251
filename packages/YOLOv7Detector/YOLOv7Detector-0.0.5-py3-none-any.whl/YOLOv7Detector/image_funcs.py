import cv2


def recolor_image(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image

def resize_image(image):
    height, width = image.shape[:2]

    # Calculate the scale factor
    scale = 800.0 / max(height, width)

    # New dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image
