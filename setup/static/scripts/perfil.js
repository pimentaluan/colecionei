function copiarLink() {
    var dummy = document.createElement('input'),
    text = window.location.href;

    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);

    var linkElement = document.querySelector('#compartilhar_perfil');
    linkElement.style.backgroundColor = '#004FFF';
    linkElement.style.transition = 'background-color 0.3s';

    var linkElementtext = document.querySelector('#compartilhar_perfil a');
    linkElementtext.innerHTML = 'Link copiado!';

    setTimeout(function() {
        linkElement.style.backgroundColor = '';
        linkElementtext.innerHTML = 'Compartilhar perfil';
    }, 4000);
}

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
    var usuario_id = $(this).attr("data-id"); // Obtenha o ID do usuário do atributo data-id do botão
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
    var usuario_id = $(this).attr("data-id"); // Obtenha o ID do usuário do atributo data-id do botão
    $.ajax({
        url: '/deixar_seguir_usuario/' + usuario_id, // Substitua por sua URL correta
        type: 'POST',
        success: function(response) {
            // Atualize o botão ou qualquer outro elemento da página aqui
            $(this).text('Seguir');
        }
    });
});


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