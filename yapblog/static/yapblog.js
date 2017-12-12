var this_page_id;

function gen_comment_body(comment_id) {
    return [
        "<div class='comment-body' id='comment" + comment_id + "'>",
        "   <span class='comment-author'></span> said:",
        "   <div class='comment-text'></div>",
        "   <button class='btn btn-link btn-xs' style='padding: 0px' onclick='create_reply_box(" + comment_id + ")'>",
        "       Reply",
        "   </button>",
        "</div>"
    ].join("\n");
}

function gen_list(p, id_to_replies) {
    var pre = gen_comment_body(p) + "<li class='comment-li'>";
    var post = "</li>";
    if (id_to_replies === null || !(p in id_to_replies)) {
        return pre + "<ul class='comment-ul'>" + "</ul>" + post;
    } else {
        // have replies
        var inner = "";
        for (var i in id_to_replies[p]) {
            inner += gen_list(id_to_replies[p][i], id_to_replies);
        }
        return pre + "<ul class='comment-ul'>" + inner + "</ul>" + post;
    }
}

function delete_reply_box(comment_id) {
    $("#comment" + comment_id + " textarea").remove();
    var button = $("#comment" + comment_id + " button").first();
    button.next().remove();
    button.attr("onclick", "create_reply_box(" + comment_id + ")");
    button.prop("disabled", false);
}

function create_reply_box(comment_id) {
    $("#comment" + comment_id + " button").attr("onclick", "submit_reply(" + comment_id + ")");
    $("#comment" + comment_id).append([
        "   <button class='btn btn-link btn-xs' style='padding: 0px' onclick='delete_reply_box(" + comment_id + ")'>",
        "       Cancel",
        "   </button>",
        "<textarea class='form-control' style='padding-bottom: 10px' rows='3'></textarea>"
    ].join("\n"));
}

function submit_reply(comment_id) {
    if (comment_id !== null) {
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
                    if (data.ok) {
                        delete_reply_box(comment_id);
                        var li = $("#comment" + comment_id).next();
                        li.append([
                            gen_comment_body(data.id),
                            "<li class='comment-li'>",
                            "   <ul class='comment-ul'></ul>",
                            "</li>"
                        ].join("\n"));
                        load_comment(data.id);
                        $("html, body").animate({scrollTop: $("#comment" + data.id).offset().top - $(window).height() / 3}, 1000);
                    }
                }
            });
        } else {
            button.prop("disabled", false);
        }
    } else {
        var textarea = $("#comments-root-textarea");
        var button = textarea.next();
        button.prop("disabled", true);
        var comment_text = textarea.val();
        if (comment_text.length > 0) {
            var data = {
                text: comment_text,
                reply_to_id: null
            };
            $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                url: "/api/page/" + this_page_id + "/comments",
                data: JSON.stringify(data),
                dataType: "json",
                success: function (data) {
                    if (data.ok) {
                        $("#comments").first().append(gen_list(data.id, null));
                        load_comment(data.id);
                        button.prop("disabled", false);
                        $("html, body").animate({scrollTop: $("#comment" + data.id).offset().top - $(window).height() / 3}, 1000);
                    }
                }
            });
        } else {
            button.prop("disabled", false);
        }
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
            $(comments_box).html("<ul class='comment-ul'></ul>");
            var box = $(comments_box + " ul");
            for (var i in roots) {
                var t = gen_list(roots[i], id_to_replies);
                box.append(t);
            }
            for (var i in comments) {
                load_comment(comments[i].id);
            }
        }
    });
}