var getDefaultBg = $(".body").css("background");
$(".body").mouseover(function() {
    $(this).css("background", "#e4764c");
}). mouseout(function() {
    $(this).css("background", getDefaultBg);
});