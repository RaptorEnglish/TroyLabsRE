import string
import random
import math
import re


def to_lower(obj):
    """convert to lowercase so matching is easier"""
    if isinstance(obj, list):
        return [str(x).lower() for x in obj]
    elif isinstance(obj, dict):
        return {k: str(v).lower() for k, v in obj.items()}
    return str(obj).lower()


def generate_id(length=10):
    """generate an id for each record (return random)"""
    return "".join(str(random.choice(string.ascii_letters + string.digits)) for _ in range(length))


def tokenize(text):
    """tokenize input text to see how many words are shared"""
    tokens = []
    for token in str(text).split(" "):
        token = "".join(x for x in token if x in list(string.ascii_letters) + list(string.digits) + [" "])
        tokens.append(token)
    return tokens




