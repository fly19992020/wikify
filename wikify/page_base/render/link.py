from typing import List


def link(l: List[str]) -> str:
    if len(l) == 1:
        return "<a href=\"{link}\">{link}</ a>".format(link=l[0])
    elif len(l) == 2:
        return "<a href=\"{link}\">{name}</ a>".format(link=l[0], name=l[1])
    else:
        return ""