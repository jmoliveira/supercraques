# coding: utf-8
#!/usr/bin/env python


class SuperCraquesError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
