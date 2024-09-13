from classes import Node, Setter
import copy
import hackathon
import re


def create_app():
    node = Node()

    # set state
    node.set_state({
        "records": [],
        "selection": [],
    })

    # set printer
    node.set_printer(hackathon.printer)

    # create setters
    node.add_setter(Setter(hackathon.select_record, 'sel(\\s+(?P<key>\\S+))?(\\s+(?P<value>.+))?'))
    node.add_setter(Setter(hackathon.demo_requests, '^demo$'))
    node.add_setter(Setter(hackathon.ask_expert, '^ask(\\s+(?P<question>.+))$'))
    node.add_setter(Setter(hackathon.rank_keywords, '^rank$'))
    node.add_setter(Setter(hackathon.answer_question, '^answer(\\s+(?P<answer>.+))$'))
    node.add_setter(Setter(hackathon.get_help, '^help$'))

    return node


def main():
    node = create_app()

    # main loop
    while True:
        node.print_state()
        uin = node.get_user_input("\nType Command:\n--> ")

        # quit from loop
        if uin == "!quit":
            break

        # use the function to execute a function
        node.execute_input(uin)


main()




