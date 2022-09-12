from django.http import HttpRequest
from django.core.validators import validate_email
from django.contrib.auth.models import User


def filtro_usuario_existente(request: HttpRequest, campos: tuple):
    post = request.POST
    if User.objects.filter(username=post['usuario']).exists() or (
            User.objects.filter(email=post['email']).exists()):
        return False, "Este usuário já está cadastrado"

    return True, "Cadastrado"


def filtro_senhas_iguais(request: HttpRequest, campos: tuple):
    post = request.POST

    if post['senha'] != post['senha2']:
        return False, "Senhas precisam ser iguais."

    return True, 'Senhas Iguais'


def filtro_tamanho_de_senha_e_caracteres(request: HttpRequest, campos: tuple):
    senha = request.POST.get('senha')

    if len(senha) < 5:
        return False, 'Senha precisa ter pelo menos 6 caracteres'

    return True, 'Senha Válida'


def filtro_tamanho_de_usuario(request: HttpRequest, campos: tuple):
    usuario = request.POST.get('usuario')

    if len(usuario) < 5:
        return False, 'Usuario precisa ter pelo menos 6 caracteres'

    return True, 'Usuario Válida'


def filtro_campos_preenchidos(request: HttpRequest, campos: tuple):
    if not all([request.POST.get(campo) for campo in campos]):
        return False, 'Todos os campos devem estar preenchidos'
    return True, 'Todos os campos estão preenchidos'


def filtro_email_correto(request: HttpRequest, campos: tuple):
    email = request.POST.get('email')
    try:
        validate_email(email)
        return True, 'Email Válido'
    except:
        return False, 'Email Inválido'


_filtros = {
    'cadastro_usuarios': [filtro_senhas_iguais,
                          filtro_campos_preenchidos,
                          filtro_email_correto,
                          filtro_tamanho_de_senha_e_caracteres,
                          filtro_tamanho_de_usuario,
                          filtro_usuario_existente],

    'login_dashboard': [filtro_campos_preenchidos],
}
