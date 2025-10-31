# loja/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Produto
from .forms import ProdutoForm
import django_filters
from .filters import ProdutoFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carrinho.carrinho import Carrinho

# ----- Class-Based View para lista -----
class ListaProdutosView(ListView):
    model = Produto
    template_name = 'lista_produtos.html'
    context_object_name = 'produtos'

# ----- Class-Based View para detalhe -----
class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produto_detail.html'
    context_object_name = 'produto'

def lista_produtos_filtrada(request):
    f = ProdutoFilter(request.GET, queryset=Produto.objects.all())
    return render(request, 'lista_produtos_filtrada.html', {'filter': f})

def adicionar_ao_carrinho(request, produto_id):
    print(f"DEBUG: Tentando adicionar produto {produto_id} ao carrinho")
    print(f"DEBUG: Usuário autenticado: {request.user.is_authenticated}")
    print(f"DEBUG: Usuário: {request.user}")
    
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para adicionar ao carrinho.')
        return redirect('login')
    
    produto = get_object_or_404(Produto, id=produto_id)
    print(f"DEBUG: Produto encontrado: {produto.nome}")

    if not produto.disponivel or produto.quantidade <= 0:
        messages.error(request, f'O produto "{produto.nome}" não está disponível')
        return redirect(request.META.get('HTTP_REFERER', 'lista_produtos'))
    
    carrinho = Carrinho(request)
    carrinho.adicionar(produto=produto)
    messages.success(request, f'"{produto.nome}" foi adicionado ao carrinho')
    print(f"DEBUG: Produto adicionado ao carrinho com sucesso")
    return redirect(request.META.get('HTTP_REFERER', 'lista_produtos'))

@login_required
def ver_carrinho(request):
    carrinho = Carrinho (request)
    return render(request,  'carrinho.html', {'carrinho': carrinho})

@login_required
def remover_do_carrinho(request, produto_id):
    carrinho = Carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho.remover(produto)
    return redirect('ver_carrinho')

@login_required
def checkout(request):
    carrinho = Carrinho(request)

    for item in carrinho:
        produto = item['produto']
        quantidade_comprada = item['quantidade']

        if produto.quantidade >= quantidade_comprada:
            produto.quantidade -= quantidade_comprada
            produto.save()
        else:
            messages.error(request, f'O produto "{produto.nome}" não tem no estoque')
            return redirect('ver_carrinho')
    
    carrinho.limpar()
    return render(request, 'checkout_concluido.html')

def sobre(request):
    return render(request, 'sobre.html')

def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        
        # Aqui você pode adicionar lógica para enviar email ou salvar no banco
        messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        return redirect('contato')
    
    return render(request, 'contato.html')

@login_required
def adicionar_produto(request):
    # Verificar se o usuário é admin
    if not request.user.is_superuser:
        messages.error(request, 'Apenas administradores podem adicionar produtos.')
        return redirect('lista_produtos')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" adicionado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    
    return render(request, 'adicionar_produto.html', {'form': form})

@login_required
def excluir_produto(request, produto_id):
    # Verificar se o usuário é admin
    if not request.user.is_superuser:
        messages.error(request, 'Apenas administradores podem excluir produtos.')
        return redirect('lista_produtos')
    
    produto = get_object_or_404(Produto, id=produto_id)
    nome_produto = produto.nome
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, f'Produto "{nome_produto}" excluído com sucesso!')
        return redirect('lista_produtos')
    
    return render(request, 'confirmar_exclusao.html', {'produto': produto})

@login_required
def editar_produto(request, produto_id):
    # Verificar se o usuário é admin
    if not request.user.is_superuser:
        messages.error(request, 'Apenas administradores podem editar produtos.')
        return redirect('lista_produtos')
    
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})



