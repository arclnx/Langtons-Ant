import pyglet
from pyglet import shapes
from pyglet import clock
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
    batch = pyglet.graphics.Batch()
    buffer = []

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
        self.buffer.append(shapes.Rectangle(
                    self.location[0] * SIZE, 
                    self.location[1] * SIZE,
                    SIZE,
                    SIZE,
                    color=GRID[self.location[0]][self.location[1]],
                    batch = self.batch))

    def debug(self):
        print('direction' + str(self.direction))
        print('location' + str(self.location))

my_ant = Ant(100,100)

@window.event
def on_draw():
    Ant.batch.draw()
    Ant.buffer = []

def update(dt):
    my_ant.iterate()

pyglet.clock.schedule_interval(update, 1/500)
pyglet.app.run()