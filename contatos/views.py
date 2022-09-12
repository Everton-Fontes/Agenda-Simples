
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from . import models
from asgiref.sync import sync_to_async

# Create your views here.


@sync_to_async()
def index(request: HttpRequest):
    #

    contatos = models.Contato.objects.order_by(
        "nome"
    ).select_related('categoria').filter(mostrar=True)
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


async def detalhes(request: HttpRequest, id: int):
    # .select_related("categoria")
    try:
        contato = await models.Contato.objects.select_related("categoria").aget(id=id)

        if not contato.mostrar:
            messages.add_message(request, messages.ERROR,
                                 'Este Contato não existe')

            return redirect('index')

        return render(request, 'contatos/detalhes.html', {
            'contato': contato
        })
    except models.Contato.DoesNotExist as e:
        raise Http404()
    # contato = get_object_or_404(models.Contato, id=id)
    # return render(request, 'contatos/detalhes.html', {
    #     'contato': contato
    # })


async def busca(request: HttpRequest):
    busca = request.GET.get('s')

    if busca is None or not busca:
        messages.add_message(request, messages.ERROR,
                             'Campo de Pesquisa não pode estar vazio')

        return redirect('index')

    campos = Concat("nome", Value(" "), "sobrenome", Value(" "), "telefone")
    contatos = await sync_to_async(list, thread_sensitive=True)(
        models.Contato.objects.annotate(
            nome_completo_telefone=campos
        )
        .select_related('categoria').filter(
            Q(nome_completo_telefone__icontains=busca),
            mostrar=True
        ))
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })
