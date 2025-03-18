from django.shortcuts import render
from contact.models import Contact


def index(request):
    contacts = Contact.objects.filter(show=True).order_by("-id")[10:20]

    context = {"contacts": contacts}

    return render(request, "contact/pages/index.html", context)
