from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def cadastro(request):
    """ Cadastra uma nova pessoa no sistema """
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O campo NOME não pode ficar em branco!')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O campo EMAIL não pode ficar em branco!')
            return redirect('cadastro')
        if campo_vazio(senha):
            messages.error(request, 'O campo SENHA não pode ficar em branco!')
            return redirect('cadastro')
        if senha != senha2:
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário ja cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário ja cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """ Realiza o login de uma pessoa no sistema """
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Preencha os campos com seu email e senha cadastrados!')
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')
        else:
            messages.error(request, 'Email e/ou senha inválidos!')
            return redirect('login')
    return render(request, 'usuarios/login.html')

def logout(request):
    """ Faz o logout de uma pessoa no sistema """
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """ Insere a pagina de dashboard no sistema """
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)
        paginator = Paginator(receitas, 6)
        page = request.GET.get('page')
        receitas_por_pagina = paginator.get_page(page)

        dados = {
            'receitas' : receitas_por_pagina
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')
        
def campo_vazio(campo):
    """ Função para não permitir que o campo esteja vazio """
    return not campo.strip()


