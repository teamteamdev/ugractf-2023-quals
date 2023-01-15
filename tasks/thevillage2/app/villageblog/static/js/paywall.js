$(document).ready(function() {
    function protect() {
        $('.pw').css("max-height", '80vh');
        $('.pw').css("filter", 'blur(1.5rem)');
    }

    $.get('/' + base_url + '/tr/' + postid, function(data) {
        $('#paywall').before('<div class="pw"></div>');
        $('.pw').html(decodeURIComponent(atob(data.data).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join('')));
        setInterval(protect, 1000);
    });

        $(".modal__close").on("click", function() {
                $(".modal-overlay").removeClass("modal-overlay_visible");
            });
                 
            $(document).on("click", function(e) {
                if(!$(e.target).closest(".modal").length && !$(e.target).closest(".modal-link").length) {
                    $(".modal-overlay").removeClass("modal-overlay_visible");
                }
            });
});

var x = true;
document.onscroll = function() {
    if ($(window).scrollTop() >= 600 && x) {
        x = false;
        $('body').css('overflow', 'hidden');
        $('body').css('height', '100%');
        $('.modal-overlay').addClass("modal-overlay_visible");
    }
}
