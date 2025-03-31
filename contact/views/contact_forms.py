from django.shortcuts import render, get_object_or_404, redirect, reverse
from contact.models import Contact
from contact.forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importe o messages


@login_required(login_url="contact:login")
def create(request):
    form_action = reverse("contact:create")

    if request.method == "POST":
        # 1. Processar dados do POST
        form = ContactForm(request.POST, request.FILES)  # Instanciar com dados
        if form.is_valid():
            # 2. Salvar se válido
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.success(request, 'Contato criado com sucesso!')
            # 3. REDIRECIONAR após sucesso (para a página de update, por exemplo)
            return redirect("contact:update", contact_id=contact.pk)
        # Se o form NÃO for válido no POST, o código continua e vai renderizar o form com erros abaixo
    else:
        # 4. Se for GET, criar um formulário vazio
        form = ContactForm()

    # 5. Preparar contexto (para GET ou POST inválido)
    context = {
        # Contém o form vazio (GET) ou o form com erros (POST inválido)
        "form": form,
        "form_action": form_action,
    }

    # 6. Renderizar o template (acontece no GET ou se o POST for inválido)
    return render(request, "contact/pages/create.html", context)

# --- Sua view update parece correta ---


@login_required(login_url="contact:login")
def update(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)
    form_action = reverse("contact:update", args=(contact_id,))

    if request.method == "POST":
        form = ContactForm(
            request.POST, files=request.FILES or None, instance=contact)
        # Removi a linha context = ... daqui, vamos definir só uma vez
        if form.is_valid():
            form.save()
            # Adicionar mensagem
            messages.success(request, 'Contato atualizado com sucesso!')
            # Redirecionar para a mesma página de update após salvar é comum
            return redirect("contact:update", contact_id=contact.pk)
        # Se inválido, cai para o render abaixo
    else:
        # GET request: preencher form com dados da instância
        form = ContactForm(instance=contact)

    # Contexto definido aqui para GET ou POST inválido
    context = {
        "form": form,  # Form com dados (GET) ou com erros (POST inválido)
        "form_action": form_action,
    }
    # Renderiza para GET ou POST inválido
    # Usa o mesmo template? Ok.
    return render(request, "contact/pages/create.html", context)

# --- Sua view delete parece correta ---


@login_required(login_url="contact:login")
def delete(request, contact_id):
    # ... (código parece ok) ...
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)

    confirmation = request.POST.get("confirmation", "no")

    if confirmation == "yes":
        contact.delete()
        # Adicionar mensagem
        messages.success(request, 'Contato apagado com sucesso!')
        return redirect("contact:index")

    # Renderiza a página de detalhe com o botão de confirmação
    return render(
        request,
        "contact/pages/contact.html",  # Template de detalhe, não create
        {
            "contact": contact,
            "confirmation": confirmation,
        },
    )
