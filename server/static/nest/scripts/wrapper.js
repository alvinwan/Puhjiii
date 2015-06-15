$(document).ready(function() {

    original = $('#html').val();

    function iframe() {
        return $('iframe').contents().find('html');
    }

    function html() {
        strip();
        raw = '<html>'+iframe().html()+'</html>'; // get HTML
        reduced = raw.replace(/\s{0,}contenteditable="\S+" len="\S+" stage="\S+"\s{0,}/g, ""); // remove editable attributes
        reduced = reduced.replace('<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>\n' +
                                    '<script src="/static/libraries/editablediv/jquery.editablediv.js"></script>\n'+
                                    '<script src="/static/nest/scripts/interactive.js"></script>', '') // remove added wrapper scripts
        cleaned = reduced.replace(/>\n{2,}</g, '>\n<') // remove repeated line breaks
        return cleaned
    }
    
    function strip() {
        var contents = ['style']
        
        for (var i = 0;i<contents.length;i++) {
            console.log(contents[i]);
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