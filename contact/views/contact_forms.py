from django.shortcuts import render, get_object_or_404, redirect, reverse
from contact.models import Contact
from contact.forms import ContactForm


def create(request):
    form_action = reverse("contact:create")
    form = ContactForm(data=request.POST or None)

    context = {
        "form": form,
        "form_action": form_action,
    }

    if request.method == "POST" and form.is_valid():
        contact = form.save()
        return redirect("contact:update", contact_id=contact.pk)

    return render(request, "contact/pages/create.html", context)


def update(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse("contact:update", args=(contact_id,))

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        context = {"form": form, "form_action": form_action}

        if form.is_valid():
            form.save()
            return redirect("contact:update", contact_id=contact.pk)
        return render(request, "contact/pages/create.html", context)

    context = {
        "form": ContactForm(instance=contact),
        "form_action": form_action,
    }

    return render(request, "contact/pages/create.html", context)
