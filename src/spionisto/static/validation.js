function parseURI (url) {
    var a, k = 'protocol hostname host pathname port search hash href'.split(' ');
    a || (a = document.createElement('a'));
    // Let browser do the work
    a.href = url;
    for (var r = {}, i = 0; i<8; i++) {
        r[k[i]] = a[k[i]];
    }
    r.toString = function() { return a.href; };
    r.requestUri = r.pathname + r.search;
    return r;
};

$(document).ready(function (){
    'use strict';
    var hostname = $('input#form\\.hostname');
    var hostname_widget = hostname.closest('.control-group');
    hostname_widget.hide();
    hostname.val('localhost');

    //Some help for lazy copy&paste
    hostname.blur(function() {
        this.value = parseURI(this.value).hostname;
    });

    $('select#form\\.camera_model').change(function(){
        if ($(this).val() === 'Dummy (GStreamer)'){
            hostname.val('localhost');
            hostname_widget.hide();
        } else { 
            hostname.val('');
            hostname_widget.show();
        }
    });
});