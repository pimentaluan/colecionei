document.addEventListener('DOMContentLoaded', function() {
    var clickableElements = document.querySelectorAll('.clicavel');

    clickableElements.forEach(function(element) {
        element.addEventListener('click', function() {
            window.location = this.getAttribute('data-url');
        });
    });

    var stopPropagationElements = document.querySelectorAll('.stop-propagation');

    stopPropagationElements.forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    });
});