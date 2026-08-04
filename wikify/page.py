class PageProvider:
    def __init__(self):
        pass

    def get_page(self, page_name: str):
        try:
            f = open(page_name)
        except:
            return "Page not found"
        return f.read()
