from pygame import image, transform


def rotate_image(sprite, angle, position, with_alpha):
    """
    Rotate image and calculate its new bounding box
    :param sprite: image to be rotated
    :param angle: angle to rotate by in degree
    :param position: position of the image
    :param with_alpha: if true image will have transparency
    :return: the rotated image and its bounding box
    """
    rotated_image = transform.rotate(sprite, angle)
    rect = rotated_image.get_rect(center=sprite.get_rect(topleft=position).center)

    if with_alpha:
        return rotated_image, rect
    else:
        return rotated_image, rect


class ResourceManager:
    def __init__(self, path):
        self.path = path

    def load_sprite(self, file, with_alpha=True):
        """
        Load image form a file in the specified resource directory
        :param file: filename
        :param with_alpha: if true image will have transparency
        :return: the loaded image
        """
        if with_alpha:
            return image.load(f"{self.path}{file}").convert_alpha()

        else:
            return image.load(f"{self.path}{file}").convert()
