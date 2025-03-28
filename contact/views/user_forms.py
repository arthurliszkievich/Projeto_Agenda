from django.shortcuts import render, redirect
from django.contrib import messages
from contact.forms import RegisterForm


def register(request):
    form = RegisterForm(data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cadastro realizado com sucesso")
        return redirect("contact:index")

    return render(request,
                  "contact/pages/register.html",
                  {"form": form}
                  )
