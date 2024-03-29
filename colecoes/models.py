from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from colorfield.fields import ColorField



class Colecao(models.Model):
    CATEGORIAS_OPCOES = [
        ('LIVROS', 'Livros'),
        ('FILMES', 'Filmes'),
        ('MÚSICAS', 'Músicas'),
        ('JOGOS', 'Jogos'),
        ('SELOS', 'Selos'),
        ('MOEDAS', 'Moedas'),
        ('QUADRINHOS', 'Quadrinhos'),
        ('CARROS', 'Carros'),
        ('VINHOS', 'Vinhos'),
        ('CARTAS', 'Cartas'),
        ('MINIATURAS', 'Miniaturas'),
        ('BRINQUEDOS', 'Brinquedos'),
        ('ANTIGUIDADES', 'Antiguidades'),
        ('RELÓGIOS', 'Relógios'),
        ('JÓIAS', 'Jóias'),
        ('INSTRUMENTOS_MUSICAIS', 'Instrumentos Musicais'),
        ('ARTES', 'Artes'),
        ('ITENS_ESPORTIVOS', 'Itens Esportivos'),
        ('ELETRÔNICOS', 'Eletrônicos'),
        ('VESTUÁRIO', 'Vestuário'),
        ('ACESSÓRIOS', 'Acessórios'),
        ('COSMÉTICOS', 'Cosméticos'),
        ('UTENSÍLIOS_DOMÉSTICOS', 'Utensílios Domésticos'),
        ('DECORAÇÃO', 'Decoração'),
        ('MÓVEIS', 'Móveis'),
        ('ELETRODOMÉSTICOS', 'Eletrodomésticos'),
        ('FERRAMENTAS', 'Ferramentas'),
        ('BRINDES', 'Brindes'),
        ('PEÇAS_RELIGIOSAS', 'Peças Religiosas'),
        ('CHARUTOS', 'Charutos'),
        ('CHAVEIROS', 'Chaveiros'),
        ('PEDRAS_PRECIOSAS', 'Pedras Preciosas'),
        ('PLANTAS', 'Plantas'),
        ('ARTEFATOS_HISTÓRICOS', 'Artefatos Históricos'),
        ('CULINÁRIA', 'Culinária'),
        ('OUTROS', 'Outros'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    cor = ColorField(default='#FFF1C0', blank=False)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_OPCOES, default='OUTROS')
    data_criacao = models.DateTimeField(auto_now_add=True)
    status_colecao = models.BooleanField(default=True)
    privacidade_colecao = models.BooleanField(default=False)
    tags = models.CharField(max_length=100, blank=True)
    orcamento_colecao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    localizacao_colecao = models.CharField(max_length=100, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nome', 'usuario',)

    def __str__(self):
        return self.nome
    
class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100, choices=Colecao.CATEGORIAS_OPCOES, default='OUTROS')
    estado = models.CharField(max_length=100, blank=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, blank=True)
    ano_fabricacao = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='fotos_itens/', blank=True, null=True)
    notas_adicionais = models.TextField(blank=True)
    colecao = models.ForeignKey(Colecao, related_name='itens', on_delete=models.CASCADE)
