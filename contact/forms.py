from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact
from django.shortcuts import render, redirect


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Primeiro Nome",
        help_text="Texto de ajuda para o usuário",
    )

    class Meta:
        model = Contact
        fields = ("first_name", "last_name", "email", "phone", "category")

    def clean(self):
        cleaned_data = self.cleaned_data

        if not cleaned_data.get("first_name"):
            self.add_error(
                "first_name",
                ValidationError("Este campo é obrigatorio", code="required"),
            )

        if not cleaned_data.get("last_name"):
            self.add_error(
                "last_name",
                ValidationError("Este campo é obrigatorio", code="required"),
            )

        if not cleaned_data.get("phone"):
            self.add_error(
                "phone", ValidationError("Este campo é obrigatorio", code="required")
            )

        return super().clean()


def create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contact:index")

        context = {"form": form}
        return render(request, "contact/pages/create.html", context)

    context = {"form": ContactForm()}

    return render(
        request,
        "contact/pages/create.html",
    )
