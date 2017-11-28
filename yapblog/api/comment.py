from yapblog import app


@app.route("/api/comment/<int:page_id>/", methods=["GET"])
def api_comment_page_id(page_id):
    pass
