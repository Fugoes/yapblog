__all__ = ["index"]

from flask import render_template, Markup
from yapblog import app, config
from yapblog.models import Article
from yapblog.lib.page import NavBar, SideBar

navbar = NavBar(
    title=config.WEBSITE_NAME,
    items=[
        NavBar.Item(is_active=True, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/about", text="About")
    ]
)

sidebar = SideBar(items=[
    SideBar.TagList(
        id="tags",
        title="Tags",
        items=[
            SideBar.CollapsibleList.Item(link="/tags/CS", text="CS"),
            SideBar.CollapsibleList.Item(link="/tags/EE", text="EE"),
        ],
    ),
])


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title=config.WEBSITE_NAME,
        navbar=navbar,
        sidebar=sidebar
    )


@app.route("/<int:year>/<int:month>/<string:title>", methods=["GET"])
def article_year_month_title(year, month, title):
    article = Article.query.filter_by(title_=title).first()
    if article is not None:
        date = article.date_time_
        if date.year == year and date.month == month:
            return render_template("article.html",
                                   title=title,
                                   html_content=Markup(article.html_content_),
                                   navbar=navbar,
                                   sidebar=sidebar)
