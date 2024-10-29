// Função para obter o token CSRF do cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');  // Armazena o token CSRF para uso posterior


// Script para curtir uma coleção
let likeTimeout;
document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        // Limita a frequência dos cliques
        clearTimeout(likeTimeout);
        likeTimeout = setTimeout(() => {
            const colecaoId = this.dataset.colecaoId;

            fetch(`/like/${colecaoId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (!response.ok) throw new Error('Erro na resposta da requisição');
                return response.json();
            })
            .then(data => {
                // Atualiza o ícone e o contador de curtidas
                if (data.liked) {
                    this.classList.add('liked');
                    this.querySelector('i').classList.remove('far');
                    this.querySelector('i').classList.add('fas');
                    this.querySelector('i').style.color = '#FF0049';
                } else {
                    this.classList.remove('liked');
                    this.querySelector('i').classList.remove('fas');
                    this.querySelector('i').classList.add('far');
                    this.querySelector('i').style.color = '';
                }
                const likeCountElement = document.getElementById(`like-count-${colecaoId}`);
                if (likeCountElement) {
                    likeCountElement.innerText = `Curtidas: ${data.likes_count}`;
                }
            })
            .catch(error => console.error('Erro ao processar a requisição:', error));
        }, 300); // Delay de 300ms
    });
});


// Script para salvar uma coleção
document.querySelectorAll('.save-button').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Previne o redirecionamento padrão

        const colecaoId = this.dataset.colecaoId;

        fetch(`/salvar/${colecaoId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken, // Certifique-se de que o token CSRF está correto
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro na resposta da requisição');
            return response.json();
        })
        .then(data => {
            // Atualiza o ícone de "salvar"
            if (data.saved) {
                this.classList.add('saved');
                this.querySelector('i').classList.remove('far');
                this.querySelector('i').classList.add('fas');
                this.querySelector('i').style.color = '#000000'; // Ícone preenchido
            } else {
                this.classList.remove('saved');
                this.querySelector('i').classList.remove('fas');
                this.querySelector('i').classList.add('far');
                this.querySelector('i').style.color = ''; // Ícone contornado
            }
        })
        .catch(error => console.error('Erro ao processar a requisição:', error));
    });
});

