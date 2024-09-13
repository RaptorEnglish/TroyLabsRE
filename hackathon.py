import re
import time
from classes import Node, Setter
import random
import helpers
import os


def printer(node: Node):
    """print the state of the app"""
    state = node.get_state()
    selection = state["selection"]
    for record in selection:
        for k, v in record.items():
            print(f'\033[36m{k}: \033[0m{v}')
        print("-" * 50)

    print(f'SELECTION: {len(selection)} of {len(state["records"])}')


def select_record(node: Node):
    """select a record in the database"""
    key = node.get_input_var("key") or input("Type a field to search:")
    value = node.get_input_var("value")

    selection = []
    for rec in node.get_state_var("records"):
        logic = any([
            key == "all",
            str(value).lower() in helpers.to_lower(rec.get(key))
        ])

        # add to selection
        if logic:
            selection.append(rec)

    node.update_state_var({"selection": selection})


def demo_requests(node: Node):
    """initialize demo records to work with"""
    records = node.get_state_var("records")

    requests = [
        "What is your catalog of gifts to send?",
        "Can I see a list of past testimonials?",
        "Who is this product for?",
        "Is RevSend a good business?",
        "What gifts are best to send to a corporate client?",
        "How long does it take RevSend to deliver the gift?",
    ]

    requests = [{
        "id": helpers.generate_id(),
        "type": "question",
        "value": req,
        "answer": "?",
        "count": 0
    } for req in requests]

    requests[-1]["answer"] = "It takes around 2 days for the product to get delivered."

    records.extend(requests)
    node.update_state_var({"selection": [x for x in requests]})


def ask_expert(node: Node):
    """ask a question to the help desk"""
    records = node.get_state_var("records")
    question = node.get_input_var("question")

    # find similar record
    q_tokens = helpers.tokenize(question)
    counts = {}
    for rec in records:
        rec_tokens = helpers.tokenize(rec.get("value", ""))
        count = len(set(q_tokens).intersection(set(rec_tokens)))
        counts[rec["id"]] = (rec, count)

    if counts:
        max_count = max(counts.items(), key=lambda x: x[1][1])
        if max_count[1][1] > 2:
            rec = max_count[1][0]
            value = rec.get("value", "")
            os.system("clear")
            print("\033[36mFound a similar question:\033[0m")
            print(value)
            print()
            if rec.get("answer", "?") != "?":
                print("\033[35mAnswer:\033[0m")
                print(rec["answer"])
            else:
                print("\033[35mNo answer yet.\033[0m")

            cont = input("\nDo you still want to send the question (y/n)?\n--> ")
            if not re.match('y', cont, re.I):
                print("\nNot sending.")
                time.sleep(1)
                return
            else:
                print("\nSending...")
                time.sleep(1)

    question = {
        "id": helpers.generate_id(),
        "type": "question",
        "value": question,
        "answer": "?",
        "count": 0
    }

    records.append(question)
    node.update_state_var({"selection": [question]})


def rank_keywords(node: Node):
    records = node.get_state_var("records")

    keywords = {}
    for rec in records:
        for token in str(rec.get("value", "")).lower().split(" "):
            keywords.setdefault(token, 0)
            keywords[token] += 1

    # sort keywords
    keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)

    # print table with keywords
    os.system("clear")
    for k, v in keywords:
        print(f"{k}: {v}")
    input("\nHere are the most common keywords:")


def answer_question(node: Node):
    records = node.get_state_var("records")
    answer = node.get_input_var("answer")
    for rec in records:
        if "answer" in rec:
            rec["answer"] = answer


def get_help(node: Node):
    print("\n".join([
        "demo",
        "ask .+",
        "answer .+",
        "rank",
        "sel .+",
    ]))
    input("\nContinue?\n")


