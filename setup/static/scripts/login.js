function MostrarSenha() {
    var senha = document.getElementById("senha");
    var olho = document.getElementById("olho");
    if (senha.type === "password") {
        senha.type = "text";
        olho.src = "static/assets/icones/1x/hide.png";
    } else {
        senha.type = "password";
        olho.src = "static/assets/icones/1x/view.png";
    }
}
