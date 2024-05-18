from django import forms
from colecoes.models import Colecao, Item
from usuarios.models import Usuario

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

class ColecaoForms(forms.ModelForm):
    class Meta:
        model = Colecao
        fields = ['nome', 'descricao', 'cor', 'categoria', 'foto', 'privacidade_colecao', 'tags', 'orcamento_colecao', 'localizacao_colecao']
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'cor': 'Cor',
            'categoria': 'Categoria',
            'foto': 'Foto',
            'privacidade_colecao': 'Privada',
            'tags': 'Tags',
            'orcamento_colecao': 'Orçamento da coleção',
            'localizacao_colecao': 'Localização da coleção',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'cor': forms.Select(choices=COLOR_CHOICES, attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'privacidade_colecao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'orcamento_colecao': forms.NumberInput(attrs={'class': 'form-control'}),
            'localizacao_colecao': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ItemForms(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['colecao']
        fields = ['nome', 'descricao', 'categoria', 'tags', 'valor', 'data_aquisicao','foto', 'notas_adicionais', 'ano_fabricacao']
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'estado': 'Estado',
            'tags': 'Tags',
            'valor': 'Valor',
            'data_aquisicao': 'Data de Aquisição',
            'foto': 'Foto',
            'notas_adicionais': 'Notas Adicionais',
            'ano_fabricacao': 'Ano de Fabricação',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'data_aquisicao': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_fabricacao': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'notas_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EditarPerfilForm(forms.ModelForm):
    nome_completo = forms.CharField(
        label='Nome completo',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    first_name = forms.CharField(
        label='Primeiro nome',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    last_name = forms.CharField(
        label='Último nome',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'first_name', 'last_name', 'email', 'username', 'photo', 'biografia']
        labels = {
            'nome_completo': 'Nome completo',
            'first_name': 'Primeiro nome',
            'last_name': 'Último nome',
            'email': 'Email',
            'username': 'Nome de usuário',
            'photo': 'Foto',
            'biografia': 'Biografia',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.nome_completo:
                self.fields['nome_completo'].initial = self.instance.nome_completo
                self.fields['first_name'].widget = forms.HiddenInput()
                self.fields['last_name'].widget = forms.HiddenInput()
            else:
                self.fields['first_name'].initial = self.instance.first_name
                self.fields['last_name'].initial = self.instance.last_name
                self.fields['nome_completo'].widget = forms.HiddenInput()