import re
import os
import time


class Setter:
    def __init__(self, func, regex):
        self.func = func
        self.regex = regex

    def match(self, text):
        if re.match(self.regex, text):
            return True
        return False

    def execute(self, node, command):
        node.set_input_vars(re.match(self.regex, command).groupdict())
        self.func(node)


class Node:
    def __init__(self):
        self.state = {}
        self.input_vars = {}
        self.setters = []
        self.printer = None

    def set_state(self, state):
        self.state = state

    def set_input_vars(self, input_vars):
        self.input_vars = input_vars

    def get_state_var(self, key):
        return self.state.get(key)

    def update_state_var(self, new_state: dict):
        self.state.update(new_state)

    def get_input_var(self, key):
        return self.input_vars.get(key)

    def get_state(self):
        return self.state

    def set_printer(self, printer):
        self.printer = printer

    def get_setters(self):
        return self.setters

    def print_state(self):
        os.system("clear")
        if self.printer is not None:
            self.printer(self)
        else:
            print("\033[31mNo Printer\033[0m")

    def execute_input(self, user_input):
        for setter in self.get_setters():
            if setter.match(user_input):
                return setter.execute(self, user_input)
        print("Invalid command")
        time.sleep(1)

    def add_setter(self, setter: Setter):
        self.setters.append(setter)

    def get_user_input(self, prompt):
        result = input(prompt)
        return result






