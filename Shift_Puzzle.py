'''
Author: Andy Sollish
Date: December 7, 2016
Platform: Python 2.7 / Pygame for 64-bit OS / Windows 10
Description: Simple shift puzzle.  User can select from one of two difficulties. Stores record of 10 fastest
            completion times.
'''

### ------------------------------------ LOAD MODULES ------------------------------------------- ###

try:
    import pygame
    import sys
    import random
    import square
    import time
    from pygame.locals import *
    from piece import *
    from Tkinter import *
    from shift_gui import *



except ImportError, err:
    print "Unable to import module. " + '%s' % (err)



### ----------------------------------- RESOURCE HANDLING ---------------------------------------- ###

def loadImages():
    # This function will eventually randomly grab an image from directory
    image = pygame.image.load('Cat_closeup.jpg')
    return image

def loadSounds():
    # This is not used.  It's an idea for future development.
    sound = pygame.mixer.Sound('Cat_meow.mp3')
    return sound


### ----------------------------------------- CLASSES --------------------------------------------- ###


class board(object):

    # --------------- Constructor ------------------- #

    def __init__(self, r, c, w, h):

        self.tile_width, self.tile_height = w, h
        self.columns, self.rows = c, r
        self.blank_tile = (c - 1, r - 1)
        (self.emptyc, self.emptyr) = self.blank_tile

        self.state = self.draw(self.columns, self.rows)
        self.state_original = self.draw(c, r)

    # ----------------- Public Methods -------------- #

    def draw(self, columns, rows):
        return {(col, row): (col, row) for col in range(columns) for row in range(rows)}


    def swap(self, c, r):
        display.blit(tiles[self.state[(c, r)]], (self.emptyc * self.tile_width, self.emptyr * self.tile_height))
        display.blit(tiles[self.blank_tile], (c * self.tile_width, r * self.tile_height))
        self.state[(self.emptyc, self.emptyr)] = self.state[(c, r)]
        self.state[(c, r)] = self.blank_tile
        (self.emptyc, self.emptyr) = (c, r)
        pygame.display.flip()


    def shift(self):
        # keep track of last shuffling direction to avoid "undo" shuffle moves

        last_r = 0
        for i in range(75):
            # slow down shuffling for visual effect
            pygame.time.delay(50)
            while True:
                # pick a random direction and make a shuffling move
                # if that is possible in that direction
                r = random.randint(1, 4)
                if (last_r + r == 5):
                    # don't undo the last shuffling move
                    continue
                if r == 1 and (self.emptyc > 0):
                    self.swap(self.emptyc - 1, self.emptyr)  # shift left
                elif r == 4 and (self.emptyc < self.columns - 1):
                    self.swap(self.emptyc + 1, self.emptyr)  # shift right
                elif r == 2 and (self.emptyr > 0):
                    self.swap(self.emptyc, self.emptyr - 1)  # shift up
                elif r == 3 and (self.emptyr < self.rows - 1):
                    self.swap(self.emptyc, self.emptyr + 1)  # shift down
                else:
                    # the random shuffle move didn't fit in that direction
                    continue
                last_r = r
                break  # a shuffling move was made


### ----------------------------------- MENU FUNCTIONS ------------------------------------------ ###

def text_objects(text, font, color):
    # create text inside buttons

    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()



def win_button(msg, x, y, w, h, action=None):
    # message, (x,y) coordinates, width, height, active color, inactive color, action

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    small = pygame.font.Font('freesansbold.ttf', 15)

    if (x + w > mouse[0] > x) and (y + h > mouse[1] > y):
        pygame.draw.rect(display, grey, (x, y, w, h))
        if click[0] == 1 and action != None:  # user pressed left mouse
            if action == "Play Again":
                main(board1)
            elif action == "Quit":
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(display, white, (x, y, w, h))

    # --------------------- button text --------------------------- #

    textSurf, textRect = text_objects(msg, small, black)
    textRect.center = ((x + 50), (y + 20))
    display.blit(textSurf, textRect)



def start_menu():
    # first surface the user sees

    # create the start menu.  User chooses easy or hard, which returns variables (rows, columns...etc.)

    pygame.init()
    size = (800, 600)
    display = pygame.display.set_mode(size)
    pygame.display.set_caption("Funny Cats Shift Puzzle")

    # ------------------- Event Loop ----------------------- #

    intro = True
    while intro:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                    (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
                intro = False
                pygame.quit()
                sys.exit()

            # ---------------------- Menu Title ------------------- #

            display.fill(black)
            title_text = pygame.font.Font('freesansbold.ttf', 50)
            TextSurf, TextRect = text_objects('Funny Cats Shift Puzzle', title_text, white)
            TextRect.center = ((400, 150))
            display.blit(TextSurf, TextRect)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            small = pygame.font.Font('freesansbold.ttf', 20)

            # ------------------- Easy Button ---------------------- #

            if (342 + 100 > mouse[0] > 342) and (295 + 40 > mouse[1] > 295):
                pygame.draw.rect(display, grey, (342, 295, 100, 40))
                if click[0] == 1:  # user pressed left mouse
                    return 3, 4, 200, 200 # return rows, columns, tile_width, tile_height
            else:
                pygame.draw.rect(display, white, (342, 295, 100, 40))

            # ------------------ Hard Button ----------------------- #

            if (342 + 100 > mouse[0] > 342) and (375 + 40 > mouse[1] > 375):
                pygame.draw.rect(display, grey, (342, 375, 100, 40))
                if click[0] == 1:  # user pressed left mouse
                    return 6, 8, 100, 100 # return rows, columns, tile_width, tile_height
            else:
                pygame.draw.rect(display, white, (342, 375, 100, 40))

            # ------------------ button text ---------------------- #

            textSurf, textRect = text_objects("Easy", small, black)
            textRect.center = ((342 + 50), (295 + 20))
            display.blit(textSurf, textRect)

            textSurf, textRect = text_objects("Hard", small, black)
            textRect.center = ((342 + 50), (375 + 20))
            display.blit(textSurf, textRect)

        pygame.display.update()


def you_win():
    # The final surface after the game is complete

    # create the end menu.  User chooses play again or quit.

    pygame.init()
    size = (800, 600)
    display = pygame.display.set_mode(size)
    pygame.display.set_caption("Funny Cats Shift Puzzle")

    # --------------------------- Event Loop ---------------------------- #
    end = True
    while end:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                    (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
                end = False
                pygame.quit()
                sys.exit()

            # --------------- End Title ------------------------------- #

            display.fill(black)
            title_text = pygame.font.Font('freesansbold.ttf', 50)
            TextSurf, TextRect = text_objects('Congratulations, You Got It!', title_text, white)
            TextRect.center = ((400, 150))
            display.blit(TextSurf, TextRect)

            # ---------------  Play Again / Quit Buttons --------------- #

            win_button("Play Again", 342, 295, 100, 40, action="Play Again")
            win_button("Quit", 342, 375, 100, 40, action="Quit")

        pygame.display.update()



### ---------------------------------- MAIN LOOP (INPUT HANDLING) ------------------------------------- ###

def main(board):
    # --------------- Start Game Clock ------------------ #
    # starts the game clock after user selects difficulty
    tStart = time.time()


    # -------------- Event Loop --------------------------- #

    start = True
    running = True
    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                    (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start == True:
                    board.shift()
                    start = False


                if event.dict['button'] == 1:
                # mouse left button: move if next to the empty tile
                    mouse_pos = pygame.mouse.get_pos() # creates an (X, Y) pixel position
                    c = mouse_pos[0] / board.tile_width # first digit in mouse_pos is X
                    r = mouse_pos[1] / board.tile_height # second digit in mouse_pos is Y

                    if ((abs(c - board.emptyc) == 1 and r == board.emptyr) or
                            (abs(r - board.emptyr) == 1 and c == board.emptyc)):
                        board.swap(c, r)

                        if board.state == board.state_original:

                            # ------------------- End Game Clock ---------------- #
                            # stop the game clock when puzzle is complete
                            tEnd = time.time()
                            totTime = tStart - tEnd

                            # Start GUI to get username for high scores
                            root = Tk()
                            root.title("High Score Entry")
                            root.geometry("350x150")
                            win = my_gui(root, totTime)
                            root.mainloop()

                            # Final Pygame screen
                            you_win()


### ------------------------- PROGRAM START ----------------------------------- #

if __name__ == '__main__':
    # Create the start menu
    rows, columns, tile_width, tile_height = start_menu()

    # Load puzzle image
    image = loadImages()

    # Create the tile objects
    tile1 = piece(image, rows, columns, tile_width, tile_height)
    tiles = tile1.tile_creator()

    # Initialize the puzzle display
    pygame.init()
    size = (800, 600)
    display = pygame.display.set_mode(size)
    pygame.display.set_caption("Funny Cats Shift Puzzle")
    display.blit(image, (0, 0))
    pygame.display.flip()

    # Create the board object
    board1 = board(rows, columns, tile_width, tile_height)

    # Start the event loop
    main(board1)
