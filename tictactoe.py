import sys
import pygame
from constans import *
import numpy as np

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE AI")
screen.fill(BG_COLOR)

class Board: 

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqr = self.squares #[squares]
        self.mark_sqr = 0

    def final_state(self):
        """
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        """

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]  
            
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[2][0] != 0:
            self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.mark_sqr += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs
    
    def isfull(self):
        return self.mark_sqr == 9
    
    def isempty(self):
        return self.mark_sqr == 0

class Game: 

    def __init__(self):
        self.board = Board()
        # self.ai = AI()
        self.player = 1 # 1-cross #2-circles
        self.gamemode = 'pvp' # or ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross in this case
            #cross will be shown as desc and asc line

            #desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET )
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)

            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            #asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET )
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE +  OFFSET)

            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #draw circle in this case
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
    
    def next_turn(self):
        self.player = self.player % 2 + 1

def main():

    game = Game()
    board = game.board

    # This is mainloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()

                    # print(board.squares)
        
        pygame.display.update()

main()