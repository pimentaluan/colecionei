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

var numCopias = 4;

var icones = document.querySelectorAll('.icone');

icones.forEach(icone => {
    for (var i = 0; i < numCopias; i++) {
        var novaIcone = icone.cloneNode(true);

        novaIcone.style.left = Math.random() * document.querySelector('.chuva-icones').offsetWidth + 'px';
        novaIcone.style.animationDuration = Math.random() * 6 + 2 + 's';

        document.querySelector('.chuva-icones').appendChild(novaIcone);
    }
});

function atualizarPosicaoIcones() {
    document.querySelectorAll('.icone').forEach(icone => {
        icone.style.left = Math.random() * document.querySelector('.chuva-icones').offsetWidth + 'px';
    });
}

window.addEventListener('resize', atualizarPosicaoIcones);

// Chame a função uma vez para definir a posição inicial dos ícones
atualizarPosicaoIcones();

var iconeAtualmenteMovendo = null;

document.querySelectorAll('.icone').forEach(icone => {
    icone.addEventListener('mousedown', function (event) {
        iconeAtualmenteMovendo = this;
        this.style.animationPlayState = 'paused';
    });

    icone.addEventListener('mouseup', function () {
        this.style.animationPlayState = 'running';
        iconeAtualmenteMovendo = null;
    });
});
