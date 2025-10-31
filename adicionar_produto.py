#!/usr/bin/env python
"""
Script para adicionar produtos facilmente
Uso: python adicionar_produto.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from loja.models import Produto

def adicionar_produto():
    print("=== ADICIONAR NOVO PRODUTO ===")
    print()
    
    # Dados do produto
    nome = input("Nome do produto: ")
    preco = float(input("Preço (ex: 29.99): "))
    quantidade = int(input("Quantidade em estoque: "))
    
    # Criar produto
    try:
        produto = Produto.objects.create(
            nome=nome,
            preco=preco,
            quantidade=quantidade,
            disponivel=True if quantidade > 0 else False
        )
        
        print(f"\n✅ Produto criado com sucesso!")
        print(f"   Nome: {produto.nome}")
        print(f"   Preço: R$ {produto.preco}")
        print(f"   Quantidade: {produto.quantidade}")
        print(f"   Disponível: {'Sim' if produto.disponivel else 'Não'}")
        
    except Exception as e:
        print(f"❌ Erro ao criar produto: {e}")

def listar_produtos():
    print("\n=== PRODUTOS EXISTENTES ===")
    produtos = Produto.objects.all()
    
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    
    for produto in produtos:
        status = "✅ Disponível" if produto.disponivel else "❌ Indisponível"
        print(f"ID: {produto.id} | {produto.nome} | R$ {produto.preco} | Qtd: {produto.quantidade} | {status}")

def menu():
    while True:
        print("\n" + "="*50)
        print("           GERENCIAR PRODUTOS")
        print("="*50)
        print("1. Adicionar novo produto")
        print("2. Listar produtos existentes")
        print("3. Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            adicionar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()


