import pygame as pg
import math
import sys
from tkinter import filedialog
pg.init()

# PYGAME SETUP
screenWidth, screenHeight = 1800, 1000
WIN = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Bézier Curves")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

class Node():
    def __init__(self, x, y, deg=0, rad=10):
        self.x = x
        self.y = y
        self.deg = deg
        self.rad = rad

    def draw(self):
        
        if self.deg == 0:
            pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad)
            pg.draw.circle(WIN, WHITE, (self.x, self.y), self.rad, 2)

        elif self.deg == len(initial)-1:
            pg.draw.circle(WIN, GREEN, (self.x, self.y), self.rad)
        else:
            pg.draw.circle(WIN, WHITE, (self.x, self.y), self.rad)

    def hover(self):
        x, y = pg.mouse.get_pos()
        return math.dist((x, y), (self.x, self.y)) <= self.rad        

class Slider():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = 50
        self.rad = 10
        self.color = WHITE
        self.inSlide = False

    def draw(self):
        # Draw line
        pg.draw.line(WIN, WHITE, (30, self.y), (180, self.y), 3)

        # Draw circle
        
        pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad)
        pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad, 5)
        
        # Draw text
        font = pg.font.SysFont('georgia', 25)
        text = font.render(str(self.val), True, WHITE)
        textW, _ = font.size(str(self.val))

        WIN.blit(text, (self.x - (textW/2), self.y + (self.rad*1.2)))

    def hover(self):
        x, y = pg.mouse.get_pos()
        return math.dist((x, y), (self.x, self.y)) <= self.rad

    def move(self):
        if self.hover() and click:
            self.inSlide = True
        
        if self.inSlide:
            x, _ = pg.mouse.get_pos()
            self.x = x
            if self.x < 30:
                self.x = 30
            elif self.x > 180:
                self.x = 180
            self.val = round((self.x - 30)/1.5)
            if self.val == 0:
                self.val = 1


def connect_nodes(n1, n2):
    if len(initial) == 2:
        red = 255
    else:
        size = len(initial) - 2
        red = (255/size) * n1.deg

    pg.draw.line(WIN, (red, 0, 120), (n1.x, n1.y), (n2.x, n2.y), 2)

def draw(t):
    WIN.fill(BLACK)

    for degree in nodes:
        # Draw lines between nodes
        for i, node in enumerate(degree):
            if node == degree[-1]:
                break
            connect_nodes(node, degree[i+1])

    # Display all nodes   
    for degree in nodes:
        for node in degree:
            node.draw()

    # Display trail
    for i, point in enumerate(trail):
        if point == trail[-1]:
            break
        
        pg.draw.line(WIN, GREEN, (point), (trail[i+1]), 2)

    # Display slider
    slider.draw()

    # Display text
    myfont = pg.font.SysFont('georgia', 48)
    textsurface = myfont.render("SPEED", True, WHITE)
    WIN.blit(textsurface,(30, 885))

    myfont = pg.font.SysFont('georgia', 58)
    textsurface = myfont.render("BÉZIER CURVES", True, (160, 0, 120))
    WIN.blit(textsurface,(1317, 915))
    textsurface = myfont.render("BÉZIER CURVES", True, WHITE)
    WIN.blit(textsurface,(1320, 915))

    myfont = pg.font.SysFont('georgia', 48)
    textsurface = myfont.render(f"n = {len(initial)}", True, WHITE)
    WIN.blit(textsurface,(215, 880))

    textsurface = myfont.render("t = {:.2f}".format(t), True, WHITE)
    WIN.blit(textsurface,(225, 930))


    myfont = pg.font.SysFont('georgia', 20)

    # Display control icons
    spacebar = pg.image.load("Sprites\\Spacebar.png").convert_alpha()
    WIN.blit(spacebar, (480, 890))
    textsurface = myfont.render("Play/Pause", True, WHITE)
    WIN.blit(textsurface,(493, 960))

    rKey = pg.image.load("Sprites\\R Key.png").convert_alpha()
    WIN.blit(rKey, (740, 890))
    textsurface = myfont.render("Reset", True, WHITE)
    WIN.blit(textsurface,(749, 960))

    leftMouse = pg.image.load("Sprites\\Left Mouse.png").convert_alpha()
    WIN.blit(leftMouse, (950, 890))
    textsurface = myfont.render("Drag Nodes", True, WHITE)
    WIN.blit(textsurface,(918, 960))

    rightMouse = pg.image.load("Sprites\\Right Mouse.png").convert_alpha()
    WIN.blit(rightMouse, (1150, 890))
    textsurface = myfont.render("Add/Delete Nodes", True, WHITE)
    WIN.blit(textsurface,(1090, 960))

    pg.display.update()

def get_middle_node(n1, n2, t):
    xDif = abs(n1.x - n2.x)
    yDif = abs(n1.y - n2.y)

    xDif *= t
    yDif *= t

    if n1.x < n2.x:
        x = n1.x + xDif
    else:
        x = n1.x - xDif
    
    if n1.y < n2.y:
        y = n1.y + yDif
    else:
        y = n1.y - yDif

    return x, y

def calculate_all_nodes(initial, t):
    nodes = []
    nodes.append(initial)

    for degree in range(len(initial)-1):

        nextDegree = []
        for j, node in enumerate(nodes[degree]):
            if node == nodes[degree][-1]:
                break

            x, y = get_middle_node(node, nodes[degree][j+1], t)

            if degree+1 > 0:
                nextDegree.append(Node(x, y, degree+1, 5))
            else:
                nextDegree.append(Node(x, y, degree+1, 5))

        nodes.append(nextDegree)

    return nodes

def move_nodes(initial, click):
    global movingNode

    for node in initial:
        if node.hover() and click:
            movingNode = node
    
    if movingNode:
        movingNode.x, movingNode.y = pg.mouse.get_pos()
            
    return initial

def add_node(pos):
    x = pos[0]
    y = pos[1]
    if len(initial) != 100:
        initial.append(Node(x, y))    

def kill_node(i):
    if len(initial) > 2:
        del initial[i]

def get_trail(initial, T, speed):
    trail = []
    t = 0
    end = False
    while True:
        if t > T:
            t = T
            end = True

        nodes = calculate_all_nodes(initial, t)
        finalNode = nodes[-1][0]

        if len(trail) > 0:
            trail.append((finalNode.x, finalNode.y))

        else:
            trail.append((nodes[0][0].x, nodes[0][0].y))

        t += speed/10000

        if end:
            break
    return trail

def save_state():
    filePath = filedialog.asksaveasfilename(defaultextension="txt", filetypes=[("Text File", ".txt")])
    if filePath:
        file = open(filePath, "w")
        
        data = []
        for i, node in enumerate(initial):
            if node == initial[-1]:
                data.append(f"{node.x}, {node.y}")
                break
            data.append(f"{node.x}, {node.y}\n")
        file.writelines(data)
        

def load_state():
    filePath = filedialog.askopenfilename()
    if filePath:
        file = open(filePath, "r")
        data = file.readlines()
        for i, line in enumerate(data):
            data[i] = (int(line.strip().split(", ")[0]), int(line.strip().split(", ")[1]))
       
        initial = []
        for pair in data:
            initial.append(Node(pair[0], pair[1]))

    return initial

def main():
    global nodes, initial, trail, movingNode, click

    clock = pg.time.Clock()
    t = 0
    trail = []
    go = False
    movingNode = None
    speed = slider.val

    # MAIN LOOP
    while True:
        clock.tick(FPS)
        click = False
        speed = slider.val

        # EVENTS
        for event in pg.event.get():
            
            # Quit
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            
            # Toggle play
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                go = not go
                if t == 1:
                    t = 0
                    go = False
                    trail = []

            # Mouse
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                movingNode = None
                slider.inSlide = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                
                killed = False
                # Kill node
                for i, node in enumerate(initial):
                    if node.hover():
                        kill_node(i)
                        killed = True

                # Add node
                if not killed:
                    add_node(event.pos)

            # Reset
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                initial = [Node(601, 771), Node(601, 171), Node(1201, 171), Node(1201, 771)]
                t = 0
                go = False
                trail = []
                slider.x = 105
                slider.val = 50

            # Save and load
            if pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]:
                if event.type == pg.KEYDOWN and event.key == pg.K_s:
                    save_state()
                elif event.type == pg.KEYDOWN and event.key == pg.K_o:
                    initial = load_state()
                    t = 0
                    go = False
                    slider.x = 105
                    slider.val = 50

        if go:
            t += speed/10000
        if t > 1:
            t = 1
        
        initial = move_nodes(initial, click)
        nodes = calculate_all_nodes(initial, t)

        trail = get_trail(initial, t, speed)

        slider.move()

        draw(t)
    
# Initialize
initial = [Node(601, 771), Node(601, 171), Node(1201, 171), Node(1201, 771)]
slider = Slider(105, 950)
main()