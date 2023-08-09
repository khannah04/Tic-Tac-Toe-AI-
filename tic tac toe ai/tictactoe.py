import sys
import random
import copy
import pygame
from constants import *
import numpy as np

#PYGAME
pygame.init() #initialize the pygame model

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')

screen.fill(BG_COLOR)

class AI: 
    def __init__(self, lvl = 1, player = 2) -> None:
        self.level = lvl
        self.player = player
    
    def random_choice(self, board): 
        empty_squares = board.get_empty_squares()
        rand_index = random.randrange(0, len(empty_squares))
        return empty_squares[rand_index]

    def minimax(self, board, maximizing): 
        #terminal cases 
        case = board.final_state()
        if case == 1: 
            return 1, None

        if case == 2:
            return -1, None
 
        elif board.is_full(): 
            return 0, None

        if maximizing: 
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for(row, col) in empty_squares: 
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval: 
                    max_eval = eval
                    best_move = (row, col)
                
            
            return max_eval, best_move


        elif not maximizing: 
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()
 
            for (row, col) in empty_squares: 
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval: 
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def evaluate(self, board): 
        if self.level == 0: 
            eval = 'random'
            move = self.random_choice(board)
        else: 
            eval, move = self.minimax(board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')
        return move

class Board: 
    def __init__(self) -> None:
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares #at the beginning, the whole board is empty squares
        self.marked_squares = 0 #number of marked squares

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares+=1
    
    def final_state(self, show = False): 
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 is player 2 wins

        '''

        #we need to check each type of win
        #let's start with vertical wins
        for col in range(COLS): 
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0: 
                if show: 
                    color = CIRCLE_COLOR
                    iPos = (col * SQSIZE + SQSIZE//2, 20)
                    fPos = (col * SQSIZE + SQSIZE//2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
        
        #now horiziontal
        for row in range(ROWS): 
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0: 
                if show: 
                    color = CIRCLE_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE//2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE//2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        #now diagonal

        #desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show: 
                    color = CIRCLE_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH - 20, HEIGHT-20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        #asc diagonal 
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0: 
            if show: 
                    color = CIRCLE_COLOR
                    iPos = (20, HEIGHT-20)
                    fPos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        #no win yet
        return 0
        

    def empty_square(self, row, col): 
        return self.squares[row][col] == 0

    def is_full(self): 
        return self.marked_squares == 9

    def is_empty(self): 
        return self.marked_squares == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS): 
            for col in range(COLS): 
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        
        return empty_squares

            
class Game: 
    def __init__(self) -> None:
        self.board =  Board()
        self.ai = AI()
        self.player = 1 #starting player
        self.gamemode = 'ai' #pvp or ai
        self.game_running = True
        self.display_board_lines()

    def make_move(self, row, col): 
        self.board.mark_square(row, col, self.player)
        self.draw_char(row, col)
        self.turn()

    def display_board_lines(self): 
        #vertical lines 
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE*2, 0), (SQSIZE*2, HEIGHT), LINE_WIDTH)

        #horiziontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE*2), (WIDTH, SQSIZE*2), LINE_WIDTH)
    
    def draw_char(self, row, col): 
        if self.player == 1: 
            start_desc = (col*SQSIZE + OFFSET, row*SQSIZE + OFFSET)
            end_desc = (col*SQSIZE + SQSIZE - OFFSET, row*SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CIRCLE_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col*SQSIZE + OFFSET, row*SQSIZE + SQSIZE - OFFSET)
            end_asc = (col*SQSIZE + SQSIZE - OFFSET, row*SQSIZE + OFFSET)
            pygame.draw.line(screen, CIRCLE_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2: 
            center = (col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRC_WIDTH)

    def turn(self):
        self.player = self.player%2+1

    def change_gamemode(self): 
        if self.gamemode == 'pvp': 
            self.gamemode = 'ai'
        else: 
            self.gamemode = 'pvp'

    def reset(self): 
        self.__init__()

    def isover(self): 
        return self.board.final_state(show = True) != 0 or self.board.is_full()

    

        
        
def main(): 

    #game object creation
    game = Game()
    ai = game.ai
    board = game.board

    while True: 
        for event in pygame.event.get(): 

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1]//SQSIZE
                col = pos[0]//SQSIZE

                if board.empty_square(row, col) and game.game_running: 
                    game.make_move(row, col)

                    if game.isover():
                        game.game_running = False

            if event.type == pygame.KEYDOWN: 
                #g changes game mode
                if event.key == pygame.K_g: 
                    game.change_gamemode()
                    
                if event.key == pygame.K_r: 
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_0: 
                    ai.level = 0
                
                if event.key == pygame.K_1: 
                    ai.level = 1

        if game.gamemode == 'ai' and game.player == ai.player and game.game_running:
            #update the screen
            pygame.display.update()
            #ai methods
            row, col = ai.evaluate(board)
            game.make_move(row, col)

            if game.isover():  
                game.game_running = False

        pygame.display.update()

main()