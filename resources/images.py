import pyglet

planet_image = pyglet.resource.image("planets-modified.png")
star_image = pyglet.resource.image("sun.jpg")
center_im = pyglet.resource.image("white_dot-modified.png")
planet_image.width = 10
planet_image.height = 10
star_image.width = 60
star_image.height = 60
center_im.width = 8
center_im.height = 8


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


center_image(star_image)
center_image(planet_image)
center_image(center_im)
