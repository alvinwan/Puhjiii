$(document).ready(function() {
    var animating = false;
    $(window).on("scroll",function() {
        var scroll = $(window).scrollTop();
        if (scroll > 250) {
            $('header.main').addClass('s');
        } else {
            $('header.main').removeClass('s');
        }
        if (!animating) {
            $('.main li a').each(function() {
                var target = $(this).attr('href');
                if (target.split()[0] == '#') {
                    if (scroll > yOf(target)-50) {
                        select(this);
                    }
                }
            })
        }
    });
    $('.glider').on('click',function(e) {
        e.preventDefault();
        var target = $(this).attr('href');
        select('a[href="'+target+'"]')
        animating = true;
        $('html, body').animate({
            scrollTop: yOf(target)
        }, 1000);
        setTimeout(function() { animating = false; }, 1000);
    })
    function yOf(id) {
        return $(id).offset().top;
    }
    
    function select(id) {
        $('.main a').removeClass('s');
        $(id).addClass('s');
    }
});