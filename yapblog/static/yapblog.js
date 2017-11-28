function gen_list(p, id_to_replies) {
    if (p in id_to_replies) {
        // have replies
        var result = "<li id='comment" + p + "'><span></span><ul>";
        for (var i in id_to_replies[p]) {
            result += gen_list(id_to_replies[p][i], id_to_replies);
        }
        result += "</ul></li>";
        return result;
    } else {
        return "<li id='comment" + p + "'><span></span></li>";
    }
}

function load_comment(comment_id) {
    var comment = $.ajax({
        type: "GET",
        url: "/api/comment/" + comment_id
    });
    comment.done(function (data) {
        if (data.ok) {
            $("#comment" + comment_id + " span").text(data.text);
        }
    });
}

function load_comments(page_id, comments_box) {
    var box = $(comments_box);
    var comments_meta = $.ajax({
        type: "GET",
        url: "/api/page/" + page_id + "/comments"
    });
    comments_meta.done(function (data) {
        var roots = [];
        var id_to_replies = [];
        if (data.ok) {
            var comments = data.comments;
            for (var i in comments) {
                var comment = comments[i];
                if (comment.reply_to_id === null) {
                    roots.push(comment.id);
                } else {
                    if (!(comment.reply_to_id in id_to_replies)) {
                        id_to_replies[comment.reply_to_id] = [];
                        id_to_replies[comment.reply_to_id].push(comment.id);
                    } else {
                        id_to_replies[comment.reply_to_id].push(comment.id);
                    }
                }
            }
            for (var i in roots) {
                var t = gen_list(roots[i], id_to_replies);
                box.append(t);
            }
            for (var i in comments) {
                load_comment(comments[i].id);
            }
        } else {
        }
    });
}