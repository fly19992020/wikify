import re
from typing import List, Callable, Dict, Optional
from ..page_base import Page


class Render:
    title: bool
    funcs: Dict[str, Callable[[List[str], Render], str]]
    def __init__(self):
        from . import link, header, notitle
        self.funcs = {
            "server": (lambda _, __: "Wikify"),
            "link": link.link,
            "h1": header.h1,
            "h2": header.h2,
            "h3": header.h3,
            "h4": header.h4,
            "h5": header.h5,
            "h6": header.h6,
            "notitle": notitle.notitle
        }

    def render(self, c: str) -> Page:
        self.title = True
        res = re.sub(r"\{(?P<content>[^}]*)}", self.execute, c)
        pattern = r'''(?mx)
        ^(?:[ \t]*$\n)? 
        (?P<paragraph>
            (?!<h[1-6]>.*</h[1-6]>)
            [^\n]+
            (?:\n(?![ \t]*$)
                [^\n]+
            )*
        )
        '''
        res = re.sub(pattern, r"<p>\g<paragraph></p>", res)
        return Page(res, title=self.title)

    def execute(self, c: re.Match) -> Optional[str]:
        c = c.group("content")
        res = re.match(r"^(?P<name>[^\s]+)(\s+(?P<args>.*))?$", c)
        name = res.group("name")
        l = str(res.group("args")).split("_")
        if name in self.funcs:
            return self.funcs[name](l, self)
        else:
            return None

if __name__ == "__main__":
    r = Render()
    print(r.render("hello {server} {link editor.html_editor}"))