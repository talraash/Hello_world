import pygame as pg
from random import randrange
from random import uniform
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

# Settings for pygames
resolution = WIDTH, HEIGHT = 1280, 720
FPS = 60

pg.init()
surface = pg.display.set_mode(resolution)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

# pymunk variables
space = pymunk.Space()
space.gravity = 0, 4000
x1 = 1
y1 = 1

segment_shape = pymunk.Segment(space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 5)
space.add(segment_shape)
segment_shape.elasticity = 1.0
segment_shape.friction = 1.0

def platforms(x1, x2, y1):
    platforms_shape = pymunk.Segment(space.static_body, (x1, y1), (x2, y1), 10)
    space.add(platforms_shape)
    platforms_shape.elasticity = 1.0
    platforms_shape.friction = 1.0

def create_figure(space, pos):
    mass, size = randrange(1, 11, 1), (randrange(30, 80), randrange(30, 80))
    points = (0, 0), (50, 0), (20, 80)
    square_moment = pymunk.moment_for_box(mass, size)
    square_body = pymunk.Body(mass, square_moment)
    square_body.position = pos
    square_shape = pymunk.Poly.create_box(square_body, size)
    square_shape.elasticity = uniform (0.1, 1.2)
    square_shape.friction = 1.0
    square_shape.color = [randrange(256) for i in range(4)]
    radius = randrange(20, 40, 5)
    circle_moment = pymunk.moment_for_circle(mass, (radius - 10), radius)
    circle_body = pymunk.Body(mass, circle_moment)
    circle_body.position = pos
    circle_shape = pymunk.Circle(circle_body, radius)
    circle_shape.elasticity = 0.4
    circle_shape.friction = 1.0
    circle_shape.color = [randrange(256) for i in range(4)]
    if mass // 2 == 1 or mass // 2 == 4:
        space.add(square_body, square_shape)
    else:
        space.add(circle_body, circle_shape)


while x1 < HEIGHT:
    x1 = x1 + randrange(40, 1100)
    x2 = x1 + randrange(120, 200)
    y1 = y1 + randrange(180, 240)
    platforms(x1, x2, y1)

while True:
    surface.fill(pg.Color('black'))
    
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_figure(space, i.pos)
                
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    pg.display.flip()
    clock.tick(FPS)
