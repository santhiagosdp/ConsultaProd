from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Produto, Emitente, Nota
from datetime import datetime, date
import datetime
from datetime import date
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
    #print(usuario)
    #prods = Produto.objects.filter(usuario=usuario) #busca somente elementos do usuario logado
    prods = Produto.objects.all() #busca todos elementos
    #prods = Produto.objects.get(especifo)  #Busca elemento Especifico
    
    #return HttpResponse(prods[0].usuario)
    pesquisa = request.GET.get('search')
    if pesquisa:
        prods = Produto.objects.filter(nome__icontains=pesquisa.rstrip().lstrip())
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
    usuario = request.user

######   SE JA EXISTIR A NFC, NEM FAZ O RESTANTE #########
    chave = chaveNF(data)
    notas = Nota.objects.filter(chave=chave)
    if notas:
        return 0
    #for nota in basedados:
        #if prod.nota.chave == chave:
            #return 0

    emitente = cadastrarEmitenteDB(data,usuario) #retorar o get do emitente
    nota = cadastrarNotaDB(data,usuario,emitente)  #retornar o get da Nota
    cadastrarProdutoDB(data,usuario,nota)

    return 0

#################  Adicionar EMITENTE caso não exista ##########################
def cadastrarEmitenteDB(dado, usuario):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    emit = data.get("emit")

    # RAZAO SOCIAL - NOME
    nome = emit.get("xNome") 
    # FANTASIA
    if emit.get("xFant"):
        fantasia = emit.get("xFant")
    else:
        fantasia = emit.get("xNome")
    # CNPJ
    cnpj = emit.get("CNPJ") 
    # ENDEREÇO
    enderEmit = emit.get("enderEmit")
    endereco = enderEmit.get("xLgr")
    # CIDADE
    cidade= enderEmit.get("xMun") 
    # ESTADO
    estado= enderEmit.get("UF")     

    mercado = Emitente.objects.filter(cnpj=cnpj)
    if mercado:
        mercado = Emitente.objects.get(cnpj=cnpj)
        return mercado
    else:
        # Criando o mercado
        emitente = Emitente.objects.create(
            usuario = usuario,
            nome=nome,
            fantasia=fantasia,
            cnpj=cnpj,
            endereco=endereco,
            cidade=cidade,
            estado=estado
        )
        return emitente
#################  FIM DO Adicionar EMITENTE caso não exista ##########################


################# Adicionar NOTA FISCAL  caso não exista ##########################
def cadastrarNotaDB(dado,usuario,emitente):
    dtcompra = dataCompra(dado)
    chave = chaveNF(dado)   
    nota =Nota.objects.create(
        usuario = usuario,
        mercado = emitente,
        dataCompra = dtcompra,
        chave=chave
    )
    return nota
#################  FIM DO Adicionar NOTA FISCAL  caso não exista##########################



################# Adicionar PRODUTO  CASO VALOR NO MESMO MERCADO SEJA MENOR E A DATA MAIS RECENTE  ##########################
def cadastrarProdutoDB(dado,usuario,nota):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    det = data.get("det")

    if (type(det) == list):  ##se tiver varios produtos,faça
        for indice in det:
            item = indice

            nome = nomeProduto(item)
            preco = precoP(item)
            produtos = Produto.objects.filter(nome=nome)
            if produtos:
                for prod in produtos:
                    if prod.nota.mercado == nota.mercado:
                        #if prod.nota.dataCompra != nota.dataCompra:  ##########Falta atualizar para so alterar quando data for maior
                        #alterando o produto ja cadastrado
                            #print(preco)
                        prod.nota = nota
                        prod.preco = preco
                        prod.save()
            else:
                #inserindo o produto um por um da lista
                produto = Produto.objects.create(
                        usuario=usuario,
                        nota = nota,
                        nome = nome,
                        preco = preco
                )
    else:
        nome = nomeProduto(det)
        preco = precoP(det)
        produtos = Produto.objects.filter(nome=nome)
        if produtos:
            for prod in produtos:
                if prod.nota.mercado == nota.mercado:
                    #if prod.nota.dataCompra > nota.dataCompra: ##########Falta atualizar para so alterar quando data for maior
                    #alterando o produto ja cadastrado
                    prod.nota = nota
                    prod.preco = preco
                    prod.save()

        else:
            #inserindo o produto único
            produto = Produto.objects.create(
                    usuario=usuario,
                    nota = nota,
                    nome = nome,
                    preco = preco
            )
#################  FIM DO Adicionar PRODUTO  CASO VALOR NO MESMO MERCADO SEJA MENOR E A DATA MAIS RECENTE##########################




################## DEFs para retirnar valores para insersão no DB ##################################

# Retornar o nomeProduto
def nomeProduto(dado):
    data = dado.get("prod")
    data = data.get("xProd")
    return data

# Retornar Preço
def precoP(dado):
    data = dado.get("prod")
    data = data.get("vUnCom")
    return data

# Retornar Data da Compra
def dataCompra(dado):
    data = dado.get("nfeProc")
    data = data.get("protNFe")
    data = data.get("infProt")
    data = data.get("dhRecbto")
    return data

# Retornar Chave da NF
def chaveNF(dado):
    data = dado.get("nfeProc")
    data = data.get("protNFe")
    data = data.get("infProt")
    data = data.get("chNFe")
    return data


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
           # print("file")
           # print(file)
            os.remove('{}/{}'.format(path, "xmlImport.xml"))