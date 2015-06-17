$(document).ready(function() {
    $('h1,h2,h3,h4,h5,h5,p,q,b,i,span,li,a').editableDiv();
    
    // Form description:
    // To edit the page's contents, click directly on the text you'd like to edit.
    // Double-click on elements to see additional options: (1) convert into a repeatable 
    // item (i.e., courses, posts, merchandise), (2) convert into a reusable template partial
    // (i.e., header, footer) or (3) edit the HTML directly.
    
    // feature disabled, maybe for future development
//    $('*').on('dblclick', function(e) {
//        $('*').blur();
//        if ($(this).css('border').lastIndexOf('0px none', 0) == 0) {
//            $(this).css('border', '1px dashed #999');
//            decrementMargins($(this), 1);
//            $(this).attr('puhjiiified', 'true');
//        }
//        e.stopPropagation();
//    })
//
//    $('*').on('blur', function(e) {
//        if ($(this).attr('puhjiiified') == 'true') {
//            incrementMargins($(this), 1);
//            $(this).css('border', '0px none rgb(255,255,255)');
//        }
//    })
    
    function crementMargins(item, func, amt) {
        func(item, 'margin-bottom', amt);
        func(item, 'margin-top', amt);
        func(item, 'margin-right', amt);
        func(item, 'margin-left', amt);
    }
    
    function decrementMargins(item) {
        crementMargins(item, decrementProp);
    }
    
    function incrementMargins(item) {
        crementMargins(item, incrementProp);
    }

    function crementProp(item, prop, func) {
        existing = item.css(prop).substr(0, -2);
        if (existing === undefined) {
            existing = 0;
        }
        func(item, prop, existing)
    }

    function decrementProp(item, prop, amt) {
        crementProp(item, prop, function(existing) {
            item.css(prop, (existing - amt)+'px');
        });
    }

    function incrementProp(item, prop, amt) {
        crementProp(item, prop, function(existing) {
            item.css(prop, (existing + amt)+'px');
        });
    }
});