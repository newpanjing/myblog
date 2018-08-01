(function () {

    $(window).resize(function () {
        initLayout();
    });
    $(window).ready(function () {
        initLayout();
    });

    function initLayout() {
        var leftWidth = $(".profile").outerWidth() + $(".archive").outerWidth();
        var size = getSize();
        var value = size.width - leftWidth;
        $(".content").css({
            width: value
        })
    }

    function getSize() {
        return {
            width: document.body.offsetWidth,
            height: document.body.offsetHeight
        };
    }


})();