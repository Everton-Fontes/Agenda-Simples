from django.shortcuts import render, redirect
from django.contrib import messages, auth
from filters import _filtros
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .models import FormContato
from asgiref.sync import sync_to_async
# Create your views here.


@sync_to_async()
def login(request):
    if request.method != 'POST':
        # messages.add_message(request, messages.INFO, 'Nada Postado')
        return render(request, "accounts/login.html")

    username = request.POST.get('usuario')
    senha = request.POST.get('senha')

    for filtro in _filtros['login_dashboard']:
        status, mensagem = filtro(request, tuple(
            campo for campo in request.POST))
        if not status:
            messages.error(request, mensagem)

    if messages.get_messages(request):
        return render(request, "accounts/login.html")

    usuario = auth.authenticate(request, username=username, password=senha)
    if not usuario:
        messages.error(request, "Usuário ou Senha Inválidos")
        return render(request, "accounts/login.html")

    auth.login(request, usuario)
    messages.success(request, "Logado com sucesso!")
    return redirect('dashboard')


@sync_to_async()
def add(request):
    # messages.add_message(request, messages.SUCCESS, 'Sucesso')
    if request.method != 'POST':
        # messages.add_message(request, messages.INFO, 'Nada Postado')
        return render(request, "accounts/add.html")

    for filtro in _filtros['cadastro_usuarios']:
        status, mensagem = filtro(request, tuple(
            campo for campo in request.POST))
        if not status:
            messages.error(request, mensagem)

    if messages.get_messages(request):
        return render(request, "accounts/add.html")

    post = request.POST
    first_name = post['nome']
    last_name = post['sobrenome']
    email = post['email']
    password = post['senha']
    username = post['usuario']

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    user.save()

    messages.success(request, 'Usuário Cadastrado com sucesso! Bora BILL')
    return redirect('login')


@sync_to_async()
@login_required(redirect_field_name='login')
def dashboard(request: HttpRequest):
    if request.method != 'POST':
        form = FormContato()
        return render(request, "accounts/dashboard.html", {
            "form": form
        })

    form = FormContato(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(
            request, 'Erro Boy, Bora Bill Digite Corretamente, USER EXPERIENCE My Shit')
        form = FormContato(request.POST)
        return render(request, "accounts/dashboard.html", {
            "form": form,
        })

    form.save()
    messages.success(request, 'SUcesso GArai, Bora fi do BILL')
    return redirect('dashboard')


@sync_to_async()
def logout(request):
    auth.logout(request)
    return redirect('login')
