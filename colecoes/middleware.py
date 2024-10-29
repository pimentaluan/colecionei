class LastVisitedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Cada caminho tem uma barra inicial para comparação exata com `current_path`
        self.ignore_paths = [
            '/seguir/',
            '/deixar_seguir_usuario/',
            '/like/',
            '/salvar/',
            '/comentar/',
            '/nova-colecao/',
            '/novo-item/',
            '/editar-perfil/',
            '/pagina_anterior/',
            '/favicon.ico'
        ]

    def __call__(self, request):
        current_path = request.path  # Exemplo: '/seguir/usuario/'
        navigation_history = request.session.get('navigation_history', [])

        # Ignora requisições que não são `GET` ou que correspondem aos paths a serem ignorados
        if request.method == 'GET' and not any(current_path.startswith(path) for path in self.ignore_paths):
            # Adiciona ao histórico se não for o último visitado
            if not navigation_history or navigation_history[-1] != current_path:
                navigation_history.append(current_path)

            # Limita o histórico ao tamanho desejado
            if len(navigation_history) > 10:
                navigation_history.pop(0)

            # Armazena o histórico na sessão
            request.session['navigation_history'] = navigation_history

        # Processa a resposta
        response = self.get_response(request)
        return response
