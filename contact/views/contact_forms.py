from django.shortcuts import render, redirect
from contact.forms import ContactForm  # Importe O FORMULÁRIO


def create(request):
    form = ContactForm(data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("contact:index")

    context = {"form": form}
    return render(request, "contact/pages/create.html", context)
