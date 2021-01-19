import math
import copy
import time
import random
from math import sqrt
from random import randint
from operator import itemgetter, attrgetter, methodcaller
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and existing functions and variables.

class MinimaxTree():
    def __init__(self, color, move=None):
        self.move = move
        self.color = color
        self.data = None
        self.child_nodes = []
        #self.alpha = -9999
        #self.beta = 9999

class MonteCarloTree ():
    def __init__(self, board, color, move_list):
        self.board = board
        self.move_list = move_list
        self.color = color
        self.move = None
        self.parent_node = None
        self.child_nodes = []
        self.expanded = False
        self.is_terminal = False
        self.board_eval = 0
        self.ucb1_eval = 0
        self.no_of_wins = 0 #n/ni (Number of wins at this node leads to)
        self.no_of_steps = 0 #t/Vi (Number of steps to reach the terminal state)
        #self.no_of_wins_root = 0 #N (Number of wins at the root)

    def __str__(self):
        str_node = "Node:"+ str([self]) + "\n"
        str_parent = "Parent: " + str([self.parent_node]) + "\n"
        str_children = "Children: " + str([self.child_nodes]) + "\n"
        return str_node + str_parent + str_children


def color(color: int):
    if color == 1:
        return "B"
    else:
        return "W"

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        #---------------------------------#
        self.area = self.row*self.col
        self.count = 0
        if self.area <= 39:
            self.depth = 8
        elif self.area <= 49:
            self.depth = 5
        elif self.area <= 79:
            self.depth = 4
        else:
            self.depth = 4

    #get move of current game state
    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        #----------------------------------------------------------#
        # MINIMAX GAME TREE SEARCH AGENT
        #----------------------------------------------------------#
        root = MinimaxTree(self.opponent[self.color])
        self.recursive_dfs(root, self.depth)
        self.recursive_minimax(root)
        move_list = root.data[list(root.data)[0]]
        current = move_list[0]
        #self.board.make_move(current, self.color)
        best_mcts_move = current
        move = current
        #----------------------------------------------------------#
        '''
        #returns some random move from the list
        #--- DEBUGGING PURPOSES ---
        moves_user = self.board.get_all_possible_moves(self.color)
        moves_opponent = self.board.get_all_possible_moves(self.opponent[self.color])
        print("---USER MOVES---")
        for item in moves_user:
            for i in item:
                print(i.seq)
        print("---OPPONENT  MOVES---")
        for item in moves_opponent:
            for i in item:
                print(i.seq)

        board_sim = copy.deepcopy(self.board)
        move_sim = moves_user[0]
        print("Simulation Making move:" + str(move_sim))
        board_sim.make_move(move_sim[0], self.color)
        print("----- SIMULATION B -----")
        board_sim.show_board()
        print("Simulation score =" + str(self.board_heuristic(board_sim)))
        print("Terminal? :" + str(board_sim.is_win(self.color)))
        print("----------------------")

        #current2 = Move(moves_user[randint(0, len(moves_user) - 1)])
        #self.board.make_move(list(current2[0]), self.color)
        #print(current2)
        print("AI Making Move:" + str(move))'''
        #----------------------------------------------------------#
        # MONTE CARLO TREE SEARCH AGENT
        #----------------------------------------------------------#
        m_list = self.board.get_all_possible_moves(self.color)
        if len(m_list) == 1:
            self.board.make_move(m_list[0][0], self.color)
            return m_list[0][0]
        root = MonteCarloTree(self.board, self.color, m_list)
        self.board.make_move(best_mcts_move, self.color)
        move = best_mcts_move
        #----------------------------------------------------------#

        return move

        # -------- CHECKERS BOARD HEURISTIC FUNCTION --------#
        #Sources Referred:
        #https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
        #https://www.cs.huji.ac.il/~ai/projects/old/English-Draughts.pd

    @staticmethod
    def check_distance(p1, p2):
        #for two given checker pieces return the distance
        #using the distance formula sqrt((x2-x1)^2 + (y2-y1)^2)
        dist = sqrt(( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 ))
        return dist

    def board_heuristic(self, board):
        score = 0
        king_score = 10 + (self.col - 1)

        pawns_b = [] #black pawns
        pawns_w = [] #white pawns
        kings_b = [] #black kings
        kings_w = [] #white kings
        for r in range(self.row):
            for c in range(self.col):
                piece = board.board[r][c]
                if piece.color == "B":
                    if piece.is_king:
                        kings_b.append((r,c))
                    else:
                        pawns_b.append((r,c))
                elif piece.color == "W":
                    if piece.is_king:
                        kings_w.append((r,c))
                    else:
                        pawns_w.append((r,c))

        for pb in pawns_b:
            score = score + pb[0] + 10
        for pw in pawns_w:
            score = score - (10 + (self.row - 1 - pw[0]))

        for kb in kings_b:
            score = score + king_score
            distance = 0

            for kw in kings_w:
                distance = distance + self.check_distance(kb, kw)
            for pw in pawns_w:
                distance = distance + self.check_distance(kb, pw)
            if len(kings_w) + len(pawns_w) != 0:
                score = score - (distance/(len(kings_w) + len(pawns_w)))

        for kw in kings_w:
            score = score + king_score
            distance = 0

            for kb in kings_b:
                distance = distance + self.check_distance(kw, kb)
            for pb in pawns_b:
                distance = distance + self.check_distance(kw, pb)
            if len(kings_b) + len(pawns_b) != 0:
                score = score - (distance/(len(kings_b) + len(pawns_b)))

        if self.color == 2:
            return score
        else:
            return -score


    #Sources Referred:
    #https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
    def recursive_dfs(self, root: MinimaxTree, depth = 1):
        if depth == 0:
            pass
        else:
            if root.move is not None:
                self.board.make_move(root.move, root.color)
            all_moves_list = self.board.get_all_possible_moves(self.opponent[root.color])
            for r in range(len(all_moves_list)):
                for c in range(len(all_moves_list[r])):
                    root.child_nodes.append(MinimaxTree(self.opponent[root.color], all_moves_list[r][c]))
            for node in root.child_nodes:
                self.recursive_dfs(node, depth-1)
            if root.move is not None:
                self.board.undo()

    #-------- MINIMAX ALGORITHM-------#
    #Sources Referred:
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/?ref=lbp
    #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
    #https://github.com/techwithtim/Python-Checkers-AI/blob/master/minimax/algorithm.py


    def min_or_max(self, color):
        if color == self.color:
            return max
        else:
            return min

    def minimax(self, color, children):
        min_or_max = self.min_or_max(color)
        hash_table = {}
        for child in children:
            for val in child.data.keys():
                hash_table.setdefault(val,[]).append(child.move)
        return {min_or_max(hash_table): hash_table[min_or_max(hash_table)]}

    def recursive_minimax(self, root: MinimaxTree):
        if root.move is not None:
            self.board.make_move(root.move, root.color)
        if len(root.child_nodes) == 0:
            root.data = {
                self.board_heuristic(self.board): []
            }
        else:
            for node in root.child_nodes:
                self.recursive_minimax(node)
            root.data = self.minimax(root.color,root.child_nodes)

        if root.move is not None:
            self.board.undo()

    # -------- MONTE CARLO TREE SEARCH ALGORITHM-------#
    # Sources Referred:
    # https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
    # https://int8.io/monte-carlo-tree-search-beginners-guide/
    # https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/

    def simulate(self, board, move):
        #print("SIMULATE")
        #board_sim = copy.deepcopy(board)
        #board_sim.make_move(move, self.color)
        board.make_move(move, self.color)
        score = self.board_heuristic(board) #board_sim
        return score, board #,board_sim

    def expansion(self, node: MonteCarloTree):
        #print("EXPANSION")
        #print(node)
        if node.board.is_win(self.color) > 0 or node.board.is_win(self.opponent[self.color]) > 0:
            node.expanded = True
            return

        for move_set in node.move_list:
            for move in move_set:
                score, new_board =  self.simulate(node.board, move)
                m_list = new_board.get_all_possible_moves(self.color)
                new_mcts_node = MonteCarloTree(new_board, self.color, m_list)
                new_mcts_node.move = move
                new_mcts_node.parent_node = node
                new_mcts_node.board_eval = score
                node.child_nodes.append(new_mcts_node)
                node.board.undo()

        #print("FINAL EXPANSION:")
        #print(node)

    def rollout(self, node: MonteCarloTree, steps=0):
        #print("ROLLOUT")
        #print(node)
        if node.board.is_win(self.color) > 0 or node.board.is_win(self.opponent[self.color]) > 0: #or steps > 1000:
            node.no_of_wins += int(node.board.is_win(self.color))
            node.no_of_steps = steps
            #print("Roll-BACKPROPOGATE")
            self.backpropogate(node)
            return

        while node.board.is_win(self.color) < 1 or node.board.is_win(self.opponent[self.color]) < 1:
            self.expansion(node)
            #Recursive Expansion
            children = node.child_nodes
            for child in children:
                if not child.expanded:
                    #print("ROLLOUT RECURSE")
                    self.rollout(child, steps+1)
                    #print("END ROLLOUT RECURSE")
                    return
                else:
                    pass

    def backpropogate(self, node:MonteCarloTree):
        #print("BACKPROPOGATE")
        #print(node)

        #update UCB1 value too

        if node.parent_node is None:
            #print("reached root node")
            return

        if node.parent_node is not None:
            node.parent_node.ucb1_eval += node.ucb1_eval
            node.parent_node.no_of_wins += node.no_of_wins
            node.parent_node.no_of_steps += node.no_of_steps
            node.board.undo()
            #print("Recurse-BACKPROPOGATE")
            self.backpropogate(node.parent_node)
            #print("End Recurse Backpropogate")

    def monte_carlo_tree_search(self, node: MonteCarloTree):
        #print("MCTS SEARCH START")
        self.expansion(node)
        #print(node)
        for nd in node.child_nodes: #should be a while loop, and always start from the root
            self.rollout(nd)
            root_wins = node.no_of_wins
            self.ucb1_evaluation(root_wins, nd)
        best_child = self.choose_best_child(node)
        return best_child.move

    def choose_best_child(self, node: MonteCarloTree):
        children = sorted(node.child_nodes, key= attrgetter('ucb1_eval'), reverse=True)
        return children[0]

    def ucb1_evaluation(self, no_of_wins_r, node: MonteCarloTree):
        #print("No. of steps = " + str(node.no_of_steps))
        #print("No. of wins at root = " + str(no_of_wins_r))
        #print("No. of wins at this node = " + str(node.no_of_wins))
        node.ucb1_eval = node.no_of_steps + 2 * math.sqrt((math.log(no_of_wins_r))/(node.no_of_wins+1))
        return

    '''
    def expansion(self, child_node: MonteCarloTree):
        #print("EXPANSION")
        #print(node)
        if node.board.is_win(self.color) > 0 or node.board.is_win(self.opponent[self.color]) > 0:
            node.expanded = True
            return

        for move_set in node.move_list:
            for move in move_set:
                score, new_board =  self.simulate(node.board, move)
                m_list = new_board.get_all_possible_moves(self.color)
                new_mcts_node = MonteCarloTree(new_board, self.color, m_list)
                new_mcts_node.move = move
                new_mcts_node.parent_node = node
                new_mcts_node.board_eval = score
                node.child_nodes.append(new_mcts_node)
                node.board.undo()

        #print("FINAL EXPANSION:")
        #print(node)
    '''





