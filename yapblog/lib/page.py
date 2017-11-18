class NavBar(object):
    class Item(object):
        def __init__(self, **kwargs):
            self.is_active = kwargs["is_active"]
            self.link = kwargs["link"]
            self.text = kwargs["text"]

    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.items = kwargs["items"]


class SideBar(object):
    class CollapsibleList(object):
        class Item(object):
            def __init__(self, **kwargs):
                self.link = kwargs["link"]
                self.text = kwargs["text"]

        def __init__(self, **kwargs):
            self.id = kwargs["id"]
            self.title = kwargs["title"]
            self.items = kwargs["items"]
            self.template = "element/collapsible_list.html"

    def __init__(self, **kwargs):
        self.items = kwargs["items"]
