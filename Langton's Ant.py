import pyglet
from pyglet import shapes
from pyglet import clock
from pyglet.window import key, mouse
import pyglet.gl as gl
import random as rand
 
# Set up global variables
WIDTH = 320
HEIGHT = 180-48
SIZE = 6
RULES = [['L','R'][rand.randint(0,1)] for turn in range(5)]
#['L', 'R', 'R', 'R',]
#['L', 'R']
#
#['L', 'L', 'R', 'R']
SPEED = 2
PAUSED = False
ITERATIONS = 0

# Set up colors
COLOR_FILE = open('colors.txt').readlines()
COLORS = list(map(eval, COLOR_FILE[:len(RULES)]))

# Set up pyglet window
window = pyglet.window.Window(WIDTH * SIZE, HEIGHT * SIZE, fullscreen = False)
batch = pyglet.graphics.Batch()
text = pyglet.graphics.Batch()

# Change cursor to crosshair
window.set_mouse_cursor(window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR))

# Set up text displays
fps_display = pyglet.window.FPSDisplay(window)
speed_label = pyglet.text.Label('Speed (iterations/frame): ',
                          font_name='Arial',
                          font_size=16,
                          x=100, y=5,
                          anchor_x='left', anchor_y='bottom',
                          color = (255,255,255,255),
                          batch = text)
pause_label = pyglet.text.Label('Paused' if PAUSED else '',
                          font_name='Arial',
                          font_size=16,
                          x=700, y=5,
                          anchor_x='left', anchor_y='bottom',
                          color = (255,0,0,255),
                          batch = text)
iter_label = pyglet.text.Label('Iterations: ' + str(ITERATIONS),
                          font_name='Arial',
                          font_size=16,
                          x=400, y=5,
                          anchor_x='left', anchor_y='bottom',
                          color = (255,255,255,255),
                          batch = text)
mouse_label =pyglet.text.Label('x=mouse_x, y=mouse_y, color=mouse_color',
                          font_name='Arial',
                          font_size=16,
                          x=WIDTH*SIZE-225
                          , y=5,
                          anchor_x='left', anchor_y='bottom',
                          color = (255,255,255,255),
                          batch = text)

# Set up function to update text displays
def update_labels():
    speed_label.text = 'Speed (iterations/frame): ' + str(SPEED)
    pause_label.text = 'Paused' if PAUSED else ''
    iter_label.text = 'Iterations: ' + str(ITERATIONS)


# Function to pause/unpause the simulation
def pause():
    global PAUSED
    PAUSED = not(PAUSED)


# Grid
class Grid:
    scale = 1
    grid_x = 0
    grid_y = 0
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
    
    def zoom(self, factor, center_x, center_y):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect =  self.rects[x][y]
                self.rects[x][y].x = (rect.x - center_x)*factor + center_x
                self.rects[x][y].y = (rect.y - center_y)*factor + center_y
                self.rects[x][y].width = rect.width * factor
                self.rects[x][y].height = rect.height * factor

    def move(self, move_x, move_y):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect =  self.rects[x][y]
                self.rects[x][y].x = rect.x + move_x
                self.rects[x][y].y = rect.y + move_y

my_grid = Grid(WIDTH, HEIGHT)

# Ant
class Ant:
 
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
            index = COLORS.index(tuple(self.grid.rects[self.location[0]][self.location[1]].color))  # Find index of current color
            self.grid.rects[self.location[0]][self.location[1]].color = COLORS[
                    (index + 1) % len(COLORS)]  # Set cell to next color
            self.turn(RULES[index])  # Turn
            self.move(1)  # Move
 
    def debug(self):
        print('direction' + str(self.direction))
        print('location' + str(self.location))
 
my_ant = Ant(100,100, my_grid)


# Draw the screen every frame
@window.event
def on_draw():
    window.clear()

    update_labels()

    batch.draw()
    text.draw()
    fps_display.draw()


# Handle keypresses
@window.event
def on_key_press(symbol, modifiers):
    global SPEED
    if symbol == key.UP:
        SPEED += 1
    if symbol == key.DOWN:
        SPEED -= 1
    if symbol == key.LEFT:
        SPEED -= 10
    if symbol == key.RIGHT:
        SPEED += 10
    SPEED = max(SPEED, 0)    
    if symbol == key.SPACE:
        pause()

# Handle mouse motion.
@window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_label.text = ('x=' + str(x//SIZE + 1).zfill(3) +
                        ', y=' + str(y//SIZE + 1).zfill(3) +
                        ', color=' + str(COLORS.index(tuple(my_ant.grid.rects[x//SIZE][y//SIZE].color))))

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y > 0:
        my_grid.zoom(2, x, y)
    if scroll_y < 0:
        my_grid.zoom(.5, x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.MIDDLE:
        my_grid.move(dx, dy)



# Actions to peform every 1/60 of a second
def update(dt):
    global ITERATIONS
    my_ant.iterate(SPEED if not PAUSED else 0)
    ITERATIONS += SPEED if not PAUSED else 0

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()