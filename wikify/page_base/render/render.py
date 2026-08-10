import re
from typing import List, Callable, Dict, Optional
from . import link, header


class Render:
    funcs: Dict[str, Callable[[List[str]], str]]
    def __init__(self):
        self.funcs = {
            "server": (lambda _: "Wikify"),
            "link": link.link,
            "h1": header.h1,
            "h2": header.h2,
            "h3": header.h3,
            "h4": header.h4,
            "h5": header.h5,
            "h6": header.h6
        }

    def render(self, c: str) -> str:
        res = re.sub(r"\{(?P<content>[^}]*)}", self.execute, c)
        pattern = r'''(?mx)
        ^(?:[ \t]*$\n)? 
        (?P<paragraph>
            [^\n]+
            (?:\n(?![ \t]*$)
                [^\n]+
            )*
        )
        '''
        res = re.sub(pattern, r"<p>\g<paragraph></p>", res)
        return res

    def execute(self, c: re.Match) -> Optional[str]:
        c = c.group("content")
        res = re.match(r"^(?P<name>[^\s]+)(\s+(?P<args>.*))?$", c)
        name = res.group("name")
        l = res.group("args").split("_")
        if name in self.funcs:
            return self.funcs[name](l)
        else:
            return None

if __name__ == "__main__":
    r = Render()
    print(r.render("hello {server} {link editor.html_editor}"))