import pyglet

planet_image = pyglet.resource.image("planets-modified.png")
star_image = pyglet.resource.image("sun.jpg")
planet_image.width = 20
planet_image.height = 20
star_image.width = 100
star_image.height = 100


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


center_image(star_image)
center_image(planet_image)
