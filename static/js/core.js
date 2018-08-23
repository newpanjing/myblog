(function () {

    Toast = {
        show: function (text, timeout) {
            timeout = timeout || 2000;

            $(document.body).append("<div class='toast'>" + text + "</div>");
            target = $(".toast");
            var value = target.outerWidth() / 2;
            target.css({"margin-left": "-" + value + "px"})

            if (this.t) {
                window.clearTimeout(this.t);
            }
            target.fadeIn();
            this.t = setTimeout(function () {
                target.fadeOut(function () {
                    target.remove();
                });
            }, timeout)
        }
    }
    window.Toast = Toast;

    Date.prototype.format = function (format) {
        var o = {
            "M+": this.getMonth() + 1, //month
            "d+": this.getDate(),    //day
            "h+": this.getHours(),   //hour
            "m+": this.getMinutes(), //minute
            "s+": this.getSeconds(), //second
            "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter
            "S": this.getMilliseconds() //millisecond
        }
        if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
            (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o) if (new RegExp("(" + k + ")").test(format))
            format = format.replace(RegExp.$1,
                RegExp.$1.length == 1 ? o[k] :
                    ("00" + o[k]).substr(("" + o[k]).length));
        return format;
    }

})();