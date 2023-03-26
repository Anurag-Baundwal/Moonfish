#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
from random import randint
from time import sleep
class Book:
    def __init__(self, time_delay: int = 0, path: str = "") -> None:
        self.book = {}
        self.time_delay = time_delay
        if path != "": self.import_book(path)
    separator = " "
    def import_book(self, path: str) -> None:
        with open(path) as file:
            line = file.readline()
            while line:
                line = line.strip()
                line = line.split(self.separator)
                move = line[-1]
                line = " ".join(line[:-1])
                book_move = self.book.get(line)
                if book_move: self.book[line].append(move)
                else: self.book[line] = [move]
                line = file.readline()
        file.close()
    def get_book_move(self, line: str, skip_delay = False, auto_play: bool = True) -> str:
        play = ""
        book_move = self.book.get(line)
        if book_move: play = book_move[randint(0, len(book_move) - 1)]
        if self.time_delay > 0: sleep(self.time_delay)
        return play
