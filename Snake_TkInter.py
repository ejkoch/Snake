from enum import Enum
from pynput import keyboard
import tkinter as tk
import random
import threading
import time


width = 400
height = 400

window = tk.Tk()
canvas = tk.Canvas(window, bg="black", height=height, width=width)
canvas.pack(fill=tk.BOTH, expand=1)


# game state enum const
class State(Enum):
    init = -1
    paused = 0
    running = 1
    dead = 2


# snake direction enum const
class Dir(Enum):
    none = 0.5
    left = 0
    up = 1
    right = 2
    down = 3


''' 
gameCounter and counterCapture are used to ensure the
only one button press is registered per game cycle
'''
gameCounter = 0
counterCapture = None
speedMultiplier = 1
'''
it is necessary to know the snake direction to
prevent the snake from turning back into itself
'''
direction = Dir.none.value
gameState = State.init
posX = posY = 9
tileCount = 20
tileSize = 400 / tileCount
foodX = foodY = 15
velX = velY = 0
snakeBody = []
tail = 5


def game_update():
    global gameState, posX, posY, foodX, foodY, tail, gameCounter, counterCapture, height, width
    if gameState == State.init:
        ''' Initial game state displays info popup '''
        #alert("Arrow Keys to move\nSpacebar to pause\n+/- to increase/decrease speed")
        gameState = State.running
    elif gameState == State.paused:
        '''Paused game state has no change, only prints contents in grey - scale '''

    elif gameState == State.running:
        ''' Running state progresses snake position and checks for death / eating '''

        ''' update x and y position of the snake head '''
        posX += velX
        posY += velY

        # printing snake body
        for i in range(len(snakeBody)):
            # checking if snake has run into its body
            if snakeBody[i][0] == posX and snakeBody[i][1] == posY and len(snakeBody) > 5:
                gameState = State.dead
                game_update()

        # checking if snake has run into the wall
        if posX < 0 or posX > tileCount-1 or posY < 0 or posY > tileCount-1:
            gameState = State.dead
            game_update()

        # updating snake body array
        snakeBody.append((posX, posY))
        while len(snakeBody) > tail:
            snakeBody.pop(0)

        # checking if snake head is on the food(eating)
        if foodX == posX and foodY == posY:
            tail = tail + 1

            # generating new food
            food_x_temp = int(random.random() * tileCount)
            food_y_temp = int(random.random() * tileCount)

            # ensuring the new food is not placed on the snake body
            contains = False
            for element in snakeBody:
                if element[0] == food_x_temp and element[1] == food_y_temp:
                    contains = True
                    break

            while contains:
                contains = False
                food_x_temp = int(random.random() * tileCount)
                food_y_temp = int(random.random() * tileCount)
                for element in snakeBody:
                    if element[0] == food_x_temp and element[1] == food_y_temp:
                        contains = True
                        break

            foodX = food_x_temp
            foodY = food_y_temp

    # incrementing the gameCounter every game cycle
    gameCounter += 1
    print("gameCounter: " + str(gameCounter))


def display_update():
    global gameState, posX, posY, foodX, foodY, tail, gameCounter, counterCapture, height, width
    if gameState == State.init:
        ''' Initial game state displays info popup '''
        #alert("Arrow Keys to move\nSpacebar to pause\n+/- to increase/decrease speed")
        gameState = State.running
    elif gameState == State.paused:
        '''Paused game state has no change, only prints contents in grey - scale '''
        canvas.delete("all")
        canvas.create_rectangle(0, 0, height, width, fill='grey')

        for i in range(len(snakeBody)):
            rectangle(snakeBody[i][0], snakeBody[i][1], 'black')

        rectangle(foodX, foodY, 'white')

    elif gameState == State.running:
        ''' Running state progresses snake position and checks for death / eating '''
        canvas.delete("all")

        # printing snake body
        for i in range(len(snakeBody)):
            rectangle(snakeBody[i][0], snakeBody[i][1], 'white')

        rectangle(posX, posY, 'white')

        # checking if snake has run into the wall
        '''if posX < 0 or posX > tileCount-1 or posY < 0 or posY > tileCount-1:
            gameState = State.dead
            display_update()'''

        rectangle(foodX, foodY, 'red')

    elif gameState == State.dead:
        # Dead state freezes game and colors snake red
        for i in range(len(snakeBody)):
            rectangle(snakeBody[i][0], snakeBody[i][1], 'red')


def on_press(key):
    global gameState, direction, posX, posY, foodX, foodY, velX, velY, snakeBody, tail, counterCapture, speedMultiplier
    print(key)
    if str(key) == "Key.space":  # space bar
        if gameState == State.paused:
            # run the game if state is paused
            gameState = State.running
        elif gameState == State.running:
            # pause the game if state is running
            gameState = State.paused
        elif gameState == State.dead:
            # restart the game if state is dead
            direction = Dir.none.value
            gameState = State.running
            posX = posY = 10
            foodX = foodY = 15
            velX = velY = 0
            snakeBody = []
            tail = 5
    elif str(key) == "Key.left":  # left arrow key
        if gameCounter != counterCapture and direction % 2 != 0 and gameState == State.running:
            velX = -1
            velY = 0
            direction = Dir.left.value
            counterCapture = gameCounter
    elif str(key) == "Key.up":  # up arrow key
        if gameCounter != counterCapture and direction % 2 != 1 and gameState == State.running:
            velX = 0
            velY = -1
            direction = Dir.up.value
            counterCapture = gameCounter
    elif str(key) == "Key.right":  # right arrow key
        if gameCounter != counterCapture and direction % 2 != 0 and gameState == State.running:
            velX = 1
            velY = 0
            direction = Dir.right.value
            counterCapture = gameCounter
    elif str(key) == "Key.down":  # down arrow key
        if gameCounter != counterCapture and direction % 2 != 1 and gameState == State.running:
            velX = 0
            velY = 1
            direction = Dir.down.value
            counterCapture = gameCounter
    elif str(key) == "+" or str(key) == "=":  # + key
        #clearInterval(intervalID)
        speedMultiplier *= 1.5
        #intervalID = setInterval(game, 1000 / (speedMultiplier * 10))
    elif str(key) == "-":  # - key
        #clearInterval(intervalID)
        speedMultiplier *= 1.5
        #intervalID = setInterval(game, 1000 / (speedMultiplier * 10))


def rectangle(x, y, color):
    global canvas
    sqr = canvas.create_rectangle(int(x * tileSize), int(y * tileSize),
                                  int((x + 1) * tileSize), int((y + 1) * tileSize),
                                  fill=color)


def set_interval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()


def game_thread():
    while True:
        game_update()
        time.sleep(0.1)


def display_thread():
    global canvas
    while True:
        display_update()
        canvas.update()


def main():
    global window, canvas

    t1 = threading.Thread(target=game_thread)
    #t2 = threading.Thread(target=display_thread)
    t1.start()
    #t2.start()

    while True:
        display_update()
        canvas.update()

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

main()
