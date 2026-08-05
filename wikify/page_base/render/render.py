import re
from typing import List, Callable, Dict


class Render:
    funcs: Dict[str, Callable[[List[str]], str]]
    def __init__(self):
        self.funcs = {}
        self.funcs["server"] = (lambda _: "Wikify")

    def render(self, c: str) -> str:
        r = re.sub(r"\{[^}]?\}", self.execute, c)
        return r

    def execute(self, c: str) -> str:
        return "Wikify"