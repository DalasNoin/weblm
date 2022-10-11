#!/usr/bin/env python
#
# natbot.py
#
# Set COHERE_KEY to your API key from os.cohere.ai, and then run this from a terminal.
#

import os
from multiprocessing import Pool

import cohere

from .controller import Command, Controller, Prompt
from .crawler import Crawler

co = cohere.Client(os.environ.get("COHERE_KEY"))

if (__name__ == "__main__"):

    def reset():
        _crawler = Crawler()

        def print_help():
            print("(g) to visit url\n(u) scroll up\n(d) scroll dow\n(c) to click\n(t) to type\n" +
                  "(h) to view commands again\n(r) to run suggested command\n(o) change objective")

        objective = "Make a reservation for 2 at 7pm at bistro vida in menlo park"
        print("\nWelcome to natbot! What is your objective?")
        i = input()
        if len(i) > 0:
            objective = i

        _controller = Controller(co, objective)
        return _crawler, _controller

    crawler, controller = reset()

    response = None
    crawler.go_to_page("google.com")
    while True:
        if response == "cancel":
            crawler, controller = reset()
        elif response == "success":
            controller.success()
            crawler, controller = reset()

        content = crawler.crawl()
        response = controller.step(crawler.page.url, content, response)

        print(response)

        if isinstance(response, Command):
            crawler.run_cmd(str(response))
        elif isinstance(response, Prompt):
            response = input(str(response))
