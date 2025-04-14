from django.shortcuts import render, get_object_or_404, redirect, reverse
from contact.models import Contact
from contact.forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
            messages.success(request, "Contato criado com sucesso!")
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


@login_required(login_url="contact:login")
def update(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)
    form_action = reverse("contact:update", args=(contact_id,))

    if request.method == "POST":
        form = ContactForm(
            request.POST, files=request.FILES or None, instance=contact)
        if form.is_valid():
            form.save()
            # Adicionar mensagem
            messages.success(request, "Contato atualizado com sucesso!")
            # Redirecionar para a mesma página de update
            return redirect("contact:update", contact_id=contact.pk)
        # Se inválido, cai para o render abaixo
    else:
        form = ContactForm(instance=contact)

    context = {
        "form": form,
        "form_action": form_action,
    }
    return render(request, "contact/pages/create.html", context)


@login_required(login_url='contact:login')
def delete(request, contact_id):
    # Busca o contato ou retorna 404, garantindo que pertence ao usuário
    contact = get_object_or_404(
        Contact, pk=contact_id, owner=request.user, show=True)

    if request.method == 'POST':
        try:
            contact_name = f"{contact.first_name} {contact.last_name}".strip()
            contact.delete()
            messages.success(
                request, f'Contato "{contact_name}" apagado com sucesso!')
            # SEMPRE redireciona após um POST bem-sucedido
            return redirect('contact:index')
        except Exception as e:
            # Em caso de erro inesperado ao deletar
            messages.error(
                request, f'Ocorreu um erro ao tentar apagar o contato: {e}')
            # Redireciona de volta para a página de detalhes
            return redirect('contact:detail', contact_id=contact_id)

    # Se o método NÃO for POST (ex: alguém tentando acessar a URL /delete/ diretamente via GET)
    messages.error(request, 'Operação não permitida.')
    # Redireciona de volta para os detalhes
    return redirect('contact:detail', contact_id=contact_id)
