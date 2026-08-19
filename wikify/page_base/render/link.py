import re
from typing import List

from wikify.page_base.render.render import Render


def link(l: List[str], _: Render) -> str:
    if len(l) == 1:
        if re.match(r"javascript:.*", l[0]):
            l[0] = ""
        return "<a href=\"{link}\">{link}</a>".format(link=l[0])
    elif len(l) == 2:
        if re.match(r"javascript:.*", l[0]):
            l[0] = ""
        return "<a href=\"{link}\">{name}</a>".format(link=l[0], name=l[1])
    else:
        return ""