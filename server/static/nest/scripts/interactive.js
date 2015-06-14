$(document).ready(function() {
    $('h1,h2,h3,h4,h5,h5,p,q,b,i,span,li,a').editableDiv();
    
    $('.nest-bar input').on('click', function(e) {
    alert('YO');
        e.preventDefault();
        html = $('iframe').html();
        console.log(html)
        //$('.iedit form').submit();
    });
});