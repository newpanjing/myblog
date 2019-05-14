(function () {
    //遮罩广告

    //JS操作cookies方法!
    //写cookies
    function setCookie(name, value) {
        var Days = 365;
        var exp = new Date();
        exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
        document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
    }

    function getCookie(name) {
        var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
        if (arr = document.cookie.match(reg))
            return unescape(arr[2]);
        else
            return null;
    }

    var dd = new Date();
    var key = ad_type + '_' + (dd.getMonth() + 1) + '' + dd.getDate();
    var value = getCookie(key);
    if (!value) {

        var eleid = '_open_ad_' + new Date().getTime()
        var html = '<div id="' + eleid + '" style="position: fixed;z-index: 9999;background: rgba(0,0,0,0.5);color: white;top:0;left:0;bottom: 0;right: 0;display: flex;align-items:center;justify-content:center">';
        html += '<img src="/static/images/ad.gif" width="300" height="300" style="vertical-align: middle"/>';
        html + '<div>123sadsdadsadsadasd</div>';
        html += '</div>';
        $(document.body).append(html);

        $("#" + eleid).click(function () {
            $(this).fadeOut();
            window.open('https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w4004-21653072801.4.2a482e31Gdv5om&id=593549043747');
        });
        setCookie(key, eleid);
    }
})();