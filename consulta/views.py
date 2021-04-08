from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Produto
from datetime import datetime, date
import json
import xmltodict
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os




########## Inicio Autenticação ########################
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('consulta_lista')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'cadastro.html', {'form_usuario': form_usuario})

def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('consulta_lista')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})

def logout_view(request):
    logout(request)
    return redirect('logar_usuario')

#########  Fim Autenticação #################



@login_required
#Página de consulta INDEX
def consulta_lista(request):
    usuario = request.user
    print(usuario)
    prods = Produto.objects.filter(author=usuario) #busca somente elementos do usuario logado
    #prods = Produto.objects.all() #busca todos elementos
    #prods = Produto.objects.get(especifo)  #Busca elemento Especifico
    
    #return HttpResponse(prods[0].author)
    print("prods safdfdasfs")
    pesquisa = request.GET.get('search')
    if pesquisa:
        prods = Produto.objects.filter(author=usuario,nomeProduto__icontains=pesquisa.rstrip().lstrip())
       #print("antes"+pesquisa.rstrip().lstrip()+"depois")
    else:
        pesquisa = "Digite o nome do produto"

    return render(request, 'consulta_lista.html', {'prods': prods, 'pesquisa': pesquisa})



@login_required
#Página para adicionar produtos através do XML
def addXML(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)  # Cria para salvar
        filename = fs.save( 'xmlImport.xml', myfile)  # Cria para importar
        uploaded_file_url = fs.url(filename)

        xmlToJson(request)
        apagarEntrada(request)
    apagarEntrada(request)
    return render(request, 'addXML.html', {})

#converter XML em Formato JSON
def xmlToJson(request):
    # def consulta_lista(request):
    # LENDO XML
    with open("xmlAdd/xmlImport.xml") as xml_file:
    #with open("santhiagosdp.pythonanywhere.com/xmlAdd/xmlImport.xml") as xml_file:  ######descomentar online#########
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
    # SALVANDO EM JSON
    json_data = json.dumps(data_dict)
    with open("consulta/xmlAdd/data.json", "w") as json_file:
    #with open("santhiagosdp.pythonanywhere.com/consulta/xmlAdd/data.json", "w") as json_file:  ######descomentar online#########
        json_file.write(json_data)
    json_file.close()

    # BUSCAR DADOS ESPECIFICOS
    data = json.loads(json_data)

    chave = chaveNF(data)
    print(chave)
    #se chave da NFC já existir, nem faz restante
    basedados = Produto.objects.all()
    for prod in basedados:
        if prod.chave == chave:
            return 0
    mercado = nomeRazao(data)
    print(mercado)
    fantasia = nomeFantasia(data)
    print(fantasia)
    cnpj = numcnpj(data)
    print(cnpj)
    cidade = nomeCidade(data)
    print(cidade)
    estado = nomeEstado(data)
    print(estado)
    endereco = enderecoM(data)
    print(endereco)
    dataC = dataCompra(data)
    print(dataC)
    dataPub = datetime.now()
    print(dataPub)
    # print(type(data))
    usuario = request.user

    Addprodutos(usuario,cnpj,fantasia,data, mercado, cidade, estado, endereco, dataC, chave, dataPub,)

    return 0

#Apagar xml criado só pra converter
def apagarEntrada(request):
    path = "xmlAdd/"
    #if os.mkdir(path): # aqui criamos a pasta caso nao exista
            #makedirs(path)
    #path = "santhiagosdp.pythonanywhere.com/xmlAdd/"          ######descomentar online#########
    #if os.mkdir(path): # aqui criamos a pasta caso nao exista
        #makedirs("C:\ Backup\ ")
    dir = os.listdir(path)
    for file in dir:
        if file == 'xmlImport.xml':
            print("file")
            print(file)
            os.remove('{}/{}'.format(path, "xmlImport.xml"))

# Retornar o nome Fantasia
def nomeRazao(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    data = data.get("xNome")
    return data

def nomeFantasia(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    print(data)
    if data.get("xFant"):
        data = data.get("xFant")
    else:
        data = data.get("xNome") 
    return data

def numcnpj(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    data = data.get("CNPJ")
    return data

# Retornar o Cidade
def nomeCidade(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    data = data.get("enderEmit")
    data = data.get("xMun")
    return data

# Retornar o Estado
def nomeEstado(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    data = data.get("enderEmit")
    data = data.get("UF")
    return data

    # Retornar o endereco

#Retornar EnderecoM
def enderecoM(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    data = data.get("enderEmit")
    data = data.get("xLgr")
    return data

# ADICIONAR PRODUTOS
def Addprodutos(usuario, cnpj, fantasia, dado, mercado, cidade, estado, endereco, dataC, chave, dataPub):
    # print("teste")
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    det = data.get("det")
    print(type(data))

    if (type(det) == list):
        for indice in det:
            print("Entrou no For")
            item = indice
            print(item)

            produto = nomeProduto(item)
            print(produto)

            valor = precoP(item)
            print(valor)

        # SALVAR NO BANCO DADOS
            add = Produto.objects.create(author=usuario, cnpj=cnpj, fantasia=fantasia,mercado=mercado, cidade=cidade, estado=estado, endereco=endereco, nomeProduto=produto, preco=valor,
                                         dataCompra=dataC, chave=chave, dataPublicacao=dataPub)

    else:
        produto = nomeProduto(det)
        print(produto)
        valor = precoP(det)
        print(valor)

        # SALVAR NO BANCO DADOS
        add = Produto.objects.create(author=usuario,mercado=mercado, cidade=cidade, estado=estado, endereco=endereco, nomeProduto=produto, preco=valor,
                                     dataCompra=dataC, chave=chave, dataPublicacao=dataPub)

# Retornar o nomeProduto
def nomeProduto(dado):
    data = dado.get("prod")
    data = data.get("xProd")
    return data

    # Retornar o preco

#Retornar Preço
def precoP(dado):
    data = dado.get("prod")
    data = data.get("vUnCom")
    return data

    # Retornar o dataCompra

#Retornar Data Compra
def dataCompra(dado):
    data = dado.get("nfeProc")
    data = data.get("protNFe")
    data = data.get("infProt")
    data = data.get("dhRecbto")
    return data

    # Retornar o chave

#Retornar Chave
def chaveNF(dado):
    data = dado.get("nfeProc")
    data = data.get("protNFe")
    data = data.get("infProt")
    data = data.get("chNFe")
    return data
