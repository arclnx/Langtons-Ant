import pyglet
from pyglet import shapes
import time

# Set up global variables
WIDTH = 250
HEIGHT = 250
SIZE = 4
COLORS = [(255,0,0), (0,0,255)]
GRID = [[COLORS[0] for y in range(HEIGHT)] for x in range(WIDTH)] # Fill Grid with first color
RULES = ['L', 'R']
# Set up pyglet window
window = pyglet.window.Window(WIDTH * SIZE, HEIGHT * SIZE)

# Ant
class Ant:
    def __init__(self, x_pos, y_pos):
        self.location = [x_pos, y_pos]
        self.direction = [1,0]
    
    def turn(self, direction):
        if direction == 'R':
            self.direction = [self.direction[1], -1 * self.direction[0]]
        if direction == 'L':
            self.direction = [-1 * self.direction[1],self.direction[0]]
    
    def move(self, distance):
        self.location = [
            direction + location for direction, location in zip(
            [item * distance for item in self.direction], self.location)]
        self.location = [self.location[0] % WIDTH, self.location[1] % HEIGHT]  # Wrap over edge
    
    def iterate(self):
        index = COLORS.index(GRID[self.location[0]][self.location[1]])  # Find index of current color
        GRID[self.location[0]][self.location[1]] = COLORS[
                (index + 1) % len(COLORS)]  # Set cell to next color
        self.turn(RULES[index])  # Turn
        self.move(1)  # Move

    
    def debug(self):
        print('direction' + str(self.direction))
        print('location' + str(self.location))

my_ant = Ant(0,0)

@window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    buffer = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            buffer.append(shapes.Rectangle(
                    x * SIZE, 
                    y * SIZE,
                    SIZE - 1,
                    SIZE - 1,
                    color=GRID[x][y],
                    batch = batch))
    window.clear
    batch.draw()
'''
@window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    buffer = []
    for i in range(0,10):
        buffer.append(shapes.Rectangle(200, 200 + 20 * i, 10, 10, color=(55, 55, 255), batch=batch))
    window.clear
    batch.draw()
'''



pyglet.app.run()