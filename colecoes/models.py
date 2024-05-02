from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from colorfield.fields import ColorField
from usuarios.models import Usuario

class Categoria(models.Model):
    CATEGORIAS_OPCOES = [
        ('Livros', 'Livros'),
        ('Filmes', 'Filmes'),
        ('Músicas', 'Músicas'),
        ('Jogos', 'Jogos'),
        ('Selos', 'Selos'),
        ('Moedas', 'Moedas'),
        ('Quadrinhos', 'Quadrinhos'),
        ('Carros', 'Carros'),
        ('Vinhos', 'Vinhos'),
        ('Cartas', 'Cartas'),
        ('Miniaturas', 'Miniaturas'),
        ('Brinquedos', 'Brinquedos'),
        ('Antiguidades', 'Antiguidades'),
        ('Relógios', 'Relógios'),
        ('Jóias', 'Jóias'),
        ('Instrumentos Musicais', 'Instrumentos Musicais'),
        ('Artes', 'Artes'),
        ('Itens Esportivos', 'Itens Esportivos'),
        ('Eletrônicos', 'Eletrônicos'),
        ('Vestuário', 'Vestuário'),
        ('Acessórios', 'Acessórios'),
        ('Cosméticos', 'Cosméticos'),
        ('Utensílios Domésticos', 'Utensílios Domésticos'),
        ('Decoração', 'Decoração'),
        ('Móveis', 'Móveis'),
        ('Eletrodomésticos', 'Eletrodomésticos'),
        ('Ferramentas', 'Ferramentas'),
        ('Brindes', 'Brindes'),
        ('Peças Religiosas', 'Peças Religiosas'),
        ('Charutos', 'Charutos'),
        ('Chaveiros', 'Chaveiros'),
        ('Pedras Preciosas', 'Pedras Preciosas'),
        ('Plantas', 'Plantas'),
        ('Artefatos Históricos', 'Artefatos Históricos'),
        ('Culinária', 'Culinária'),
        ('Outros', 'Outros'),
    ]
    nome = models.CharField(max_length=100, choices=CATEGORIAS_OPCOES)
    imagem_padrao = models.ImageField(upload_to='imagens_categorias/', blank=True, null=True)

    def __str__(self):
        return self.nome
COLOR_CHOICES = [
    ('#FFCA2C', 'Amarelo Claro'),
    ('#D9C95B', 'Amarelo Escuro'),
    ('#D9AA5B', 'Laranja Claro'),
    ('#D9D2A3', 'Areia'),
    ('#004FFF', 'Azul Marinho'),
    ('#5300FF', 'Roxo'),
    ('#5B5BD9', 'Lilás'),
    ('#5BABD9', 'Azul Claro'),
    ('#8F00DB', 'Uva'),
    ('#A3A3D9', 'Lilás Claro'),
    ('#FF0049', 'Vermelho'),
    ('#FF4400', 'Laranja Neon'),
    ('#D9675B', 'Laranja Claro'),
    ('#D95BCA', 'Rosa'),
    ('#DB6100', 'Laranja Escuro'),
    ('#D9A8A3', 'Bege'),
]

class Colecao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    cor = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FFCA2C')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    foto = models.ImageField(upload_to='fotos_colecoes/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status_colecao = models.BooleanField(default=True)
    privacidade_colecao = models.BooleanField(default=False)
    tags = models.CharField(max_length=100, blank=True)
    orcamento_colecao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    localizacao_colecao = models.CharField(max_length=100, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Usuario, related_name='colecoes_curtidas', blank=True)

    class Meta:
        unique_together = ('nome', 'usuario',)

    def __str__(self):
        return self.nome

    def get_likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.nome
    
class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=100, blank=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, blank=True)
    ano_fabricacao = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='fotos_itens/', blank=True, null=True)
    notas_adicionais = models.TextField(blank=True)
    colecao = models.ForeignKey(Colecao, related_name='itens', on_delete=models.CASCADE)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    colecao = models.ForeignKey(Colecao, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.usuario.username} em {self.colecao.nome}'
    
class Busca(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)