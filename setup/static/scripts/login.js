function MostrarSenha() {
    var senha = document.getElementById("senha");
    var olho = document.getElementById("olho");
    if (senha.type === "password") {
        senha.type = "text";
        olho.src = "static/assets/icones/hide.png";
    } else {
        senha.type = "password";
        olho.src = "static/assets/icones/view.png";
    }
}

document.querySelectorAll('.icone').forEach(icone => {
    icone.style.left = Math.random() * document.querySelector('.chuva-icones').offsetWidth + 'px';
    icone.style.animationDuration = Math.random() * 2 + 3 + 's'; // Entre 3 e 5 segundos
});

// Número de cópias que você quer criar de cada ícone
var numCopias = 4;

// Seleciona todos os ícones
var icones = document.querySelectorAll('.icone');

// Para cada ícone
icones.forEach(icone => {
    // Cria as cópias
    for (var i = 0; i < numCopias; i++) {
        // Cria uma nova cópia do ícone
        var novaIcone = icone.cloneNode(true);

        // Define uma posição inicial aleatória e uma velocidade de queda aleatória
        novaIcone.style.left = Math.random() * document.querySelector('.chuva-icones').offsetWidth + 'px';
        novaIcone.style.animationDuration = Math.random() * 2 + 1 + 's'; // Entre 1 e 3 segundos

        // Adiciona a nova ícone ao contêiner
        document.querySelector('.chuva-icones').appendChild(novaIcone);
    }
});