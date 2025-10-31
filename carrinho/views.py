from django.shortcuts import render

# Create your views here.
# No seu views.py

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .carrinho import Carrinho
from .models import Produto

@require_POST  # Força que esta view só aceite requisições POST
def adicionar_ao_carrinho(request, produto_id):
    carrinho = Carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Pega a quantidade do formulário, ou assume 1
    quantidade = int(request.POST.get('quantidade', 1))
    
    carrinho.adicionar(produto=produto, quantidade=quantidade)
    
    # Redireciona para a página de onde o usuário veio
    return redirect(request.META.get('HTTP_REFERER', 'lista_produtos'))