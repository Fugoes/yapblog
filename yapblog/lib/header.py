class Header(object):
    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.name = kwargs["name"]
        self.items = kwargs["items"]
