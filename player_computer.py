import random

MAX_VALUE = 1000000000
maxMove = 1
depth_MAX = 100
class Computer:
    def __init__(self):
        self.shape = 10
        self.grid_board = [[0 for _ in range(self.shape)] for _ in range(self.shape)]
        self.grid_value = [[0 for _ in range(self.shape)] for _ in range(self.shape)]
        self.case_human = ["11", "101", "1112", "2111", "1011", "1101", "111", "11011", "10111", "11101", "11112", "21111", "1111", "11111"]
        self.case_com = ["22", "202", "2221", "1222", "2022", "2202", "222", "22022", "20222", "22202", "22221", "12222", "2222", "22222"]
        self.point_grid = [5, 5, 10, 10, 500, 500, 500, 600, 600, 600, 600, 600, 5000, 5000]
        self.aScore = [0,1,2,9,81,729]
        self.dScore = [0,2,18,162,1458]
        self.value = 'X'
        self.color = (255, 0, 0)

    def findMoveOfCom(self, player, grid_board):
        maxp = -MAX_VALUE
        copy_grid_board = grid_board.copy()
        self.evalCheckBoard(2, copy_grid_board)
        list_MaxPoint = []
        for Maxpoint in range(maxMove):
            list_MaxPoint.append(self.getMaxPoint())
        list_choice = []
        for maxPoint in list_MaxPoint:
            copy_grid_board[maxPoint[0]][maxPoint[1]] = player
            temp = self.minVal(copy_grid_board, -MAX_VALUE, MAX_VALUE, 0)
            if(temp>maxp):
                maxp=temp
                list_choice = []
                list_choice.append(maxPoint)
            elif(temp==maxp):
                list_choice.append(maxPoint)
            copy_grid_board[maxPoint[0]][maxPoint[1]] = 0
        return random.choice(list_choice)


    def minVal(self, grid_board, alpha, belta, depth):
        val = self.evalDanger(grid_board)
        # print(f'minVal: {val}')
        if(depth >= depth_MAX or abs(val) > 5000):
            return val
        self.evalCheckBoard(1, grid_board)
        list_MaxPoint = []
        for Maxpoint in range(maxMove):
            list_MaxPoint.append(self.getMaxPoint())
        for maxPoint in list_MaxPoint:
            grid_board[maxPoint[0]][maxPoint[1]] = 1
            belta = min(belta, self.maxVal(grid_board, alpha, belta, depth+1))
            grid_board[maxPoint[0]][maxPoint[1]] = 0
            if(alpha >= belta):
                break
        return belta

    def maxVal(self, grid_board, alpha, belta, depth):
        val = self.evalDanger(grid_board)
        # print(f'maxVal: {val}')
        if (depth >= depth_MAX or abs(val) > 5000):
            return val
        self.evalCheckBoard(2, grid_board)
        list_MaxPoint = []
        for Maxpoint in range(maxMove):
            list_MaxPoint.append(self.getMaxPoint())
        for maxPoint in list_MaxPoint:
            grid_board[maxPoint[0]][maxPoint[1]] = 2
            alpha = max(alpha, self.minVal(grid_board, alpha, belta, depth + 1))
            grid_board[maxPoint[0]][maxPoint[1]] = 0
            if (alpha >= belta):
                break
        return alpha

    def evalDanger(self, grid_board):
        l = len(grid_board)
        s = ''
        for i in range(l):
            for j in range(l):
                s += str(grid_board[i][j])
            s += ';'
            for j in range(l):
                s += str(grid_board[j][i])
            s += ';'
        for i in range(l-4):
            for j in range(l-i):
                s += str(grid_board[j][i+j])
            s += ';'
        for i in range(l-5, 0, -1):
            for j in range(l-i):
                s += str(grid_board[j+i][j])
            s += ';'
        for i in range(4, l):
            for j in range(i+1):
                s += str(grid_board[i-j][j])
            s += ';'
        for i in range(l-5, 0, -1):
            for j in range(l-1, i-1, -1):
                s += str(grid_board[j][i+l-j-1])
            s += ';'
        score = 0
        for i in range(len(self.case_human)):
            count1 = s.count(self.case_human[i])
            count2 = s.count(self.case_com[i])
            score += self.point_grid[i]*count2
            score -= self.point_grid[i]*count1
        return score

    def getMaxPoint(self):
        list_MaxPoint = []
        temp = -MAX_VALUE
        for row in range(len(self.grid_value)):
            for col in range(len(self.grid_value[row])):
                if(temp<self.grid_value[row][col]):
                    list_MaxPoint = []
                    temp = self.grid_value[row][col]
                    list_MaxPoint.append([row, col])
                elif(temp==self.grid_value[row][col]):
                    list_MaxPoint.append([row, col])

        for maxPoint in list_MaxPoint:
            self.grid_value[maxPoint[0]][maxPoint[1]] = 0

        Maxpoint = random.choice(list_MaxPoint)
        return Maxpoint




    def evalCheckBoard(self, player, grid_board):
        self.grid_value = [[0 for _ in range(self.shape)] for _ in range(self.shape)]
        # Check Row
        for row in range(len(self.grid_value)):
            for col in range(len(self.grid_value[row])-4):
                eval_pc = 0
                eval_human = 0
                for i in range(5):
                    if(grid_board[row][col+i]==2):
                        eval_pc += 1
                    if(grid_board[row][col+i]==1):
                        eval_human += 1
                if(eval_pc*eval_human==0 and eval_pc != eval_human):
                    for i in range(5):
                        if(grid_board[row][col+i]==0):
                            if(eval_human == 0):
                                if(player == 1):
                                    self.grid_value[row][col+i] += self.dScore[eval_pc]
                                else:
                                    self.grid_value[row][col + i] += self.aScore[eval_pc]
                            if (eval_pc == 0):
                                if (player == 2):
                                    self.grid_value[row][col + i] += self.dScore[eval_human]
                                else:
                                    self.grid_value[row][col + i] += self.aScore[eval_human]

                            if(eval_pc==4 or eval_human==4):
                                self.grid_value[row][col + i] *= 2

        # Check Col
        for col in range(len(self.grid_value)):
            for row in range(len(self.grid_value[col])-4):
                eval_pc = 0
                eval_human = 0
                for i in range(5):
                    if(grid_board[row+i][col]==2):
                        eval_pc += 1
                    if(grid_board[row+i][col]==1):
                        eval_human += 1
                if(eval_pc*eval_human==0 and eval_pc != eval_human):
                    for i in range(5):
                        if(grid_board[row+i][col]==0):
                            if(eval_human == 0):
                                if(player==1):
                                    self.grid_value[row+i][col] += self.dScore[eval_pc]
                                else:
                                    self.grid_value[row+i][col] += self.aScore[eval_pc]
                            if (eval_pc == 0):
                                if (player == 2):
                                    self.grid_value[row+i][col] += self.dScore[eval_human]
                                else:
                                    self.grid_value[row+i][col] += self.aScore[eval_human]

                            if(eval_pc==4 or eval_human==4):
                                self.grid_value[row+i][col] *= 2

        # check left diagonal
        for col in range(len(self.grid_value)-4):
            for row in range(len(self.grid_value[col])-4):
                eval_pc = 0
                eval_human = 0
                for i in range(5):
                    if(grid_board[row+i][col+i]==2):
                        eval_pc += 1
                    if(grid_board[row+i][col+i]==1):
                        eval_human += 1
                if(eval_pc*eval_human==0 and eval_pc != eval_human):
                    for i in range(5):
                        if(grid_board[row+i][col+i]==0):
                            if(eval_human == 0):
                                if(player == 1):
                                    self.grid_value[row+i][col+i] += self.dScore[eval_pc]
                                else:
                                    self.grid_value[row+i][col+i] += self.aScore[eval_pc]
                            if (eval_pc == 0):
                                if (player == 2):
                                    self.grid_value[row+i][col+i] += self.dScore[eval_human]
                                else:
                                    self.grid_value[row+i][col+i] += self.aScore[eval_human]

                            if(eval_pc==4 or eval_human==4):
                                self.grid_value[row+i][col+i] *= 2

        # check right diagonal
        for row in range(4,len(self.grid_value)):
            for col in range(len(self.grid_value[row])-4):
                eval_pc = 0
                eval_human = 0
                for i in range(5):
                    if(grid_board[row-i][col+i]==2):
                        eval_pc += 1
                    if(grid_board[row-i][col+i]==1):
                        eval_human += 1
                if(eval_pc*eval_human==0 and eval_pc != eval_human):
                    for i in range(5):
                        if(grid_board[row-i][col+i]==0):
                            if(eval_human == 0):
                                if(player == 1):
                                    self.grid_value[row-i][col+i] += self.dScore[eval_pc]
                                else:
                                    self.grid_value[row-i][col + i] += self.aScore[eval_pc]
                            if (eval_pc == 0):
                                if (player == 2):
                                    self.grid_value[row-i][col + i] += self.dScore[eval_human]
                                else:
                                    self.grid_value[row-i][col + i] += self.aScore[eval_human]

                            if(eval_pc==4 or eval_human==4):
                                self.grid_value[row-i][col + i] *= 2

