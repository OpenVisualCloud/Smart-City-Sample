$(document).foundation();

$(window).on("popstate", function (e) {
    console.log(e);
    selectPage1(e.originalEvent.state.page,e.originalEvent.state.options);
});

$(window).on("load", function () {
    $(window).resize();
    selectPage("home");
    $("#pg-office").trigger(":setup-alerts");
});

function selectPage1(page, options) {
    if (typeof page == "undefined") page=sessionStorage.page;
    sessionStorage.page=page;
    console.log("SELECT " + page);

    var contents=$("#ContentWindow");
    contents.children().show().not("#pg-"+page).hide().trigger(":closepage");
    contents.find("#pg-"+page).trigger(":initpage", options);
    $(window).trigger('resize');    
}

function selectPage(page, options) {
    selectPage1(page, options);
    history.pushState({page:page,options:options},page);
}
