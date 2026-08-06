import re
from typing import List, Callable, Dict, Optional
from . import link


class Render:
    funcs: Dict[str, Callable[[List[str]], str]]
    def __init__(self):
        self.funcs = {
            "server": (lambda _: "Wikify"),
            "link": link.link
        }

    def render(self, c: str) -> str:
        res = re.sub(r"\{(?P<content>[^}]*)}", self.execute, c)
        return res

    def execute(self, c: re.Match) -> Optional[str]:
        c = c.group("content")
        l = c.split()
        name = l[0]
        if name in self.funcs:
            l.pop(0)
            return self.funcs[name](l)
        else:
            return None

if __name__ == "__main__":
    r = Render()
    print(r.render("hello {server} {link editor.html editor}"))