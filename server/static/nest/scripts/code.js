$(document).ready(function() {
    
    $('code').editableDiv();
    
    function join(currentValue, index, array) {
        text += currentValue.textContent
    }

    $('input.button').on('click',function(e) {
        e.preventDefault();
        parts = getTextNodesIn(document.getElementById('editor'), true);
        text = ''
        parts.map(join);
        $('#code').val(text);
        $('.editor form').submit();
    });

    // http://stackoverflow.com/a/4399718/4855984
    function getTextNodesIn(node, includeWhitespaceNodes) {
        var textNodes = [], nonWhitespaceMatcher = /\S/;

        function getTextNodes(node) {
            if (node.nodeType == 3) {
                if (includeWhitespaceNodes || nonWhitespaceMatcher.test(node.nodeValue)) {
                    textNodes.push(node);
                }
            } else {
                for (var i = 0, len = node.childNodes.length; i < len; ++i) {
                    getTextNodes(node.childNodes[i]);
                }
            }
        }

        getTextNodes(node);
        return textNodes;
    }
});