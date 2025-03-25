from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact, Category  # Importe Category


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Digite o seu primeiro nome"}
        ),
        label="Primeiro Nome",
        help_text="Digite o seu primeiro nome",
        # Mensagem customizada
        error_messages={"required": "Este campo é obrigatório."},
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Digite o seu sobrenome"}
        ),
        label="Sobrenome",
        help_text="Digite o seu sobrenome",
        required=False,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Digite o seu e-mail"}
        ),
        label="E-mail",
        help_text="Digite o seu e-mail",
        error_messages={"required": "Este campo é obrigatório."},
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Digite o seu telefone"}
        ),
        label="Telefone",
        help_text="Digite o seu telefone",
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Digite uma descrição"}
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
        empty_label="----------",  # Boa prática
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contact
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "description",
            "category",
        )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name and not first_name.isalpha():
            self.add_error(
                "first_name",
                ValidationError(
                    "Este campo deve conter apenas letras.", code="invalid"
                ),
            )
        return first_name

    def clean_last_name(self):  # Adicionado clean_last_name
        last_name = self.cleaned_data.get("last_name")
        if last_name and not last_name.isalpha():
            self.add_error(
                "last_name",
                ValidationError(
                    "Este campo deve conter apenas letras.", code="invalid"
                ),
            )
        return last_name

    def clean_phone(self):  # Adicionado clean_phone
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():  # somente números
            self.add_error(
                "phone",
                ValidationError(
                    "O campo telefone deve conter apenas números.", code="invalid"
                ),
            )
        return phone

    def clean_description(self):
        description = self.cleaned_data.get("description")

        if description:  # Só valida se a descrição foi preenchida
            description = (
                description.strip()
            )  # Remove espaços em branco do início e do final
            # Reduz múltiplos espaços a um único
            description = " ".join(description.split())

            min_length = 10  # Exemplo: mínimo de 10 caracteres
            max_length = 200  # Exemplo: máximo de 200 caracteres

            if len(description) < min_length:
                self.add_error(
                    "description",
                    ValidationError(
                        f"A descrição deve ter pelo menos {min_length} caracteres.",
                        code="min_length",
                    ),
                )
            if len(description) > max_length:
                self.add_error(
                    "description",
                    ValidationError(
                        f"A descrição deve ter no máximo {max_length} caracteres.",
                        code="max_length",
                    ),
                )
            # validação de palavras proibidas:
            forbidden_words = ["Bobão", "Henry", "Boboca, Bobao"]
            for word in forbidden_words:
                if word.lower() in description.lower():
                    self.add_error(
                        "description",
                        ValidationError(
                            "A descrição contém palavras proibidas.",
                            code="forbidden_words",
                        ),
                    )
                    break  # Interrompe o loop após encontrar a primeira palavra proibida

        return description
