import pygame
import numpy as np
class Window:
    def __init__(self, shape):
        # GLOBALS VARS
        pygame.font.init()
        self.shape = shape
        self.s_width = 6*self.shape*self.shape
        self.s_height = 6*self.shape*self.shape
        self.play_width = 4*self.shape*self.shape
        self.play_height = 4*self.shape*self.shape
        self.block_size = 4*self.shape
        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = (self.s_height - self.play_height) // 2
        self.grid = [[[] for _ in range(self.shape)] for _ in range(self.shape)]
        self.win = self.__create_window()

    def draw_value(self, locked_positions: dict):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in locked_positions:
                    c = locked_positions[(j, i)]
                    self.grid[i][j] = c
        # return self.grid

    def __create_window(self):
        win = pygame.display.set_mode((self.s_width, self.s_height))
        pygame.display.set_caption('Caro')
        return win

    def __draw_grid(self):
        sx = self.top_left_x
        sy = self.top_left_y

        for i in range(len(self.grid)):
            pygame.draw.line(self.win, (128, 128, 128), (sx, sy + i * self.block_size),
                             (sx + self.play_width, sy + i * self.block_size))
            for j in range(len(self.grid[i])):
                pygame.draw.line(self.win, (128, 128, 128), (sx + j * self.block_size, sy),
                                 (sx + j * self.block_size, sy + self.play_height))

    def draw_window(self):
        self.win.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 6*self.shape)

        label = font.render('Caro', 2, (255, 255, 0))
        self.win.blit(label, (self.top_left_x + self.play_width / 2 - (label.get_width() / 2), 30))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if(self.grid[i][j]):
                    value = font.render(self.grid[i][j][0], 1, self.grid[i][j][1])
                    self.win.blit(value, (self.top_left_x + j*self.block_size + 5,
                                                    self.top_left_y + i*self.block_size + 4))

        pygame.draw.rect(self.win, (255, 0, 0), (self.top_left_x, self.top_left_y, self.play_width, self.play_height), 4)

        self.__draw_grid()

    def draw_text_middle(self, text, size, color):
        font = pygame.font.SysFont('comicsans', size)
        label = font.render(text, 1, color)
        self.win.blit(label, (self.top_left_x + self.play_width / 2 - label.get_width() / 2, self.top_left_y + self.play_height / 2))