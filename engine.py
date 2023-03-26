#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
from time import time
from time import sleep
import json, api, random
import subprocess
class EngineFPC:
    def __init__(self, engine_path: str, api_handler):
        self.engine = subprocess.Popen(
            engine_path,
            universal_newlines = True,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            bufsize = 1,
        )
        self.bestmove_found = ""
        self.api_handler = api_handler
        self.move_info = []
    def put(self, command: str):
        self.engine.stdin.write(command + '\n')
    def get(self):
        while True:
            text = self.engine.stdout.readline().strip()
            if text == 'search complete': return text
            self.move_info.append(text)
    def decode_uci_move(self, text: str):
        data = text.split(' ')
        depth_reached = int(data[1])
        nodes_reached = int(data[3])
        bestmove_found = data[5]
        pos_eval = data[7]
        elapsed_time = int(data[9])
        pv_line = data[11]
        return depth_reached, nodes_reached, bestmove_found, pos_eval, elapsed_time, pv_line
    def clear_move_info(self):
        self.move_info = []
    def search_fen_str(self, fen: str, time_allowed: int):
        self.clear_move_info()
        self.bestmove_found = ""
        self.put("go " + fen + " " + str(time_allowed))
        return self.get()
