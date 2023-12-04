######################################################################
# Name: Jordan Fasolt-Holmes
# Collaborators (if any):
# List of extensions made (if any): Added messages
######################################################################

"""
This program implements the Breakout game
"""

from pgl import GWindow, GOval, GRect, GLabel
import random
import math

# Constants
GWINDOW_WIDTH = 360                     # Width of the graphics window
GWINDOW_HEIGHT = 600                    # Height of the graphics window
N_ROWS = 10                             # Number of brick rows
N_COLS = 10                             # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1              # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 1             # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3           # Ratio of brick to paddle width
BRICK_SEP = 2                           # Separation between bricks (in pixels)
TOP_FRACTION = 0.1                      # Fraction of window above bricks
BOTTOM_FRACTION = 0.05                  # Fraction of window below paddle
N_BALLS = 3                             # Number of balls (lives) in a game
TIME_STEP = 10                          # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0                # Starting y velocity downwards
MIN_X_VELOCITY = 1.0                    # Minimum random x velocity
MAX_X_VELOCITY = 3.0                    # Maximum random x velocity

# Derived Constants
BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_DIAMETER = BRICK_WIDTH / BRICK_TO_BALL_RATIO

# Function: breakout
def breakout():
    """ The main program for the Breakout game. """
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    """ Creates and colors a grid of bricks. """
    def createGrid(BRICK_WIDTH,BRICK_HEIGHT,N_ROWS,N_COLS,BRICK_SEP,TOP_FRACTION):
        xPos = BRICK_SEP
        gridColors = ["Red","Red", "Orange", "Orange", "Green", "Green", "Cyan", "Cyan", "Blue", "Blue"]
        for x in range(N_COLS):
            gridColorSelector = 0
            yPos = 50 + BRICK_SEP
            for y in range(N_ROWS):
                brick = GRect(xPos,yPos, BRICK_WIDTH,BRICK_HEIGHT)
                brick.set_color(gridColors[gridColorSelector])
                brick.set_filled(True)
                gw.add(brick)
                yPos += BRICK_HEIGHT + BRICK_SEP
                gridColorSelector += 1
                if gridColorSelector == 10:
                    gridColorSelector = 0
            xPos += BRICK_WIDTH + BRICK_SEP
    createGrid(BRICK_WIDTH, BRICK_HEIGHT, N_ROWS, N_COLS, BRICK_SEP, TOP_FRACTION)
    """ Creates the paddle and sets it to the middle of the screen. """
    PADDLE_X = 160
    paddle = GRect(PADDLE_X, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle.set_color("Black")
    paddle.set_fill_color("Gray")
    paddle.set_filled(True)
    gw.add(paddle)
    """ Sets the boundaries and controls the movement of the paddle. """
    def move_action(e):
        paddleCenterX = PADDLE_X - 25
        cursorXLocation = e.get_x() - 25
        paddle.set_location(cursorXLocation, PADDLE_Y)
        if cursorXLocation <= 2:
            paddle.set_location(2, PADDLE_Y)
        if cursorXLocation >= 305:
            paddle.set_location(305, PADDLE_Y)
    """ Creates the ball. """
    ball = GOval(175,300, BALL_DIAMETER,BALL_DIAMETER)
    ball.set_color("Black")
    ball.set_filled(True)
    gw.add(ball)
    """ Sets the velocity for the ball. """
    gw.vx = random.uniform (MIN_X_VELOCITY, MAX_X_VELOCITY)
    if random.uniform (0 ,1) < 0.5:
        gw.vx =- gw.vx
    bx = ball.get_x()
    by = ball.get_y() 
    px = paddle.get_x()
    py = paddle.get_y()
    """ Controls the movement for the ball. """
    def step():
        if gw.ball_is_moving:
            ball.move(gw.vx, gw.dy)
            bx = ball.get_x()
            by = ball.get_y() 
            px = paddle.get_x()
            py = paddle.get_y()
            """ Controls collisions with paddle and bricks. """
            collider = get_colliding_object()
            if collider != None:
                if collider != paddle:
                    gw.dy = -gw.dy
                    gw.remove(collider)
                    gw.NUMBER_BRICKS -= 1
                else:
                    gw.dy = -gw.dy
            """ Controls collisions with walls. """
            if bx < 0 or bx > GWINDOW_WIDTH - BALL_DIAMETER:
                gw.vx = -gw.vx
            if by < 0:
                gw.dy = -gw.dy
            """ Controls various actions when the win/lose counters requirements are met. """
            if by > GWINDOW_HEIGHT - BALL_DIAMETER:
                if gw.loseCounter > 0:
                    gw.ball_is_moving = False
                    gw.remove(ball)
                    gw.add(ball, 175, 300)
                gw.loseCounter -= 1
                if gw.loseCounter <= 0:
                    gw.ball_is_moving = False
                    gw.remove(ball)
                    loseMessage = GLabel("You lose.", 150, 400)
                    gw.add(loseMessage)
            if gw.NUMBER_BRICKS < 1:
                gw.ball_is_moving = False
                gw.remove(ball)
                winMessage = GLabel("You win!", 150, 400)
                gw.add(winMessage) 
    """ Gets the ball rolling. """         
    def click_action(e):
        gw.ball_is_moving = True
    """ Checks the four corners of the balls to check if it collides with anything. """
    def get_colliding_object():
        bx = ball.get_x()
        by = ball.get_y() 
        corner_topLeft = gw.get_element_at(bx, by)
        corner_topRight = gw.get_element_at(bx + BALL_DIAMETER, by)
        corner_lowerRight = gw.get_element_at(bx + BALL_DIAMETER, by + BALL_DIAMETER)
        corner_lowerLeft = gw.get_element_at(bx, by + BALL_DIAMETER)
        if corner_topLeft != None:
            return corner_topLeft
        if corner_topRight != None:
            return corner_topRight
        if corner_lowerLeft != None:
            return corner_lowerLeft
        if corner_lowerRight != None:
            return corner_lowerRight
    """ Defines a counter for number checking if you have lost or won the game. """
    gw.NUMBER_BRICKS = N_ROWS * N_COLS
    gw.loseCounter = 3
    """ Defines Y velocity and sets the ball to a still state. """
    gw.ball_is_moving = False
    gw.dy = INITIAL_Y_VELOCITY
    """ Adds the timer and listens for user actions. """
    gw.add_event_listener("mousemove", move_action)
    gw.add_event_listener("click", click_action)
    gw.set_interval(step, TIME_STEP)
# Startup code
if __name__ == "__main__":
    breakout()
