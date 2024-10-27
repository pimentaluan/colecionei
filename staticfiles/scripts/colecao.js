var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        })


//mais... biografia
$(document).ready(function(){
    $("#moreLink").click(function(e){
        e.preventDefault();
        var $moreText = $("#moreText");
        var $ellipsis = $("#ellipsis");
        if ($moreText.is(":visible")) {
            $moreText.hide();
            $ellipsis.show();
            $(this).show();
        } else {
            $moreText.show();
            $ellipsis.hide();
            $(this).hide();
        }
    });
});