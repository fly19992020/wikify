from typing import List

from wikify.page_base.render.render import Render


def h1(l: List[str], _: Render) -> str:
    if len(l) == 1:
        return "<h1>{header}</h1>".format(header=l[0])
    else:
        return ""

def h2(l: List[str], _: Render) -> str:
    if len(l) == 1:
        return "<h2>{header}</h2>".format(header=l[0])
    else:
        return ""

def h3(l: List[str], _: Render) -> str:
    if len(l) == 1:
        return "<h3>{header}</h3>".format(header=l[0])
    else:
        return ""

def h4(l: List[str], _: Render) -> str:
    if len(l) == 1:
        return "<h4>{header}</h4>".format(header=l[0])
    else:
        return ""

def h5(l: List[str], _: Render) -> str:
    if len(l) == 1:
        return "<h5>{header}</h5>".format(header=l[0])
    else:
        return ""

def h6(l: List[str], _: Render) -> str:
    if len(l) == 1:
        return "<h6>{header}</h6>".format(header=l[0])
    else:
        return ""