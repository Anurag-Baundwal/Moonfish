#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
from urllib3.exceptions import ProtocolError
try:
    from http.client import RemoteDisconnected
except ImportError:
    from http.client import BadStatusLine as RemoteDisconnected
import backoff
ENDPOINTS={
    "arrow":  "?token=d545syfDfy&arrows=h2-h4",
    "chat":   "?token=d545syfDfy&chat=hello",
    "play":   "?token=d545syfDfy&play=h2-h4",
    "resign": "?token=d545syfDfy&play=R",
    "stream": "?token=d545syfDfy&stream=1"
}
class Api():
    def __init__(self, url: str, token: str, bot_name: str = "?", version: str = "v1.0.0"):
        self.header = {}
        self.url = url
        self.token = token
        self.version = version
        self.session = requests.Session()
        self.set_user_agent(bot_name)
    def is_final(exception):
        return isinstance(exception, HTTPError) and exception.response.status_code < 500
    @backoff.on_exception(backoff.constant,
        (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout),
        max_time = 9999999999999,
        interval = 0.1,
        giveup = is_final)
    def api_get(self, path: str):
        url = urljoin(self.url, path)
        response = self.session.get(url, timeout = 2)
        response.raise_for_status()
        return response.json()
    def stream(self):
        url = urljoin(self.url, ENDPOINTS["stream"].format(self.token))
        return requests.get(url, headers = self.header, stream = True)
    def arrow(self, data: str):
        return self.api_get(ENDPOINTS["arrow"].format(self.token, data))
    def play(self, move: str):
        return self.api_get(ENDPOINTS["play"].format(self.token, move))
    def chat(self, message: str):
        return self.api_get(ENDPOINTS["chat"].format(self.token, message))
    def resign(self):
        return self.api_get(ENDPOINTS["resign"].format(self.token))
    def set_user_agent(self, user: str):
        self.header.update({"User-Agent": "chesscom-bot/{} user:{}".format(self.version, user)})
        self.session.headers.update(self.header)