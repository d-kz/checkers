from copy import deepcopy
import time
import math
import random

ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"



EMPTY_CELL = "---"

class Node:
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, maximizing_player, mandatory_jumping):
        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        big_letter = ""
        queen_row = 0
        if maximizing_player is True:
            available_moves = Checkers.find_available_moves(current_state, mandatory_jumping)
            big_letter = "C"
            queen_row = 7
        else:
            available_moves = Checkers.find_player_available_moves(current_state, mandatory_jumping)
            big_letter = "B"
            queen_row = 0
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
        return children_states

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent


class Checkers:
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.current_turn = True
        self.computer_pieces = 12
        self.player_pieces = 12
        self.available_moves = []
        self.mandatory_jumping = False

        for row in self.matrix:
            for i in range(8):
                row.append(EMPTY_CELL)
        self.position_computer()
        self.position_player()

    def position_computer(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("c" + str(i) + str(j))

    def position_player(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("b" + str(i) + str(j))

    def print_matrix(self):
        i = 0
        print()
        for row in self.matrix:
            print(i, end="  |")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n")

    def get_player_input(self):
        available_moves = Checkers.find_player_available_moves(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            if self.computer_pieces > self.player_pieces:
                print(
                    ansi_red + "You have no moves left, and you have fewer pieces than the computer.YOU LOSE!" + ansi_reset)
                exit()
            else:
                print(ansi_yellow + "You have no available moves.\nGAME ENDED!" + ansi_reset)
                exit()
        self.player_pieces = 0
        self.computer_pieces = 0
        while True:

            coord1 = input("Which piece[i,j]: ")
            if coord1 == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit()
            elif coord1 == "s":
                print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
                exit()
            coord2 = input("Where to[i,j]:")
            if coord2 == "":
                print(ansi_cyan + "Game ended!" + ansi_reset)
                exit()
            elif coord2 == "s":
                print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
                exit()
            old = coord1.split(",")
            new = coord2.split(",")

            if len(old) != 2 or len(new) != 2:
                print(ansi_red + "Ilegal input" + ansi_reset)
            else:
                old_i = old[0]
                old_j = old[1]
                new_i = new[0]
                new_j = new[1]
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print(ansi_red + "Ilegal input" + ansi_reset)
                else:
                    move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    if move not in available_moves:
                        print(ansi_red + "Ilegal move!" + ansi_reset)
                    else:
                        Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "B", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                                    self.computer_pieces += 1
                                elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                                    self.player_pieces += 1
                        break

    def count_pieces(self):
        self.player_pieces = 0
        self.computer_pieces = 0
        for m in range(8):
            for n in range(8):
                if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                    self.computer_pieces += 1
                elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                    self.player_pieces += 1

    @staticmethod
    def find_available_moves(board, mandatory_jumping):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n][0] == "c": # forward
                    if Checkers.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2): # TODO: 'eating'? 
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n][0] == "C": # both directions
                    if Checkers.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    @staticmethod
    def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        # 
        if board[via_i][via_j] == EMPTY_CELL:
            return False
        if board[via_i][via_j][0] == "C" or board[via_i][via_j][0] == "c": # 
            return False

        if board[new_i][new_j] != EMPTY_CELL: # target needs to be empty
            return False

        if board[old_i][old_j] == EMPTY_CELL:
            return False
        if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
            return False
        return True

    @staticmethod
    def check_moves(board, old_i, old_j, new_i, new_j):

        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[old_i][old_j] == EMPTY_CELL:
            return False
        if board[new_i][new_j] != EMPTY_CELL:
            return False
        if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
            return False
        if board[new_i][new_j] == EMPTY_CELL:
            return True

    @staticmethod
    def calculate_heuristics(board):
        result = 0
        mine = 0
        opp = 0
        """
        Example board:
        0  |--- c01 --- c03 --- c05 --- c07 
        1  |c10 --- c12 --- c14 --- --- --- 
        2  |--- --- --- c23 --- --- --- c27 
        3  |b30 --- --- --- c34 --- --- --- 
        4  |--- b41 --- c43 --- b45 --- c47 
        5  |b50 --- b52 --- --- --- b56 --- 
        6  |--- --- --- --- --- b65 --- b67 
        7  |b70 --- b72 --- b74 --- b76 --- 

             0   1   2   3   4   5   6   7  
        """

        for i in range(8):
            for j in range(8):
                # [0] is for letter of the element. 
                if board[i][j][0] == "c" or board[i][j][0] == "C":
                    mine += 1

                    # # "counting pieces". Queens are 2x.
                    # if board[i][j][0] == "c":
                    #     result += 5
                    # if board[i][j][0] == "C":
                    #     result += 10
                    # # "border/corner piece" - since they are protected
                    # if i == 0 or j == 0 or i == 7 or j == 7: 
                    #     result += 7
                    # # if border piece, skip following logic
                    # if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                    #     continue

                    # # "YOUR piece can be eaten": if (next to an enemy piece) & (cell behind you is free)
                    # # TODO: why [0] for one but not the other. What's at board[i][j]?
                    # if (board[i + 1][j - 1][0] == "b" or board[i + 1][j - 1][0] == "B") and board[i - 1][j + 1] == EMPTY_CELL:
                    #     result -= 3
                    # if (board[i + 1][j + 1][0] == "b" or board[i + 1][j + 1] == "B") and board[i - 1][j - 1] == EMPTY_CELL:
                    #     result -= 3
                    # # Queen can eat backwards too
                    # if board[i - 1][j - 1][0] == "B" and board[i + 1][j + 1] == EMPTY_CELL:
                    #     result -= 3
                    # if board[i - 1][j + 1][0] == "B" and board[i + 1][j - 1] == EMPTY_CELL:
                    #     result -= 3

                    # if i + 2 > 7 or j - 2 < 0:
                    #     continue
                    # # "ENEMY can be eaten (to-the-left)"
                    # if (board[i + 1][j - 1][0] == "B" or board[i + 1][j - 1][0] == "b") and board[i + 2][j - 2] == EMPTY_CELL:
                    #     result += 6 # TODO: why you gain 6 if you can eat something, but lose only 3 if you can be eaten?
                    # if i + 2 > 7 or j + 2 > 7: 
                    #     continue
                    # # "ENEMY can be eaten (to-the-right)"
                    # if (board[i + 1][j + 1][0] == "B" or board[i + 1][j + 1][0] == "b") and board[i + 2][j + 2] == EMPTY_CELL:
                    #     result += 6

                elif board[i][j][0] == "b" or board[i][j][0] == "B": # TODO: why we dont' do the same for opponent?
                    opp += 1

        # We value pieces above all, so if we ever lose a piece, it's a huge loss. 
        # Everything else is positional advantage just to differentiate. 
        # position_heuristic + (piece count difference)*1000.
        return result + (mine - opp) * 1000

    @staticmethod
    def find_player_available_moves(board, mandatory_jumping):
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n][0] == "b":
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                elif board[m][n][0] == "B":
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Checkers.check_player_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_player_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    @staticmethod
    def check_player_moves(board, old_i, old_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[old_i][old_j] == EMPTY_CELL:
            return False
        if board[new_i][new_j] != EMPTY_CELL:
            return False
        if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
            return False
        if board[new_i][new_j] == EMPTY_CELL:
            return True

    @staticmethod
    def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[via_i][via_j] == EMPTY_CELL:
            return False
        if board[via_i][via_j][0] == "B" or board[via_i][via_j][0] == "b":
            return False
        if board[new_i][new_j] != EMPTY_CELL:
            return False
        if board[old_i][old_j] == EMPTY_CELL:
            return False
        if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
            return False
        return True

    def evaluate_states(self, maximizing_player, silent, depth=4):
        """
        return: -1 - "computer" lost, 0 - neutral (game keeps going), 1 - "player" won
        """
        t1 = time.time()
        current_state = Node(deepcopy(self.matrix))

        first_computer_moves = current_state.get_children(maximizing_player, self.mandatory_jumping)
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print(
                    ansi_yellow + "Computer has no available moves left, and you have more pieces left.\nYOU WIN!" + ansi_reset)
                return -1
            else:
                print(ansi_yellow + "Computer has no available moves left.\nGAME ENDED!" + ansi_reset)
                return -1

        # find the most optimal move. Note the switch in maximizing_player's turn. 
        dict = {}
        for i in range(len(first_computer_moves)):
            value_child = first_computer_moves[i]
            key_value = Checkers.minimax(value_child.get_board(), depth, -math.inf, math.inf, not(maximizing_player), self.mandatory_jumping)
            l = dict.get(key_value, [])
            l.append(value_child)
            dict[key_value] = l # TODO: why can't update list in-place?
            # print(l, dict, key_value, value_child)
        if len(dict.keys()) == 0:
            print(ansi_green + "Computer has cornered itself.\nYOU WIN!" + ansi_reset)

        # pick best move from computed options
        if maximizing_player:
            best_value = max(dict)
        else:
            best_value = min(dict)

        if not silent:
            copy = [(key, value[0].move) for (key, value) in deepcopy(dict).items()]
            print(best_value, copy)
        best_boards = dict[best_value]

        if len(best_boards) > 1:
            best_board = random.sample(best_boards, 1)[0]
        else:
            best_board = best_boards[0]        
        new_board = best_board.get_board()
        move = best_board.move 
        self.matrix = new_board
        t2 = time.time()
        diff = t2 - t1
        if not silent:
            print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(move[3]) + ").")
            print("It took him " + str(diff) + " seconds.")

        # update pieces count
        self.count_pieces()

        return 0

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player, mandatory_jumping):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player:
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    @staticmethod
    def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
        letter = board[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = EMPTY_CELL

        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = EMPTY_CELL

        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = EMPTY_CELL

        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = EMPTY_CELL

        if new_i == queen_row:
            letter = big_letter
        board[old_i][old_j] = EMPTY_CELL
        board[new_i][new_j] = letter + str(new_i) + str(new_j)

    def play(self, silent=False, depths=[4,4]):
        if not silent:
            print(ansi_cyan + "##### WELCOME TO CHECKERS ####" + ansi_reset)
            print("\nSome basic rules:")
            print("1.You enter the coordinates in the form i,j.")
            print("2.You can quit the game at any time by pressing enter.")
            print("3.You can surrender at any time by pressing 's'.")
            print("Now that you've familiarized yourself with the rules, enjoy!")
        self.mandatory_jumping = True
        # while True:
        #     answer = input("\nFirst, we need to know, is jumping mandatory?[Y/n]: ")
        #     if answer == "Y":
        #         self.mandatory_jumping = True
        #         break
        #     elif answer == "n":
        #         self.mandatory_jumping = False
        #         break
        #     else:
        #         print(ansi_red + "Invalid option!" + ansi_reset)
        
        status = 0
        while (status == 0):
            if not silent:
                self.print_matrix()
            if self.current_turn is True:
                if not silent:
                    print(ansi_cyan + "\nPlayer's turn." + ansi_reset)
                # self.get_player_input()
                status = self.evaluate_states(maximizing_player=False, silent=silent, depth=depths[0])
            else:
                if not silent:
                    print(ansi_cyan + "Computer's turn." + ansi_reset)
                    print("Thinking...")
                status = self.evaluate_states(maximizing_player=True, silent=silent, depth=depths[0])

            if self.player_pieces == 0:
                self.print_matrix()
                print(ansi_red + "You have no pieces left.\nYOU LOSE!" + ansi_reset)
                status = 1
            elif self.computer_pieces == 0:
                self.print_matrix()
                print(ansi_green + "Computer has no pieces left.\nYOU WIN!" + ansi_reset)
                status = -1

            # ENDGAME
            if (self.player_pieces == 1 and self.computer_pieces >=2):
                print(ansi_red + "You have 1 piece left, computer has more than 2.\nYOU LOSE!" + ansi_reset)
                status = -1  
            if (self.computer_pieces == 1 and self.player_pieces >= 2):
                print(ansi_red + "Computer has 1 piece left, you have more than 2.\nYOU LOSE!" + ansi_reset)
                status = 1
            # elif self.computer_pieces - self.player_pieces == 7:
            #     wish = input("You have 7 pieces fewer than your opponent.Do you want to surrender?")
            #     if wish == "" or wish == "yes":
            #         print(ansi_cyan + "Coward." + ansi_reset)
            #         exit()
            self.current_turn = not self.current_turn

        return(status)


def run_trials(n, depths):
    total = 0.0
    print(n,depths)
    for i in range(n):
        checkers = Checkers()
        status = checkers.play(silent=True, depths=depths)
        total += status
    print(total/n)



if __name__ == '__main__':
    # run_trials(10, depths=[4,3])
    run_trials(10, depths=[4,2])
    # run_trials(10, depths=[4,1])

    # checkers = Checkers()
    # checkers.play()

"""
TRIALS:
Symmetrical heuristic: (piece count), depth: (player=4, computer=4)      
0.2 (10)
Symmetrical heuristic: (piece count), depth: (player=4, computer=3)      
0.4 (10)
Symmetrical heuristic: (piece count), depth: (player=4, computer=2)      
0.6 (10)
-0.4
Symmetrical heuristic: (piece count), depth: (player=4, computer=1)      
-0.4 (10) - lolwhat
-0.2
Seems like trash results tbh. Possiblity for difference in depth computing imperfect estimates of the opponent, but I've seen weird moves in general. 
"""












