from flask_login import current_user
from itertools import groupby
from copy import deepcopy
from yapblog import config
from yapblog.models import Tag, Article, Category


class NavBar(object):
    class Item(object):
        def __init__(self, **kwargs):
            self.is_active = kwargs["is_active"]
            self.link = kwargs["link"]
            self.text = kwargs["text"]

    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.left_items = kwargs["left_items"]
        self.right_items = kwargs["right_items"]


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
            self.id = kwargs["id"]
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


navbar_anonymous = NavBar(
    title=config.WEBSITE_NAME,
    left_items=[
        NavBar.Item(is_active=False, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/tags", text="Tags"),
        NavBar.Item(is_active=False, link="/categories", text="Categories"),
        NavBar.Item(is_active=False, link="/archives", text="Archives"),
    ],
    right_items=[
        NavBar.Item(is_active=False, link="/login", text="Login"),
        NavBar.Item(is_active=False, link="/register", text="Register"),
    ],
)

navbar_user = NavBar(
    title=config.WEBSITE_NAME,
    left_items=[
        NavBar.Item(is_active=False, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/tags", text="Tags"),
        NavBar.Item(is_active=False, link="/categories", text="Categories"),
        NavBar.Item(is_active=False, link="/archives", text="Archives"),
    ],
    right_items=[
        NavBar.Item(is_active=False, link="/logout", text="Logout"),
    ],
)

navbar_admin = NavBar(
    title=config.WEBSITE_NAME,
    left_items=[
        NavBar.Item(is_active=False, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/tags", text="Tags"),
        NavBar.Item(is_active=False, link="/categories", text="Categories"),
        NavBar.Item(is_active=False, link="/archives", text="Archives"),
        NavBar.Item(is_active=False, link="/admin", text="Admin"),
    ],
    right_items=[
        NavBar.Item(is_active=False, link="/logout", text="Logout"),
    ],
)


def get_navbar(active):
    if current_user.is_anonymous:
        navbar = navbar_anonymous
    else:
        if current_user.is_admin_:
            navbar = navbar_admin
        else:
            navbar = navbar_user
    navbar = deepcopy(navbar)
    for item in navbar.left_items:
        item.is_active = item.text == active
    for item in navbar.right_items:
        item.is_active = item.text == active
    return navbar


def archives_data():
    for (year, month), group in groupby(Article.query.order_by(Article.date_time_).all(),
                                        lambda x: (x.date_time_.year, x.date_time_.month)):
        yield (year, month), group


def get_archives():
    items = []
    for (year, month), group in archives_data():
        count = len(list(group))
        items.append(SideBar.CollapsibleList.Item(link="/archives/%04d/%02d" % (year, month),
                                                  text="%04d-%02d (%d)" % (year, month, count)))
    return SideBar.CollapsibleList(id="archives",
                                   title="Archives",
                                   items=items)


def get_categories():
    items = []
    for category in Category.query.all():
        name = category.name_
        articles = category.articles
        count = len(articles)
        if count > 0:
            items.append(SideBar.CollapsibleList.Item(link="/categories/%s" % name,
                                                      text="%s (%d)" % (name, count)))
    return SideBar.CollapsibleList(id="categories",
                                   title="Categories",
                                   items=items)
