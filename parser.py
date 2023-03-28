#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import string
from collections import defaultdict


class Parser:
    def __init__(self):
        self.sq_conv = dict(zip(string.ascii_lowercase[:14], range(1, 15)))
        self.sd_conv = {
            f'{c}P': 1, f'{c}N': 2, f'{c}B': 3,
            f'{c}R': 4, f'{c}Q': 5, f'{c}K': 6
            for c in 'rbyg'
        }
        self.col2mve = 0
        self.ep_sqrs = [0] * 5
        self.cst_sqrs = [[False] * 2 for _ in range(5)]
        self.color_mailbox = [
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            ]

        self.pieceMailbox = [
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
            -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1,
        ]


_kings = [0, 0, 0, 0, 0]


def parse_fen(fen):
    fen += "/0-0"
    delimiter = "-"
    pos = 0
    counter = 0
    is_done = False
    token = ""

    while (pos := fen.find(delimiter)) != -1:
        token = fen[:pos]
        if counter == 0:
            col = token[0]
            col2Mve = get_color(col)
        elif counter == 2:
            for p in range(4):
                ck = token[p * 2]
                cstSqrs[p + 1][0] = ck == '1'
        elif counter == 3:
            for i in range(4):
                ck = token[i * 2]
                cstSqrs[i + 1][1] = ck == '1'
        elif counter == 6:
            if "enPassant" in token:
                pose = 0
                ctr = 0
                ptr = -1
                epky = ""
                delimiter_e = "'"
                length = 0
                while (pose := token.find(delimiter_e)) != -1:
                    epky = token[:pose]
                    if ctr in [3, 5, 7, 9]:
                        ptr += 1
                        if epky == "":
                            goto_k = True
                            break
                        if epky[2] == ':':
                            length = 1
                        else:
                            length = 2
                        file = sqConv[epky[0]]
                        rank = abs(int(epky[1:length + 1]) - 14)
                        sq = rank * 16 + file
                        epSqrs[ptr + 1] = sq
                    ctr += 1
                    token = token[pose + len(delimiter_e):]
                if not goto_k:
                    is_done = True
            else:
                goto_l = True
                break
        if is_done:
            pose_board = 0
            pose_key = 0
            rank_data = ""
            key_data = ""
            delimiter_g = "/"
            delimiter_x = ","
            initial_start_pointer = 1
            while (pose_board := token.find(delimiter_g)) != -1:
                rank_data = token[:pose_board]
                rank_data += ",x"
                while (pose_key := rank_data.find(delimiter_x)) != -1:
                    key_data = rank_data[:pose_key]
                    if key_data == "x":
                        initial_start_pointer += 1
                    elif is_piece(key_data):
                        color_to_set = get_color(key_data[0])
                        colorMailbox[initial_start_pointer] = color_to_set
                        pieceMailbox[initial_start_pointer] = sdConv[key_data]
                        if sdConv[key_data] == 6:
                            _kings[color_to_set] = initial_start_pointer
                        initial_start_pointer += 1
                    else:
                        initial_start_pointer += int(key_data)
                    rank_data = rank_data[pose_key + len(delimiter_x):]
                initial_start_pointer += 2
                token = token[pose_board + len(delimiter_g):]
            break
        counter += 1
        fen = fen[pos + len(delimiter):]


def init_parser(self):
        self.sqConv = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,
            'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14}
        self.sdConv = {'rP': 1, 'rN': 2, 'rB': 3, 'rR': 4, 'rQ': 5, 'rK': 6, 'bP': 1, 'bN': 2, 'bB': 3, 'bR': 4, 'bQ': 5,
            'bK': 6, 'yP': 1, 'yN': 2, 'yB': 3, 'yR': 4, 'yQ': 5, 'yK': 6, 'gP': 1, 'gN': 2, 'gB': 3, 'gR': 4, 'gQ': 5, 'gK': 6}

    def is_piece(self, data):
        p = data[0]
        return p == 'r' or p == 'b' or p == 'y' or p == 'g'

    def get_color(self, color):
        if color == 'R' or color == 'r':
            return 1
        elif color == 'B' or color == 'b':
            return 2
        elif color == 'Y' or color == 'y':
            return 3
        else:
            return 4
