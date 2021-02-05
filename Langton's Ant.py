import pyglet
from pyglet import shapes
from pyglet import clock

import colorsys as color
 
# Set up global variables
WIDTH = 240
HEIGHT = 135
SIZE = 8
RULES = ['L', 'R', 'L', 'L', 'R', 'L']

COLOR_FILE = open('colors.txt').readlines()
COLORS = list(map(eval, [COLOR_FILE[color][1:-2] for color in range(0, 63, 63//len(RULES))]))
COLORS = COLORS[:-1]
print(COLORS)
SPEED = 2
#This grid keeps track of the color numbers, the class 'Grid' keeps track of the actual pyglet recteangles and batching
GRID = [[COLORS[0] for y in range(HEIGHT)] for x in range(WIDTH)] # Fill Grid with first color

# Set up pyglet window
window = pyglet.window.Window(WIDTH * SIZE, HEIGHT * SIZE, fullscreen = True)
 
fps_display = pyglet.window.FPSDisplay(window)
 
batch = pyglet.graphics.Batch()
 
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.rects = {}
        for x in range(width):
            self.rects[x] = {}
            for y in range(height):
                self.rects[x][y] = shapes.Rectangle(
                        x * SIZE, 
                        y * SIZE,
                        SIZE,
                        SIZE,
                        color=COLORS[0],
                        batch = batch)
 
my_grid = Grid(WIDTH, HEIGHT)
 
# Ant
class Ant:
    buffer = []
 
    def __init__(self, x_pos, y_pos, grid):
        self.location = [x_pos, y_pos]
        self.direction = [1,0]
        self.grid = grid
    
    def turn(self, direction):
        if direction == 'R':
            self.direction = [self.direction[1], -1 * self.direction[0]]
        if direction == 'L':
            self.direction = [-1 * self.direction[1], self.direction[0]]
        if direction == 'U':
            self.direction = [-1 * self.direction[0], self.direction[1]]
        if direction == 'N':
            self.directiom = self.direction

    def move(self, distance):
        self.location = [
            direction + location for direction, location in zip(
            [item * distance for item in self.direction], self.location)]
        self.location = [self.location[0] % WIDTH, self.location[1] % HEIGHT]  # Wrap over edge
    
    def iterate(self, iterations):
        for iteration in range(iterations):
            index = COLORS.index(GRID[self.location[0]][self.location[1]])  # Find index of current color
            GRID[self.location[0]][self.location[1]] = COLORS[
                    (index + 1) % len(COLORS)]  # Set cell to next color
            self.turn(RULES[index])  # Turn
            self.move(1)  # Move
            self.grid.rects[self.location[0]][self.location[1]].color = GRID[self.location[0]][self.location[1]]
 
    def debug(self):
        print('direction' + str(self.direction))
        print('location' + str(self.location))
 
my_ant = Ant(100,100, my_grid)
 
@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()
 
def update(dt):
    my_ant.iterate(10)
   
pyglet.clock.schedule_interval(update, 1/60)
 
pyglet.app.run()