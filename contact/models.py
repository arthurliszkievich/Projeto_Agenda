from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Importante para validação


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="pictures/%Y/%m/", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()  # Chame super().clean() em models também

        if self.first_name and self.last_name and self.first_name == self.last_name:
            raise ValidationError(
                "O primeiro nome e o sobrenome não podem ser iguais.")

        # Exemplo: Validação que *sempre* deve ser verdadeira para o modelo
        if self.email and not "@" in self.email:  # Validação básica do formato
            raise ValidationError({"email": "Formato de e-mail inválido."})
