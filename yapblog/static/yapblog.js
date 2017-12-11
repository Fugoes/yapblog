var this_page_id;

function gen_list(p, id_to_replies) {
    var pre = [
        "<li id='comment" + p + "'>",
        "   <div class='comment-author'></div>",
        "   <div class='comment-text'></div>"
    ].join("\n");
    var post = [
        "   <button onclick='create_reply_box(" + p + ")'>Reply</button>",
        "</li>"
    ].join("\n");
    if (p in id_to_replies) {
        // have replies
        var inner = "";
        for (var i in id_to_replies[p]) {
            inner += gen_list(id_to_replies[p][i], id_to_replies);
        }
        return pre + [
            "   <ul class='comment'>" + inner,
            "   </ul>"
        ].join("\n") + post;
    } else {
        return pre + post;
    }
}

function create_reply_box(comment_id) {
    $("#comment" + comment_id + " button").attr("onclick", "submit_reply(" + comment_id + ")");
    $("#comment" + comment_id).append("<textarea class='form-control' rows='5' id='comment" + comment_id + "'></textarea>");
}

function submit_reply(comment_id) {
    var button = $("#comment" + comment_id + " button");
    button.prop("disabled", true);
    var comment_text = $("#comment" + comment_id + " textarea").val();
    var data = {
        text: comment_text,
        reply_to_id: comment_id
    };
    if (comment_text.length > 0) {
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/api/page/" + this_page_id + "/comments",
            data: JSON.stringify(data),
            dataType: "json",
            success: function (data) {
                alert(data.id);
            }
        });
    } else {
        button.prop("disabled", false);
    }
}

function load_comment(comment_id) {
    var this_comment = "#comment" + comment_id;
    var comment = $.ajax({
        type: "GET",
        url: "/api/comment/" + comment_id
    });
    comment.done(function (data) {
        if (data.ok) {
            $(this_comment + " .comment-author").text(data.author_name);
            $(this_comment + " .comment-text").text(data.text);
        }
    });
}

function load_comments(page_id, comments_box) {
    this_page_id = page_id;
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
            $(comments_box).html("<ul class='comment'></ul>");
            var box = $(comments_box + " ul");
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