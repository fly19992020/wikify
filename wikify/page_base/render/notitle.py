from typing import List

from wikify.page_base.render.render import Render


def notitle(_: List[str], r: Render) -> str:
    r.title = False
    return ""