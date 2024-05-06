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


$(".follow-button").click(function() {
    var usuario_id = $(this).data("id"); // Obtenha o ID do usuário do atributo data-id do botão
    $.ajax({
        url: '/seguir_usuario/' + usuario_id, // Substitua por sua URL correta
        type: 'POST',
        success: function(response) {
            // Atualize o botão ou qualquer outro elemento da página aqui
            $(this).text('Seguindo');
        }
    });
});

$(".unfollow-button").click(function() {
    var usuario_id = $(this).data("id"); // Obtenha o ID do usuário do atributo data-id do botão
    $.ajax({
        url: '/deixar_seguir_usuario/' + usuario_id, // Substitua por sua URL correta
        type: 'POST',
        success: function(response) {
            // Atualize o botão ou qualquer outro elemento da página aqui
            $(this).text('Seguir');
        }
    });
});
