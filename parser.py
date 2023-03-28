#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import extras, moonfish

class Parser:
    def parse_fen(fen):
        fen = fen.split('-')
        castling = [
            [False, False, False, False],
            [False, False, False, False],
        ]
        pointer = 0
        for castling_ks in fen[2].split(','):
            if int(castling_ks)==1: castling[0][pointer] = True
            pointer=(pointer + 1) % 4
        for castling_qs in fen[3].split(','):
            if int(castling_qs)==1: castling[1][pointer] = True
            pointer=(pointer + 1) % 4
        enpassants=[(0,0),(0,0),(0,0),(0,0)]
        if 'enPassant' in fen[6]:
            info = fen[6].split('(')
            info = info[1].strip(')\'"')
            values = info.split(',')
            for value in values:
                value = value.strip("')}")
                if value != '':
                    squares = value.split(':')
                    enpassants[pointer] = (extras.REVERT_CORD[squares[0]], extras.REVERT_CORD[squares[1]])
                pointer = (pointer + 1) % 4
            fen[6] = fen[7]
