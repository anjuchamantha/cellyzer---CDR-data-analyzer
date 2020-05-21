const tableOffset = $("#table-1").offset().top;
const $header = $("#table-1 > thead").clone();
const $fixedHeader = $("#header-fixed").append($header);

$(window).bind("scroll", function() {
    const offset = $(this).scrollTop();

    if (offset >= tableOffset && $fixedHeader.is(":hidden")) {
        $fixedHeader.show();
    }
    else if (offset < tableOffset) {
        $fixedHeader.hide();
    }
});