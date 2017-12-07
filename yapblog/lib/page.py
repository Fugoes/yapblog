from yapblog.models import Tag


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

    class TagList(object):
        class Item(object):
            def __init__(self, **kwargs):
                self.link = kwargs["link"]
                self.text = kwargs["text"]
                self.count = kwargs["count"]

        def __init__(self, **kwargs):
            self.title = kwargs["title"]
            self.items = kwargs["items"]
            self.template = "element/tag_list.html"

    def __init__(self, **kwargs):
        self.items = kwargs["items"]

    @staticmethod
    def gen_tag_list():
        tags = Tag.query.all()
        items = []
        for tag in tags:
            count = len(tag.articles)
            if count > 0:
                if count > 8:
                    count = "max"
                items.append(SideBar.TagList.Item(link="/tags/%s" % tag.name_,
                                                  text=tag.name_,
                                                  count=count))
        return SideBar.TagList(
            id="tags",
            title="Tags",
            items=items
        )
