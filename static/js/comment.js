$(function () {

    function saveComment(val, cb, parentId, atMemberId) {

        if (!window.MEMBER) {
            document.getElementById('comment-link').click();
            return;
        }

        if (val.replace(/ /g, "").length == 0) {
            return Toast.show("请输入评论内容")
        }

        var params = {
            SID: _PAGE_CONFIG.SID,
            TARGET_ID: _PAGE_CONFIG.TARGET_ID,
            content: val,
            parentId: parentId,
            atMemberId: atMemberId,
            type: _PAGE_CONFIG.TYPE
        };
        //提交
        $.post("/comment/post", params, function (json) {
            if (json.code == 1) {
                //追加内容到div
                obj = {id: json.id}
                obj.name = MEMBER.name;
                obj.avatar = MEMBER.avatar;
                obj.url = MEMBER.url;
                var content = val;
                dict = {
                    '<': '&lt;',
                    '>': '&gt;',
                    "'": '&#39;',
                    '"': '&quot;'
                }
                for (var i in dict) {
                    content = content.replace(new RegExp(i, 'gm'), dict[i]);
                }
                obj.content = content;
                obj.date = new Date().format('yyyy-MM-dd hh:mm:ss');
                //更新数量到页面
                var people = parseInt($(".comment-count .people").text());
                var count = parseInt($(".comment-count .count").text());
                people += 1;
                count += 1;
                if (!parentId) {
                    $(".comment-count .people").text(people);
                }
                $(".comment-count .count").text(count);
                cb(obj, json);
            }
            Toast.show(json.msg);
        });
    }

    $(".comment-box .post").click(function () {

        postComment();
    });

    function postComment() {
        var val = $(".comment-input").val();
        if (val.replace(/ /g, "").length == 0) {
            return Toast.show("请输入要评论的内容！");
        }
        saveComment(val, function (obj, json) {
            $(".tips").remove();
            $(".comment-list").prepend(render(obj));
            bindBtnClick();
            $(".comment-input").val('');
        });

    }

    function render(obj) {
        var html = '<div class="item">\n' +
            '                    <div class="avatar">\n' +
            '                        <img src="' + obj.avatar + '"/>\n' +
            '                    </div>\n' +
            '                    <div class="body">\n' +
            '                        <div class="name">\n' +
            '                            <a href="' + obj.url + '" target="_blank">' + obj.name + '</a>\n' +
            '                        </div>\n' +
            '                        <div class="text">' + obj.content + '</div>\n' +
            '                        <div class="clearfix">\n' +
            '                            <div class="float-left date">' + obj.date + '</div>\n' +
            '                            <div class="float-right reply">\n' +
            '                                <a href="javascript:;" class="reply-btn" parentId="' + obj.id + '">回复</a>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '<div class="reply-list"><div class="items"></div></div>\n' +
            '                    </div>\n' +
            '                </div>';
        return html;
    }

    function bindBtnClick() {


        $(".reply-btn").unbind('click');
        $(".reply-btn").bind('click', function () {

            var parent = $(this).parent().parent().parent();
            var parentId = $(this).attr("parentId");

            if (parent.find(".reply-top").length > 0) {

                var display = parent.find(".reply-top").css("display")
                if (display == "none") {
                    display = "table";
                } else {
                    display = "none";
                }
                parent.find(".reply-top").css("display", display);

            } else {
                var name = parent.find(".name").text().replace(/ /g, "");

                var html = ' <div class="reply-input reply-top">\n' +
                    '<div class="input"><input type="text" class="form-control" placeholder="回复@' + name + '："/></div>\n' +
                    '<div class="action"><a class="btn btn-success" onclick="replyComment(this)" href="javascript:;" parentId="' + parentId + '">评论</a></div>\n' +
                    '</div>';

                parent.find(".reply-list").prepend(html);
            }
        });
    }

    bindBtnClick();

    window.replyComment = function (obj) {
        var parent = $(obj).parent().parent();
        var input = parent.find(".input").find("input");
        var val = input.val();
        var parentId = $(obj).attr('parentId');

        saveComment(val, function (obj, json) {

            input.val('');
            var html = '<div class="item">\n' +
                '<a class="sub-name" href="' + obj.url + '" target="_blank">\n' +
                '<img class="comment-avatar" src="' + obj.avatar + '"/>\n' +
                '<span>' + obj.name + '</span>\n' +
                '</a><span>:</span>\n' +
                '<span>' + obj.content + '</span>\n' +
                ' <div class="clearfix reply-comment-box">\n' +
                '<div class="float-left date">' + obj.date + '</div>\n' +
                '<div class="float-right reply">\n' +
                '<a href="javascript:;" onclick="atComment(this)" memberId="' + MEMBER.id + '" parentid="' + parentId + '">回复</a>\n' +
                '</div>\n' +
                '</div>' +
                '</div>';

            parent.parent().find(".items").prepend(html);
        }, parentId)
    }

    window.atComment = function (obj) {
        var memberId = $(obj).attr("memberId");
        var parentId = $(obj).attr("parentId");
        var parent = $(obj).parent().parent();
        var name = parent.parent().find(".sub-name").text().replace(/ /g, "");


        if (parent.find(".reply-input").length > 0) {

            var display = parent.find(".reply-input").css("display")
            if (display == "none") {
                display = "table";
            } else {
                display = "none";
            }
            parent.find(".reply-input").css("display", display);

        } else {

            var html = ' <div class="reply-input">\n' +
                '<div class="input"><input type="text" class="form-control" placeholder="回复@' + name + '："/></div>\n' +
                '<div class="action"><a class="btn btn-success" onclick="atCommentSave(this)" memberId="' + memberId + '" href="javascript:;" parentId="' + parentId + '">评论</a></div>\n' +
                '</div>';
            parent.append(html)
        }
    }

    window.atCommentSave = function (obj) {
        var memberId = $(obj).attr("memberId");
        var parentId = $(obj).attr("parentId");
        var parent = $(obj).parent().parent();
        var input = parent.find("input");
        var name = parent.parent().parent().find(".sub-name").text().replace(/ /g, "");
        saveComment(input.val(), function (obj, json) {
            input.val("");
            var html = '<div class="item">\n' +
                '<a class="sub-name" href="' + obj.url + '" target="_blank">\n' +
                '<img class="comment-avatar" src="' + obj.avatar + '"/>\n' +
                '<span>' + obj.name + '</span>\n' +
                '</a><span>:</span>\n' +
                '回复@' + name + ':<span>' + obj.content + '</span>\n' +
                ' <div class="clearfix reply-comment-box">\n' +
                '<div class="float-left date">' + obj.date + '</div>\n' +
                '<div class="float-right reply">\n' +
                '<a href="javascript:;" onclick="atComment(this)" memberId="' + MEMBER.id + '" parentid="' + parentId + '">回复</a>\n' +
                '</div>\n' +
                '</div>' +
                '</div>';
            parent.parent().parent().parent().prepend(html);
        }, parentId, memberId)
    }

});