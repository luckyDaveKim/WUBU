#-*- coding: utf-8 -*-
import sys


class testInterface():
    def __init__(self, info):
        self.use = 0
        self.comment=""

    def printComment(self):
        print(self.comment)

    def checkUse(self):
        return self.use

    def setUse(self):
        self.use = 1

    def unsetUse(self):
        self.use = 0

    def run(self):
        raise NotImplementedError()

    def register(self):
        """" test module register """
        pass

    def process(self):
        self.run()

