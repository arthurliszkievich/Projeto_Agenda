from django.shortcuts import render, redirect
from django.contrib import messages, auth
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm

# Decorador para exigir login e opcionalmente para exigir POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST  # Para logout seguro


def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)  # Passa os dados do POST
        if form.is_valid():
            user = form.save()  # Assume que form.save() lida com hash da senha
            messages.success(
                request,
                f"Usuário '{user.username}' cadastrado com sucesso! Faça o login.",
            )
            return redirect("contact:login")
        else:
            # Se inválido, a view continua e renderiza o form com erros abaixo
            messages.error(
                request, "Erro ao tentar cadastrar. Verifique os erros abaixo."
            )
    else:  # Se for GET
        form = RegisterForm()  # Cria um formulário vazio

    return render(request, "contact/pages/register.html", {"form": form})


@login_required(login_url="contact:login")
def user_update(request):
    # Lógica do POST primeiro
    if request.method == "POST":
        # Passa dados do POST E a instância do usuário logado
        form = RegisterUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Assume que form.save() lida com hash da senha se alterada
            messages.success(request, "Seus dados foram atualizados com sucesso!")
            return redirect("contact:login")
        # else: Se o form POST for inválido, a view continua e renderiza o mesmo form com erros abaixo
    else:  # Se for GET
        # Cria o formulário preenchido com os dados do usuário logado
        form = RegisterUpdateForm(instance=request.user)

    return render(request, "contact/pages/user_update.html", {"form": form})


# --- View de Login ---
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(
                request, f"Login realizado com sucesso como {user.username}!"
            )
            next_url = request.POST.get("next", request.GET.get("next", None))
            if next_url:
                return redirect(next_url)
            return redirect("contact:index")  # Ou para um dashboard, etc.
        else:
            messages.error(request, "Login inválido! Verifique usuário e senha.")
    else:
        form = AuthenticationForm(request)

    # Passa o 'next' para o template, se existir (para o form poder incluir)
    context = {"form": form, "next": request.GET.get("next")}
    return render(request, "contact/pages/login.html", context)


# --- View de Logout ---
@require_POST  # <-- BOA PRÁTICA: Garante que logout só ocorra via POST
def logout_view(request):
    auth.logout(request)
    messages.success(request, "Logout realizado com sucesso.")
    return redirect("contact:login")
