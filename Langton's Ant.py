import pyglet
from pyglet import shapes

WIDTH = 10
HEIGHT = 10
GRID = [[0 for y in range(HEIGHT)] for x in range(WIDTH)]
COLORS = [(0,0,0), (255,255,255)]
RULES = ['L', 'R']

class Ant:
    def __init__(self, x_pos, y_pos):
        self.location = [x_pos, y_pos]
        self.direction = [1,0]
    
    def turn(self, direction):
        if direction == 'R':
            self.direction = [-1 * self.direction[1], self.direction[0]]
        if direction == 'L':
            self.direction = [self.direction[1], -1 * self.direction[0]]
    
    def move(self, distance):
        #[a + b for (a, b) in zip(list1, list2)]
        self.location = [
            direction + location for direction, location in zip(
            [item * distance for item in self.direction], self.location)]
    
    def iterate(self):
        GRID[self.location[0]][self.location[1]] = 
    
    def debug(self):
        print('direction' + str(self.direction))
        print('location' + str(self.location))
        print('color' + str(self.color))

my_ant = Ant(0,0)
my_ant.debug()
my_ant.move(1)
my_ant.debug()