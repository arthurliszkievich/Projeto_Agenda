# contact/forms.py

from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    # --- Definições Explícitas dos Campos (para customização) ---
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu primeiro nome", }
        ),
        label="Primeiro Nome",
        help_text="Digite o seu primeiro nome",
        error_messages={"required": "Este campo é obrigatório."},
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu sobrenome"}
        ),
        label="Sobrenome",
        help_text="Digite o seu sobrenome",
        required=False,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu e-mail"}
        ),
        label="E-mail",
        help_text="Digite o seu e-mail",
        error_messages={"required": "Este campo é obrigatório."},
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu telefone"}
        ),
        label="Telefone",
        help_text="Digite o seu telefone",
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "placeholder": "Digite uma descrição"}
        ),
        label="Descrição",
        help_text="Digite uma descrição, caso queira",
        required=False,
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Categoria",
        help_text="Selecione uma categoria",
        empty_label="----------",
        required=False,
    )

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        ),
        label="Imagem",
        help_text="Selecione uma imagem",
        required=False,
    )

    # --- Classe Meta (DEPOIS dos campos explícitos) ---
    class Meta:
        model = Contact
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "description",
            "category",
            "picture",
        )

    # --- Métodos Clean ---
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name and not first_name.isalpha():
            self.add_error(
                "first_name",
                ValidationError(
                    "Este campo deve conter apenas letras.", code="invalid"),
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name and not last_name.isalpha():
            self.add_error(
                "last_name",
                ValidationError(
                    "Este campo deve conter apenas letras.", code="invalid"),
            )
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            self.add_error(
                "phone",
                ValidationError(
                    "O campo telefone deve conter apenas números.", code="invalid"),
            )
        return phone

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            description = description.strip()
            description = " ".join(description.split())
            min_length = 10
            max_length = 200
            if len(description) < min_length:
                self.add_error("description", ValidationError(
                    f"A descrição deve ter pelo menos {min_length} caracteres.", code="min_length"))
            if len(description) > max_length:
                self.add_error("description", ValidationError(
                    f"A descrição deve ter no máximo {max_length} caracteres.", code="max_length"))
            # Cuidado com vírgula dentro da string
            forbidden_words = ["Bobão", "Henry", "Boboca", "Bobao"]
            for word in forbidden_words:
                if word.lower() in description.lower():
                    self.add_error("description", ValidationError(
                        "A descrição contém palavras proibidas.", code="forbidden_words"))
                    break
        return description


class RegisterForm(UserCreationForm):

    # --- Definições Explícitas dos Campos ---
    username = forms.CharField(  # Adicionado campo username
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu nome de usuário", }
        ),
        label="Nome de Usuário",
        help_text="Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.",
        max_length=150,
        error_messages={
            "required": "Por favor, digite um nome de usuário.",
            "unique": "Um usuário com este nome de usuário já existe.",
        },
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu primeiro nome", }
        ),
        label="Primeiro Nome",
        help_text="Digite o seu primeiro nome.",
        min_length=3,
        error_messages={"required": "Este campo é obrigatório."},
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu sobrenome"}
        ),
        label="Sobrenome",
        help_text="Digite o seu sobrenome",
        required=False,
        min_length=3,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control",
                   "placeholder": "Digite o seu e-mail"}
        ),
        label="E-mail",
        help_text="Digite o seu e-mail",
        error_messages={"required": "Informe um e-mail valido."},
    )

    # --- Classe Meta (DEPOIS dos campos explícitos) ---
    class Meta:
        model = User
        fields = (
            "username",  # Adicionado username
            "first_name",
            "last_name",
            "email",
            # Removido password1 e password2 daqui, UserCreationForm cuida deles
        )

    # --- Métodos Clean ---
    def clean_username(self):  # Adicionado clean_username
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error("username", ValidationError(
                "Este nome de usuário já está em uso. Por favor, escolha outro.", code="duplicate_username"))
        return username

    def clean_email(self):  # Modificado para usar add_error e iexact
        email = self.cleaned_data.get("email")
        # iexact para case-insensitive
        if email and User.objects.filter(email__iexact=email).exists():
            self.add_error("email", ValidationError(
                "Este e-mail já foi cadastrado.", code="duplicate_email"))
        return email
