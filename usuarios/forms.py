from django import forms

class LoginForms(forms.Form):
    nome_login = forms.CharField(
        label="Nome de Login",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: fulano"
            }
        )
    )
    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Abc123@"
            }
        )
    )

class CadastroForms(forms.Form):

    nome_cadastro = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: fulano"
            }
        )
    )

    nome_completo_cadastro = forms.CharField(
        label="Nome completo",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Fulando Silva"
            }
        )
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: fulano@gmail.com"
            }
        )
    )

    senha_1 = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Digite sua senha"
            }
        )
    )

    senha_2 = forms.CharField(
        label="Confirme a senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Confirme sua senha "
            }
        )
    )