$(document).ready(function() {

    original = $('#html').val();

    function iframe() {
        content = $('iframe').contents();
        content.find('*').blur();
        return content.find('html');
    }

    function html() {
        strip();
        raw = '<html>'+iframe().html()+'</html>'; // get HTML
        reduced = raw.replace('<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>\n' +
                                    '<script src="/static/libraries/editablediv/jquery.editablediv.js"></script>\n'+
                                    '<script src="/static/nest/scripts/interactive.js"></script>', '') // remove added wrapper scripts
        return reduced
    }
    
    function strip() {
        var contents = ['style', 'link', 'script']
        
        for (var i = 0;i<contents.length;i++) {
            iframe().find(contents[i]).each(function() {
                substr = htmlify($(this));
                if (original.indexOf(substr) <= -1) {
                    $(this).remove();
                }
            });
        }
    }
    
    function htmlify(tag) {
        return tag.clone().wrap('<span>').parent().html();
    }
    
    $('.nest-bar input').on('click', function(e) {
        e.preventDefault();
        html = html();
        $('#html').val(html);
        $('.iedit form').submit();
    });
});