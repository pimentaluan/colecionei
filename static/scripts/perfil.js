document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('icone-menu').addEventListener('click', function() {
        var cabecalho = document.getElementById('cabecalho');
        cabecalho.classList.toggle('cabecalho-escondido');
    });
});