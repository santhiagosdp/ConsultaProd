from django.shortcuts import render
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

    return render(request, 'addXML.html', {})

#Página de consulta INDEX
def consulta_lista(request):
    prods = Produto.objects.all()
    # print(prods)
    pesquisa = request.GET.get('search')
    if pesquisa:
        prods = Produto.objects.filter(nomeProduto__icontains=pesquisa)
    else:
        pesquisa = "Digite o nome do produto"

    return render(request, 'consulta_lista.html', {'prods': prods, 'pesquisa': pesquisa})



#converter XML em Formato JSON
def xmlToJson(request):
    # def consulta_lista(request):
    # LENDO XML
    with open("xmlAdd/xmlImport.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
    # SALVANDO EM JSON
    json_data = json.dumps(data_dict)
    with open("consulta/xmlAdd/data.json", "w") as json_file:
        json_file.write(json_data)
    json_file.close()

    # BUSCAR DADOS ESPECIFICOS
    data = json.loads(json_data)
    mercado = nomeMercado(data)
    print(mercado)
    cidade = nomeCidade(data)
    print(cidade)
    estado = nomeEstado(data)
    print(estado)
    endereco = enderecoM(data)
    print(endereco)
    dataC = dataCompra(data)
    print(dataC)
    chave = chaveNF(data)
    print(chave)
    dataPub = datetime.now()
    print(dataPub)
    # print(type(data))

    Addprodutos(data, mercado, cidade, estado, endereco, dataC, chave, dataPub)

    return 0

#Apagar xml criado só pra converter
def apagarEntrada(request):
    path = "xmlAdd/"
    dir = os.listdir(path)
    for file in dir:
        if file == 'xmlImport.xml':
            print("file")
            print(file)
            os.remove('{}/{}'.format(path, "xmlImport.xml")) 

# Retornar o nome Fantasia
def nomeMercado(dado):
    data = dado.get("nfeProc")
    data = data.get("NFe")
    data = data.get("infNFe")
    data = data.get("emit")
    # data = data.get("xFant")
    data = data.get("xNome")
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
def Addprodutos(dado, mercado, cidade, estado, endereco, dataC, chave, dataPub):
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
            me = User.objects.get(username='admin')
            add = Produto.objects.create(author=me, mercado=mercado, cidade=cidade, estado=estado, endereco=endereco, nomeProduto=produto, preco=valor,
                                         dataCompra=dataC, chave=chave, dataPublicacao=dataPub)

    else:
        produto = nomeProduto(det)
        print(produto)
        valor = precoP(det)
        print(valor)

        # SALVAR NO BANCO DADOS
        me = User.objects.get(username='admin')
        add = Produto.objects.create(author=me, mercado=mercado, cidade=cidade, estado=estado, endereco=endereco, nomeProduto=produto, preco=valor,
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
