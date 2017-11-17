class Page(object):
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
        pass

    class Content(object):
        pass

    def __init__(self):
        self.navbar = Page.NavBar()
