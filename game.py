from boardgame import Window
from player import player
from player_computer import Computer
import pygame

class GameCaro:
    def __init__(self):
        self.gameboard = Window(10)
        self.player1 = player(0,0, 'O')
        self.player2 = player(0,0, 'X')
        self.computer = Computer()

    def startplay(self):
        run = True
        while run:
            self.gameboard.win.fill((0, 0, 0))
            self.gameboard.draw_text_middle('Press Any Key To Play', 60, (255, 255, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    x = GameCaro()
                    x.run_game()

        pygame.display.quit()

    def run_game(self):
        locked_position = {}
        count_turn_player = 0
        run = True
        grid_check = self.computer.grid_board
        while run:
            self.gameboard.draw_value(locked_position)
            if (count_turn_player % 2 == 0):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        position = event.pos
                        if (self.__check_position(position, locked_position)):
                            # player = self.__turn_player(count_turn_player)
                            i = int((position[1] - self.gameboard.top_left_y) / self.gameboard.block_size)
                            j = int((position[0] - self.gameboard.top_left_x) / self.gameboard.block_size)
                            locked_position[(j, i)] = [self.player1.value, self.player1.color]
                            grid_check[i][j] = 1
                            count_turn_player += 1
                            if (self.__checkwin(locked_position, self.player1.value, j, i)):
                                self.gameboard.draw_value(locked_position)
                                self.gameboard.draw_window()
                                self.gameboard.draw_text_middle(f"Player win !!!", 60, (255, 255, 255))
                                pygame.display.update()
                                pygame.time.delay(10000)
                                run = False
            else:
                self.computer.evalCheckBoard(2, grid_check)
                position = self.computer.findMoveOfCom(1, grid_check)
                j,i= position[1], position[0]

                locked_position[(j,i)] = [self.computer.value, self.computer.color]
                grid_check[i][j] = 2
                count_turn_player += 1
                if (self.__checkwin(locked_position, self.computer.value, j, i)):
                    self.gameboard.draw_value(locked_position)
                    self.gameboard.draw_window()
                    self.gameboard.draw_text_middle(f"Computer win !!!", 60, (255, 255, 255))
                    pygame.display.update()
                    pygame.time.delay(1500)
                    run = False
            pygame.display.update()
            self.gameboard.draw_window()


    def __turn_player(self, count):
        if(count%2==0):
            return self.player1
        else:
            return self.player2

    def __check_position(self, position, locked_position):
        for key in locked_position.keys():
            if( (self.gameboard.top_left_x + key[0]*self.gameboard.block_size < position[0] and
                 self.gameboard.top_left_x + key[0]*self.gameboard.block_size + self.gameboard.block_size > position[0])
                and
                (self.gameboard.top_left_y + key[1] * self.gameboard.block_size < position[1] and
                 self.gameboard.top_left_y + key[1] * self.gameboard.block_size + self.gameboard.block_size > position[1])):
                return False
        return True

    def __checkwin(self, locked_position, player_value, x, y):
        list_position = [key for key, value in locked_position.items() if locked_position[key][0] == player_value]
        count = 1
        # check row
        j, i = x, y
        while((j+1, i) in list_position):
            count += 1
            j+=1
        j = x
        while((j-1, i) in list_position):
            count += 1
            j-=1
        if(count >= 5):
            return True

        # check col
        count = 1
        while ((j, i+1) in list_position):
            count += 1
            i += 1
        i = y
        while ((j, i-1) in list_position):
            count += 1
            i -= 1
        if (count >= 5):
            return True

        # check left diagonal
        count = 1
        while ((j+1, i+1) in list_position):
            count += 1
            i += 1
            j += 1
        j, i = x, y
        while ((j-1, i-1) in list_position):
            count += 1
            i -= 1
            j -= 1
        if (count >= 5):
            return True

        # check right diagonal
        count = 1
        while ((j-1, i+1) in list_position):
            count += 1
            i += 1
            j -= 1
        j, i = x, y
        while ((j+1,i-1) in list_position):
            count += 1
            i -= 1
            j += 1
        if (count >= 5):
            return True

        return False