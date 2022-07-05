from email import charset
from pickle import TRUE
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Produto, Emitente, Nota, Acesso
from datetime import datetime, date
import datetime
from datetime import date, datetime
import json
import xmltodict
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
import requests

#def addqrcode
from bs4 import BeautifulSoup
import bs4 as bs
from pyzbar.pyzbar import decode
from PIL import Image
import cv2



########## Inicio Autenticação ########################
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def cadastrar_usuario(request):
    form_usuario = UserCreationForm(request.POST)
    if form_usuario.is_valid():
        form_usuario.save()
        return redirect('consulta_lista')
    else:
        return render(request, 'login.html', {'form_usuario': form_usuario})

    #return redirect('logar_usuario')

def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        #print(username)
        password = request.POST["password"]
        #print(password)
        usuario = authenticate(request, username=username, password=password)
        #print(usuario)
        if usuario is not None:
            login(request, usuario)
            usuario.email = usuario.username
            usuario.save()
            #print(usuario.email)
            print("usuario.username")
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

prodsCarregados = False
#@login_required
#Página de consulta INDEX
def consulta_lista(request):
    usuario = request.user
    #print(usuario)
    #prods = Produto.objects.filter(usuario=usuario) #busca somente elementos do usuario logado
    if prodsCarregados == False:
        prods = Produto.objects.all().order_by('-data') #busca todos elementos
    #prodsCarregados = True
    #prods = Produto.objects.get(especifo)  #Busca elemento Especifico

    #return HttpResponse(prods[0].usuario)
    pesquisa = request.GET.get('search')
    if pesquisa:
        prods = Produto.objects.filter(nome__icontains=pesquisa.rstrip().lstrip()).order_by('-data')
       #print("antes"+pesquisa.rstrip().lstrip()+"depois")
    else:
        pesquisa = "Digite o nome do produto"

    #Acesso.objects.create(nome=request.user,data=datetime.now())
    contador = len(prods)
    return render(request, 'consulta_lista.html', {'prods': prods, 'pesquisa': pesquisa, 'contador':contador})


#@login_required
def acessos(request):
    acessos =[]
    print(request.user)
    if request.user.username == 'santhiago':
        acessos = Acesso.objects.filter().order_by('-data')
        print("entrou")
        #return HttpResponse(consulta)
    return render(request, 'acessos.html', {'acessos': acessos})


@login_required
def consulta_lista_mercado(request,id):
    usuario = request.user
    mercado = Emitente.objects.get(id=id)
    prods = Produto.objects.filter( nota__mercado = mercado ).order_by('-data') #busca todos elementos
    pesquisa = request.GET.get('search')
    if pesquisa:
        prods = Produto.objects.filter( nota__mercado = mercado, nome__icontains=pesquisa.rstrip().lstrip()).order_by('nome')
    else:
        pesquisa = "Digite o nome do produto"
    sair = " - Sair"
    contador = len(prods)
    return render(request, 'consulta_lista.html', {'prods': prods, 'pesquisa': pesquisa, 'mercado':mercado, 'sair':sair, 'contador':contador})


def TESTEaddXML(request):
    if request.method == 'POST' and request.FILES['myfile[]']:
        myfile = request.FILES['myfile[]']

    return HttpResponse(myfile[0])



import shutil
from os import listdir
from os.path import isfile, join
#@login_required
#Página para adicionar produtos através do XML
def addXML(request):  ##/add3
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)  # Cria para salvar
        filename = fs.save( 'xmlImport.xml', myfile)  # Cria para importar
        uploaded_file_url = fs.url(filename)

        xmlToJson(request)
        apagarEntrada(request)
        shutil.move('xmlAdd/{}'.format(myfile),'xmlAdd/adicionadas/')
        #shutil.move('santhiagosdp.pythonanywhere.com/xmlAdd/{}'.format(xml),'santhiagosdp.pythonanywhere.com/xmlAdd/adicionadas/') ###### descomentar online#########
    apagarEntrada(request)
    #return render(request, 'addXML.html', {})
    return redirect('consulta_lista')
    
def addFotoNFC(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)  # Cria para salvar
        filename = fs.save( 'qrcode.jpeg', myfile)# Cria para importar
        #uploaded_file_url = fs.url(filename)  

        #shutil.move('xmlAdd/{}'.format(myfile),'consulta/qrcodes/')
        shutil.move('xmlAdd/qrcode.jpeg','consulta/qrcodes/')
        
        # chama metodo pra buscar dados e salvar
        #chama metodo salvar dados
        # move foto p outra pasta
        addqrcode()

    return redirect('consulta_lista')

'''

# LOGICA TESTE PARA ADD VARIOS XMLs
def addXML(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)  # Cria para salvar
        filename = fs.save( 'xmlImport.xml', myfile)  # Cria para importar
        uploaded_file_url = fs.url(filename)

        xmlToJson(request)
        apagarEntrada(request)
        shutil.move('xmlAdd/{}'.format(xml),'xmlAdd/adicionadas/')
        #shutil.move('santhiagosdp.pythonanywhere.com/xmlAdd/{}'.format(xml),'santhiagosdp.pythonanywhere.com/xmlAdd/adicionadas/') ###### descomentar online#########
    apagarEntrada(request)
    #return render(request, 'addXML.html', {})
    return redirect('consulta_lista')

    '''

import shutil
from os import listdir
from os.path import isfile, join
def addLote (request):
    path = 'xmlAdd/'  ######descomentar online   santhiagosdp.pythonanywhere.com/ #########
    repetidas = []
    repetidas2 = []

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for xml in files:
       
        with open('xmlAdd/{}'.format(xml)) as xml_file: ###### descomentar online#########
            #print("DATA  INICIO 2 erro aqui")
            #print(xml_file)
            data_dict = xmltodict.parse(xml_file.read())
            #print("DATA  INICIO 3")
        xml_file.close()
        #print("DATA  INICIO 4")
        json_data = json.dumps(data_dict)
        #print("DATA  INICIO 5")
        with open("consulta/xmlAdd/data.json", "w") as json_file:  ###### descomentar online#########
            json_file.write(json_data)
        json_file.close()
        data = json.loads(json_data)
        
        #print(data)
        #print("DATA  FIM 2")
        usuario = request.user
        chave = chaveNF(data)
        notas = Nota.objects.filter(chave=chave)
        if notas:
            repetidas.append(xml)
            repetidas2.append(chave)
            shutil.move('xmlAdd/{}'.format(xml),'xmlAdd/repetidos/') ###### descomentar online#########
        else:
            emitente = cadastrarEmitenteDB(data,usuario)
            nota = cadastrarNotaDB(data,usuario,emitente)
            cadastrarProdutoDB(data,usuario,nota)
            shutil.move('xmlAdd/{}'.format(xml),'xmlAdd/adicionadas/') ###### descomentar online#########
    #print (repetidas2)
    #print (repetidas)
    #return HttpResponse("adicionados")
    return redirect('consulta_lista')


def uploadlote (request):
    
    return HttpResponse("teste url Upload  Lote")


def addAvulso(request):
    usuario = request.user

    nomeMercado = request.POST.get('nomeM')
    cnpj= request.POST.get('cnpj')
    cidade = request.POST.get('cidade')
    estado = request.POST.get('estado')
    endereco = request.POST.get('endereco')
    emitente = Emitente.objects.create(
        usuario = usuario,
        nome=nomeMercado,
        fantasia=nomeMercado,
        cnpj=cnpj,
        cidade = cidade,
        estado = estado,
        endereco = endereco
        )

    #adicionando nota avulsa
    dtcompra = timezone.now()
    chave = "Adicionado Avulso"
    nota = Nota.objects.create(
        usuario = usuario,
        mercado = emitente,
        dataCompra = dtcompra,
        chave=chave
    )

    #adicionando produto avulso
    nome = request.POST.get('nomeP')
    preco = request.POST.get('preco')
    produto = Produto.objects.create(
        usuario=usuario,
        nota = nota,
        nome = nome,
        preco = preco
    )
    #return render(request, 'addXML.html', {})
    return redirect('consulta_lista')


#converter XML em Formato JSON
def xmlToJson(request):
    # def consulta_lista(request):
    # LENDO XML
    with open("xmlAdd/xmlImport.xml") as xml_file:  ######descomentar online#########
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
    # SALVANDO EM JSON
    json_data = json.dumps(data_dict)
    with open("consulta/xmlAdd/data.json", "w") as json_file:  ######descomentar online#########
        json_file.write(json_data)
    json_file.close()

    # BUSCAR DADOS ESPECIFICOS
    data = json.loads(json_data)
    usuario = request.user

######   SE JA EXISTIR A NFC, NEM FAZ O RESTANTE #########
    chave = chaveNF(data)
    notas = Nota.objects.filter(chave=chave)
    if notas:
        #shutil.move('xmlAdd/{}'.format(xml),'xmlAdd/repetidos/') ###### descomentar online#########
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
        print("INSERINDO EMITENTE NO BD")
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
    print("INSERINDO NF NO BD")
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
            data = nota.dataCompra
            produtos = Produto.objects.filter(nome=nome)
            if produtos:
                for prod in produtos:
                    if prod.nota.mercado == nota.mercado:
                        #if prod.nota.dataCompra != nota.dataCompra:  ##########Falta atualizar para so alterar quando data for maior
                        #alterando o produto ja cadastrado
                            #print(preco)
                        prod.nota = nota
                        prod.preco = preco
                        prod.data = data
                        prod.save()
            else:
                #inserindo o produto um por um da lista
                print("INSERINDO VÁRIOS PRODUTOS NO BD")
                produto = Produto.objects.create(
                        usuario=usuario,
                        nota = nota,
                        nome = nome,
                        preco = preco,
                        data = data
                )
    else:  # se for somente um produto
        nome = nomeProduto(det)
        preco = precoP(det)
        data = nota.dataCompra
        produtos = Produto.objects.filter(nome=nome)
        if produtos:
            for prod in produtos:
                if prod.nota.mercado == nota.mercado:
                    #if prod.nota.dataCompra > nota.dataCompra: ##########Falta atualizar para so alterar quando data for maior
                    #alterando o produto ja cadastrado
                    prod.nota = nota
                    prod.preco = preco
                    prod.data = data

                    prod.save()

        else:
            #inserindo o produto único
            print("INSERINDO PRODUTO ÚNICO NO BD")
            produto = Produto.objects.create(
                    usuario=usuario,
                    nota = nota,
                    nome = nome,
                    preco = preco,
                    data = data

            )
#################  FIM DO Adicionar PRODUTO  CASO VALOR NO MESMO MERCADO SEJA MENOR E A DATA MAIS RECENTE##########################




################## DEFs para retirnar valores para insersão no DB ##################################

# Retornar o nomeProduto
def nomeProduto(dado):
    data = dado.get("prod")
    nome = data.get("xProd")
    cprod = data.get("cProd")
    ncm = data.get("NCM")
    todo = nome+" - NCM:"+ncm+" - Cod:"+cprod
    #print('**********************************************************************************')
    print("nome produto retornado: "+todo)
    return todo

# Retornar Preço
def precoP(dado):
    data = dado.get("prod")
    valorVenda = float(data.get("vUnCom"))
    desc = float(0)
    print('**********************************************************************************')
    print(data.get("vDesc"))
    if data.get("vDesc") != None:
        #print ("valor igual a NONE")
        desc = float(data.get("vDesc"))
    print('**********************************************************************************')
    print(desc)
    if (desc != 0):
        valorVenda = valorVenda - desc

    print("Preço produto retornado: ")
    print(valorVenda)
    return valorVenda
    #31220211200418000673550010401552471220982742

# Retornar Data da Compra
def dataCompra(dado):
    data = dado.get("nfeProc")
    data = data.get("protNFe")
    data = data.get("infProt")
    data = data.get("dhRecbto")
    print("data compra produto retornado: "+data)
    return data

# Retornar Chave da NF
def chaveNF(dado):
    data = dado.get("nfeProc")
    data = data.get("protNFe")
    data = data.get("infProt")
    data = data.get("chNFe")
    print("Chave NF retornado: "+data)
    return data


#Apagar xml criado só pra converter
def apagarEntrada(request):
    #path = "xmlAdd/"
    path = "xmlAdd/"          ######descomentar online#########
    dir = os.listdir(path)
    for file in dir:
        if file == 'xmlImport.xml':
           # print("file")
           # # print(file)
            print("APAGANDO XMLIMPORT")
            os.remove('{}/{}'.format(path, "xmlImport.xml"))




####### INICIAL  - TESTE ADD VIA QRCODE #########################
'''from pyzbar.pyzbar import decode
from PIL import Image
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
#import picamera

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
#	help="path to output CSV file containing barcodes")
#args = vars(ap.parse_args())


def addqrcode(request, mirror=False):
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open("output", "w")
    found = set()


    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

    # loop over the detected barcodes
        for barcode in barcodes:
            print("entrou no BARCODE 111")

            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                print("entrou no BARCODE 222")
                csv.write("{},{}\n".format(datetime.datetime.now(),
                    barcodeData))
                csv.flush()
                #found.add(barcodeData)
        # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # close the output CSV file do a bit of cleanup
    print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()


    return HttpResponse("concluido")'''


####### FINAL   - TESTE ADD VIA QRCODE #########################

def teste(request):
    #result = "teste  fff"

    #html = requests.get("https://www.climatempo.com.br/previsao-do-tempo/cidade/593/palmas-to").content
    #html = requests.get("http://www.sefaz.to.gov.br/nfce/qrcode?p=17220516593945000102650050000192061016877637|2|1|1|9be42a48b5ab0422d6b9f90a099ceae604a349a7").content

    #soup = BeautifulSoup(html,'html.parser')
    #resume = soup.find(class_='-gray -line-height-24 _center')
    #titulo = soup.find(class_="-bold -font-18 -dark-blue _margin-r-10 _margin-b-sm-5")
    #nfc = soup.find(class_="ui-menuitem ui-widget ui-corner-all")
   # class_="ui-widget-content ui-datatable-odd"
   # class_="ui-widget-content ui-datatable-even"
   
    #print(nfc)
    #return HttpResponse(nfc)


   ###
## trabalhar com tabelas
#https://acervolima.com/analise-de-tabelas-e-xml-com-beautifulsoup/
    #URL = 'https://worldpopulationreview.com/countries'
    URL = 'http://www.sefaz.to.gov.br/nfce/qrcode?p=17220516593945000102650050000192061016877637|2|1|1|9be42a48b5ab0422d6b9f90a099ceae604a349a7'

    url_link = requests.get(URL) 
    file = bs.BeautifulSoup(url_link.text, "lxml") 
    find_table = file.find('table') 
    rows = find_table.find_all('tr') 
    for i in rows: 
        table_data = i.find_all('td') 
        data = [j.text for j in table_data] 
        print(data)

    #print(nfc)
    return HttpResponse(data)

'''def addqrcode(request, mirror=False):
    img = cv2.imread('consulta/qrcodes/qrcode.png')
    result = decode(img)
    for i in result:
       result = i.data.decode("utf-8")

    request = requests.get(result)

    #return HttpResponse(img)
    #return HttpResponse(result)
    
    print(result)
    return HttpResponse(request)
    #return HttpResponse("concluido")'''


def addqrcode(mirror=False):

    img = cv2.imread('consulta/qrcodes/qrcode.jpeg')
    #return HttpResponse(img)
    
    result = decode(img)
    print("######################################### resultado 1 ##########################")
    print(result)
    for i in result:
       result = i.data.decode("utf-8")
       print("######################################### resultado 2 ##########################")
       print(result)

    url_link = requests.get(result)
    file = bs.BeautifulSoup(url_link.text, "lxml") 
    find_table = file.find('table') 
    rows = find_table.find_all('tr') 
    for i in rows: 
        table_data = i.find_all('td') 
        data = [j.text for j in table_data] 
        print(data)

    #print(nfc)
    return HttpResponse(data)