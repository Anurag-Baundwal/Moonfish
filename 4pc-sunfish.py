#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import time
import platform
import api
import extras
import json
from itertools import count
from collections import namedtuple
colors = (2, 3, 0, 1)
double_pawns = (-16, 1, 16, -1)

initial = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (2, 6), (2, 4), (2, 5), (2, 8), (2, 7), (2, 5), (2, 4), (2, 6), 0, 0, 0, 0, 0, 0, 0, 0, (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (1, 6), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 6), 0, 0, (1, 4), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 4), 0, 0, (1, 5), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 5), 0, 0, (1, 8), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (
    3, 7), 0, 0, (1, 7), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 8), 0, 0, (1, 5), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 5), 0, 0, (1, 4), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 4), 0, 0, (1, 6), (1, 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3), (3, 6), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), 0, 0, 0, 0, 0, 0, 0, 0, (0, 6), (0, 4), (0, 5), (0, 7), (0, 8), (0, 5), (0, 4), (0, 6), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# initial board state
# (0, 0) -> first item is the color (0 to 4)
#        -> second item is the type of piece (0, 1, 2, 3 = pawn, 6 = rook, 4 = bishop, 5 = knight, 7 = king, 8 = queen)

valid_keys = (36, 37, 38, 39, 40, 41, 42, 43, 52, 53, 54, 55, 56, 57, 58, 59, 68, 69, 70, 71, 72, 73, 74, 75, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 145, 146, 147,148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 212, 213, 214, 215, 216, 217, 218, 219, 228, 229, 230, 231, 232, 233, 234, 235, 244, 245, 246, 247, 248, 249, 250, 251)
# the valid squares / the playing area

directions = [(-16, -32, -15, -17), (1, 2, -15, 17), (16, 32, 15, 17), (-1, -2, -17, 15), (-33, 33, -31, 31, 18, -18, 14, -14),
              (-17, -15, 17, 15), (1, -1, 16, -16), (1, -1, 16, -16, -17, -15, 17, 15), (1, -1, 16, -16, -17, -15, 17, 15)]
# direction offsets to move pieces
# 0, 1, 2, 3 = pawns
# 4 =
revert_cord = {"d14": 36, "e14": 37, "f14": 38, "g14": 39, "h14": 40, "i14": 41, "j14": 42, "k14": 43, "d13": 52, "e13": 53, "f13": 54, "g13": 55, "h13": 56, "i13": 57, "j13": 58, "k13": 59, "d12": 68, "e12": 69, "f12": 70, "g12": 71, "h12": 72, "i12": 73, "j12": 74, "k12": 75, "a11": 81, "b11": 82, "c11": 83, "d11": 84, "e11": 85, "f11": 86, "g11": 87, "h11": 88, "i11": 89, "j11": 90, "k11": 91, "l11": 92, "m11": 93, "n11": 94, "a10": 97, "b10": 98, "c10": 99, "d10": 100, "e10": 101, "f10": 102, "g10": 103, "h10": 104, "i10": 105, "j10": 106, "k10": 107, "l10": 108, "m10": 109, "n10": 110, "a9": 113, "b9": 114, "c9": 115, "d9": 116, "e9": 117, "f9": 118, "g9": 119, "h9": 120, "i9": 121, "j9": 122, "k9": 123, "l9": 124, "m9": 125, "n9": 126, "a8": 129, "b8": 130, "c8": 131, "d8": 132, "e8": 133, "f8": 134, "g8": 135, "h8": 136, "i8": 137, "j8": 138, "k8": 139, "l8": 140, "m8": 141,
               "n8": 142, "a7": 145, "b7": 146, "c7": 147, "d7": 148, "e7": 149, "f7": 150, "g7": 151, "h7": 152, "i7": 153, "j7": 154, "k7": 155, "l7": 156, "m7": 157, "n7": 158, "a6": 161, "b6": 162, "c6": 163, "d6": 164, "e6": 165, "f6": 166, "g6": 167, "h6": 168, "i6": 169, "j6": 170, "k6": 171, "l6": 172, "m6": 173, "n6": 174, "a5": 177, "b5": 178, "c5": 179, "d5": 180, "e5": 181, "f5": 182, "g5": 183, "h5": 184, "i5": 185, "j5": 186, "k5": 187, "l5": 188, "m5": 189, "n5": 190, "a4": 193, "b4": 194, "c4": 195, "d4": 196, "e4": 197, "f4": 198, "g4": 199, "h4": 200, "i4": 201, "j4": 202, "k4": 203, "l4": 204, "m4": 205, "n4": 206, "d3": 212, "e3": 213, "f3": 214, "g3": 215, "h3": 216, "i3": 217, "j3": 218, "k3": 219, "d2": 228, "e2": 229, "f2": 230, "g2": 231, "h2": 232, "i2": 233, "j2": 234, "k2": 235, "d1": 244, "e1": 245, "f1": 246, "g1": 247, "h1": 248, "i1": 249, "j1": 250, "k1": 251}
# self explanatory

coordinates = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "d14", "e14", "f14", "g14", "h14", "i14", "j14", "k14", 0, 0, 0, 0, 0, 0, 0, 0, "d13", "e13", "f13", "g13", "h13", "i13", "j13", "k13", 0, 0, 0, 0, 0, 0, 0, 0, "d12", "e12", "f12", "g12", "h12", "i12", "j12", "k12", 0, 0, 0, 0, 0, "a11", "b11", "c11", "d11", "e11", "f11", "g11", "h11", "i11", "j11", "k11", "l11", "m11", "n11", 0, 0, "a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10", "j10", "k10", "l10", "m10", "n10", 0, 0, "a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9", "j9", "k9", "l9", "m9", "n9", 0, 0, "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8",
               "j8", "k8", "l8", "m8", "n8", 0, 0, "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7", "j7", "k7", "l7", "m7", "n7", 0, 0, "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6", "j6", "k6", "l6", "m6", "n6", 0, 0, "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5", "j5", "k5", "l5", "m5", "n5", 0, 0, "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", "k4", "l4", "m4", "n4", 0, 0, 0, 0, 0, "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", 0, 0, 0, 0, 0, 0, 0, 0, "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", 0, 0, 0, 0, 0, 0, 0, 0, "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# self explanatory

promotion = [(81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94), (43, 59, 75, 91, 107, 123, 139, 155, 171, 187, 203, 219, 235, 251),
             (193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206), (36, 52, 68, 84, 100, 116, 132, 148, 164, 180, 196, 212, 228, 244)]
# promotion squares
# 4 tuples - one for each color

pstart = (52, 53, 54, 55, 56, 57, 58, 59, 82, 98, 114, 130, 146, 162, 178, 194,
          93, 109, 125, 141, 157, 173, 189, 205, 228, 229, 230, 231, 232, 233, 234, 235)
# starting positions of the pieces?

pvs = (100, 100, 100, 100, 300, 400, 525, 1025, 60000)
# material values

delta_margin = pvs[7]  # 1025 (Queen value)
infinity = 999999
mate = infinity-100000


class Position(namedtuple('Position', 'board score color')):
    def gen_moves(self):
        moves = []
        for key in extras.VALID_KEYS:
            if self.board[key] == 0 or self.board[key][0] != self.color:
                continue  # empty square or piececolor != side to move
            # self.board[key][1] selects the type of piece
            for location in directions[self.board[key][1]]:
                for keyr in count(key + location, location):  # keyr ?
                    if keyr not in extras.VALID_KEYS:
                        break
                    elif self.board[keyr] == 0:
                        captured = False
                    elif self.board[keyr][0] == self.color or self.board[keyr][0] == colors[self.color]:
                        break
                    else:
                        captured = True
                    if self.board[keyr] in (0, 1, 2, 3) and location in (-16, 16, 1, -1, -32, 32, 2, -2) and captured:
                        break
                    if self.board[keyr] in (0, 1, 2, 3) and location in (-32, 32, 2, -2) and (key not in pstart or self.board[keyr-double_pawns[self.color]]) != 0:
                        break
                    if self.board[keyr] in (0, 1, 2, 3) and location in (-17, -15, 17, 15) and not captured:
                        break
                    moves.append((key, keyr))
                    if self.board[keyr] in (0, 1, 2, 3, 4, 8) or captured:
                        break
        return moves

    def nullmove(self):
        return Position(self.board, -self.score, (self.color+1) % 4)

    def move(self, move):
        board, score = self.board[:], self.score
        score = score+self.value(move)
        if board[move[0]][1] in (0, 1, 2, 3) and move[1] in promotion[self.color]:
            board[move[0]] = (self.color, 7)
        board[move[1]] = board[move[0]]
        board[move[0]] = 0
        return Position(board, -score, (self.color+1) % 4)

    def dead(self):
        pos = self.nullmove()
        for move in pos.gen_moves():
            if self.board[move[1]] != 0 and self.board[move[1]][1] == 8:
                return True
        pos = Position(self.board, -self.score, (self.color+2) % 4)
        for move in pos.gen_moves():
            if self.board[move[1]] != 0 and self.board[move[1]][1] == 8:
                return True
        return False

    def value(self, move):
        score = 0
        if self.board[move[1]] != 0:
            score += pvs[self.board[move[1]][1]]
        if self.board[move[0]][1] in (0, 1, 2, 3) and move[1] in promotion[self.color]:
            score -= pvs[0]+pvs[7]
        return score

    def hash(self):
        h = ''
        loop = iter(self.board[:])
        for square in loop:
            if square == 0:
                h += 'v'
            else:
                h += extras.indexing(square)
        return h

    def render(self):
        g = m = r = ""
        a = iter(self.board[:])
        for c in range(36):
            next(a)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for d in range(3):
            for e in range(8):
                f = next(a)
                if f == 0:
                    g += "     |"
                else:
                    g += " "+str(f[0])+"."+str(f[1])+" |"
            if d < 2:
                for h in range(8):
                    next(a)
            print("|-----|-----|-----|"+g+"-----|-----|-----|\n")
            print(
                "+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            g = ""
        for j in range(5):
            next(a)
        for k in range(8):
            for l in range(14):
                t = next(a)
                if t == 0:
                    m += "     |"
                else:
                    m += " "+str(t[0])+"."+str(t[1])+" |"
            if k < 7:
                for i in range(2):
                    next(a)
            print("|"+m+"\n")
            print(
                "+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            m = ""
        for n in range(5):
            next(a)
        for o in range(3):
            for p in range(8):
                q = next(a)
                if q == 0:
                    r += "     |"
                else:
                    r += " "+str(q[0])+"."+str(q[1])+" |"
            if o < 2:
                for s in range(8):
                    next(a)
            print("|-----|-----|-----|"+r+"-----|-----|-----|\n")
            print(
                "+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            r = ""


class Search:
    def __init__(self):
        self.nodes = 0
        self.tt_score = {}
        self.tt_move = {}

    def preform(self, pos):
        self.nodes = 0
        self.tt_score = {}
        best_move = ()
        for depth in range(1, 1000):
            best = alpha = -infinity
            beta = -alpha
            for move in self.sorted(pos):
                score = -self.search(pos.move(move), -beta, -alpha, depth-1, 1)
                if score >= beta:
                    best_move = move
                    best = score
                    break
                if score > best:
                    best_move = move
                    best = score
                    alpha = max(alpha, score)
            yield best_move, depth, best

    def search(self, pos, alpha, beta, depth=3, ply=1):
        self.nodes += 1
        if pos.dead():
            return -mate+ply
        mating_value = mate-ply
        if mating_value < beta:
            beta = mating_value
            if alpha >= mating_value:
                return mating_value
        mated_value = -mate+ply
        if mated_value > alpha:
            alpha = mated_value
            if beta <= mated_value:
                return mated_value
        depth = max(depth, 0)
        entry = self.tt_score.get(pos.hash())
        if entry and entry[1] >= depth:
            if entry[0] == 0:
                return entry[2]
            elif entry[0] == -1:
                alpha = max(alpha, entry[2])
            elif entry[1] == 1:
                beta = min(beta, entry[2])
            if alpha >= beta:
                return entry[2]
        if depth <= 0:
            return self.qsearch(pos, alpha, beta, ply+1)
        o_alpha = alpha
        best = -infinity
        if len(pos.gen_moves()) < 2:
            depth += 1
        for move in self.sorted(pos):
            score = -self.search(pos.move(move), -beta, -alpha, depth-1, ply+1)
            if score >= beta:
                self.tt_move[pos.hash()] = move
                best = score
                break
            if score > best:
                self.tt_move[pos.hash()] = move
                best = score
                alpha = max(alpha, score)
        if best <= o_alpha:
            self.tt_score[pos.hash()] = (1, depth, best)
        elif best >= beta:
            self.tt_score[pos.hash()] = (-1, depth, best)
        else:
            self.tt_score[pos.hash()] = (0, depth, best)
        return best

    def qsearch(self, pos, alpha, beta, ply):
        self.nodes += 1
        if pos.dead():
            return -mate+ply
        score = pos.score
        if score >= beta:
            return beta
        if score < alpha-delta_margin:
            return alpha
        alpha = max(alpha, score)
        for move in self.sorted(pos):
            if pos.board[move[1]] == 0:
                continue
            score = -self.qsearch(pos.move(move), -beta, -alpha, ply+1)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha

    def sorted(self, pos):
        killer = self.tt_move.get(pos.hash())
        if killer:
            yield killer
        for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
            if move == killer:
                # If this move matches the killer then continue, we have already yielded the killer move.
                continue
            yield move


def main():
    search = Search()
    history = [Position(initial, 0, 0)]
    history[-1].render()
    x = 0
    while True:
        # Fire the engine up and search for a move.
        start = time.time()
        for move, depth, score in search.preform(history[-1]):
            if time.time()-start > 6:
                break
        history.append(history[-1].move(move))
        history[-1].render()
        print("Depth Reached:"+str(depth)+"\n")
        print("Nodes Reached:"+str(search.nodes)+"\n")
        if history[-1].color in (1, 3):
            print("Eval Score: "+str(-score)+"\n")
        else:
            print("Eval Score: "+str(score)+"\n")
        if history[-1].dead():
            break


if __name__ == '__main__':
    main()
