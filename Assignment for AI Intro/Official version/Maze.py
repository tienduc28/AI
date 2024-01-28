import turtle
import time
import sys
from collections import deque
import PySimpleGUI as sg

global input_grid
global start_x, start_y, end_x, end_y

# Set up the maze with PySimpleGUI
def method_setup():
    layout = [[sg.Text('Select how you want to create the maze: ')],
              [sg.Button('Import File'), sg.Button('Use GUI')]
              ]
    window = sg.Window('Welcome', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Use GUI':
            window.close()
            create_maze_with_GUI()
        elif event == 'Import File':
            import_layout = [[sg.Text('Choose file to import:')],
                             [sg.Input(), sg.FileBrowse()],
                             [sg.OK()]
                             ]
            window1 = sg.Window('Import File', import_layout)
            event1, values1 = window1.read()
            if event1 == 'OK':
                global input_grid
                filename = values1[0]
                with open(filename, 'r') as f:
                    input_grid = []
                    for line in f:
                        row = line.strip()
                        input_grid.append(row)
            window1.close()
            window.close()


def create_maze_with_GUI():
    layout = [[sg.Text('Number of rows:'), sg.Input(size=(5, 1), key='-ROWS-')],
              [sg.Text('Number of columns:'), sg.Input(size=(5, 1), key='-COLS-')],
              [sg.Button('Submit')]]

    window = sg.Window('Maze Setup', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Submit':
            if int(values['-ROWS-']) <= 0 or int(values['-COLS-']) <= 0:
                layout1 = [[sg.Text('Invalid size!')],
                            [sg.Button('OK')]
                            ]
                window1 = sg.Window('Warning', layout1)
                event1, values1 = window1.read()
                if event1 == 'OK':
                    window1.close()
            else:
                break

    window.close()

    m = int(values['-ROWS-'])
    n = int(values['-COLS-'])

    layout = [[sg.Button('', size=(2, 1), key=(i, j), pad=(0, 0), button_color=('white', 'white')) for j in range(n)] for i in range(m)]
    layout.append([sg.Button('Set Start'), sg.Button('Set End'), sg.Button('Set Wall')])
    layout.append([sg.Button('Submit')])

    window = sg.Window('Maze Setup', layout)

    start_set = False
    end_set = False
    wall_set = True
    start = end = None

    start_existed = 0
    end_existed = 0

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if type(event) == tuple:
            button = window[event]
            if wall_set:
                if button.ButtonColor[1] == 'white':
                    button.update(button_color=('white', 'black'))
                elif button.ButtonColor[1] == 'black':
                    button.update(button_color=('white', 'white'))
            elif start_set:
                if start:
                    start.update(button_color=('white', 'white'))
                button.update(button_color=('white', 'red'))
                start = button
            elif end_set:
                if end:
                    end.update(button_color=('white', 'white'))
                button.update(button_color=('white', 'purple'))
                end = button
        elif event == 'Set Start':
            start_set = True
            end_set = False
            wall_set = False
        elif event == 'Set End':
            end_set = True
            start_set = False
            wall_set = False
        elif event == 'Set Wall':
            wall_set = True
            start_set = False
            end_set = False
        elif event == 'Submit':
            global input_grid
            input_grid = []
            tmp = "+" * (n + 2)
            input_grid.append(tmp)
            for i in range(m):
                row = '+'
                for j in range(n):
                    button = window[(i, j)]
                    if button.ButtonColor[1] == 'black':
                        row += '+'
                    elif button.ButtonColor[1] == 'white':
                        row += ' '
                    elif button.ButtonColor[1] == 'red':
                        row += 's'
                        start_existed = 1
                    elif button.ButtonColor[1] == 'purple':
                        row += 'e'
                        end_existed = 1
                row += '+'
                input_grid.append(row)
            input_grid.append(tmp)

            if start_existed == 0:
                layout1 = [[sg.Text('The start point hasn\'t been set!')],
                            [sg.Button('OK')]
                            ]
                window1 = sg.Window('Warning', layout1)
                event1, values1 = window1.read()
                if event1 == 'OK':
                    window1.close()

            if end_existed == 0:
                layout1 = [[sg.Text('The end point hasn\'t been set!')],
                            [sg.Button('OK')]
                            ]
                window1 = sg.Window('Warning', layout1)
                event1, values1 = window1.read()
                if event1 == 'OK':
                    window1.close()
            if start_existed == 1 and end_existed == 1:
                break

    window.close()


def select_algorithm():
    layout = [[sg.Text('Choose the algorithm you want to solve this maze with:')],
              [sg.Button('BFS'), sg.Button('DFS'), sg.Button('A*')]
              ]

    window = sg.Window('Select Algorithm', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'BFS':
            window.close()
            bfs(start_x, start_y)
        elif event == 'DFS':
            window.close()
            dfs(start_x, start_y)
        elif event == 'A*':
            window.close()
            aStar(start_x, start_y)


def unsolvable():
    unreachable = [[sg.Text('No path can be found')]]
    window = sg.Window('Warning', unreachable)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            sys.exit()
        window.close()

# Maze by Turtle
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Solving Program")
wn.setup(10, 10)

# Hàm đóng chương trình
def on_close():
    sys.exit()
canvas = turtle.getcanvas()
root = canvas.winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", on_close)

class Maze(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Green(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)


class Blue(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)


# this is the class for the yellow or turtle
class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)


class Yellow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed(0)


class Black(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)


def update_window_size(grid):
    base_cell_size = 24
    num_rows = len(grid)
    num_cols = len(grid[0])

    window_width = num_cols * base_cell_size
    window_height = num_rows * base_cell_size

    wn.setup(width=window_width + 50, height=window_height + 50)


def setup_maze(grid):
    update_window_size(input_grid)
    maze_width = len(grid[0]) * 24
    maze_height = len(grid) * 24

    screen_x_start = -maze_width / 2
    screen_y_start = maze_height / 2

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            character = grid[y][x]

            screen_x = (x * 24) + screen_x_start
            screen_y = screen_y_start - (y * 24)

            maze.goto(screen_x, screen_y)

            if character == "+":
                maze.stamp()
                walls.append((screen_x, screen_y))

            elif character == " " or character == "e":
                path.append((screen_x, screen_y))

            if character == "e":
                green.color("purple")
                green.goto(screen_x, screen_y)
                green.stamp()
                green.color("green")
                global end_x, end_y
                end_x, end_y = screen_x, screen_y

            if character == "s":
                global start_x, start_y
                start_x, start_y = screen_x, screen_y
                red.goto(screen_x, screen_y)
                red.stamp()


def end_program(x, y):
    wn.bye()  
    sys.exit()

def bfs(x, y):
    frontier.append((x, y))
    solution[x, y] = x, y

    while len(frontier) > 0:
        time.sleep(0.1)
        x, y = frontier.popleft()

        if (end_x, end_y) in visited:
            break
        if (x - 24, y) in path and (x - 24, y) not in visited:
            cell = (x - 24, y)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x - 24, y))

        if (x, y - 24) in path and (x, y - 24) not in visited:
            cell = (x, y - 24)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x, y - 24))
            # print(solution)

        if (x + 24, y) in path and (x + 24, y) not in visited:
            cell = (x + 24, y)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x + 24, y))

        if (x, y + 24) in path and (x, y + 24) not in visited:
            cell = (x, y + 24)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x, y + 24))
        green.goto(x, y)
        green.stamp()
    if (end_x, end_y) not in visited:
        unsolvable()


def dfs(x, y):
    frontier.append((x, y))
    solution[x, y] = x, y

    while len(frontier) > 0:
        time.sleep(0.1)
        x, y = frontier.pop()

        if (end_x, end_y) in visited:
            break
        if (x - 24, y) in path and (x - 24, y) not in visited:
            cell = (x - 24, y)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x - 24, y))

        if (x, y - 24) in path and (x, y - 24) not in visited:
            cell = (x, y - 24)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x, y - 24))
            # print(solution)

        if (x + 24, y) in path and (x + 24, y) not in visited:
            cell = (x + 24, y)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x + 24, y))

        if (x, y + 24) in path and (x, y + 24) not in visited:
            cell = (x, y + 24)
            solution[cell] = x, y
            blue.goto(cell)
            blue.stamp()
            frontier.append(cell)
            visited.add((x, y + 24))
        green.goto(x, y)
        green.stamp()
    if (end_x, end_y) not in visited:
        unsolvable()


def heuristic(x, y):
    return abs(x - end_x) * abs(x - end_x) + abs(y - end_y) * abs(y - end_y)


def aStar(x, y):
    open_set = set()
    closed_set = set()
    came_from = {}

    g_score = {(x, y): 0}
    h_score = {(x, y): heuristic(x, y)}
    f_score = {(x, y): h_score[(x, y)]}

    solution[x, y] = x, y
    open_set.add((x, y))

    while open_set:
        time.sleep(0.1)
        (a, b) = min(open_set, key=lambda node: f_score[node])

        if (a, b) == (end_x, end_y):
            break

        open_set.remove((a, b))
        closed_set.add((a, b))

        for (next_x, next_y) in [(a + 24, b), (a - 24, b), (a, b + 24), (a, b - 24)]:
            if (next_x, next_y) in path:
                if (next_x, next_y) in closed_set:
                    continue

                tentative_g_score = g_score[(a, b)] + 24

                if (next_x, next_y) not in open_set or tentative_g_score < g_score[(next_x, next_y)]:
                    came_from[(next_x, next_y)] = (a, b)
                    g_score[(next_x, next_y)] = tentative_g_score
                    h_score[(next_x, next_y)] = heuristic(next_x, next_y)
                    f_score[(next_x, next_y)] = g_score[(next_x, next_y)] + h_score[(next_x, next_y)]

                    solution[(next_x, next_y)] = a, b

                    if (next_x, next_y) not in open_set:
                        open_set.add((next_x, next_y))
                    blue.goto((next_x, next_y))
                    blue.stamp()

        green.goto(a, b)
        green.stamp()

    if (end_x, end_y) not in solution:
        unsolvable()


def back_route(x, y):
    yellow.goto(x, y)
    yellow.stamp()
    while (x, y) != (start_x, start_y):
        yellow.goto(solution[x, y])
        yellow.stamp()
        x, y = solution[x, y]


# set up classes
maze = Maze()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()
black = Black()

# setup lists
walls = []
path = []
visited = set()
frontier = deque()
solution = {}

# main program
method_setup()
setup_maze(input_grid)
select_algorithm()
back_route(end_x, end_y)
turtle.mainloop()
turtle.onscreenclick(sys.exit())
