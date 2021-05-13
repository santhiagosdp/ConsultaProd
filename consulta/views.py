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

    return redirect('logar_usuario')

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
    prods = Produto.objects.all().order_by('nome') #busca todos elementos
    #prods = Produto.objects.get(especifo)  #Busca elemento Especifico

    #return HttpResponse(prods[0].usuario)
    pesquisa = request.GET.get('search')
    if pesquisa:
        prods = Produto.objects.filter(nome__icontains=pesquisa.rstrip().lstrip()).order_by('data')
       #print("antes"+pesquisa.rstrip().lstrip()+"depois")
    else:
        pesquisa = "Digite o nome do produto"
    
    Acesso.objects.create(nome=request.user,data=datetime.now())
    contador = len(prods)
    return render(request, 'consulta_lista.html', {'prods': prods, 'pesquisa': pesquisa, 'contador':contador})


@login_required
def acessos(request):
    consulta = Acesso.objects.all()
    #acessos = json.dumps(consulta, indent=2)
    #for c in consulta: 
        #acessos.append = c.nome
    return HttpResponse(consulta)

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
    #return render(request, 'addXML.html', {})
    return redirect('consulta_lista')


import shutil
from os import listdir
from os.path import isfile, join
def addLote (request):
    path = 'xmlAdd/'
    #path = 'santhiagosdp.pythonanywhere.com/xmlAdd/'  ######descomentar online#########
    repetidas = []
    repetidas2 = []

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for xml in files:
        with open('xmlAdd/{}'.format(xml)) as xml_file:
        #with open('santhiagosdp.pythonanywhere.com/xmlAdd/{}'.format(xml)) as xml_file: ###### descomentar online#########
            data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()
        json_data = json.dumps(data_dict)
        with open("consulta/xmlAdd/data.json", "w") as json_file:
        #with open("santhiagosdp.pythonanywhere.com/consulta/xmlAdd/data.json", "w") as json_file:  ###### descomentar online#########
            json_file.write(json_data)
        json_file.close()
        data = json.loads(json_data)
        usuario = request.user
        chave = chaveNF(data)
        notas = Nota.objects.filter(chave=chave)
        if notas:
            repetidas.append(xml)
            repetidas2.append(chave)
            shutil.move('xmlAdd/{}'.format(xml),'xmlAdd/repetidos') 
            #shutil.move('santhiagosdp.pythonanywhere.com/xmlAdd/{}'.format(xml),'santhiagosdp.pythonanywhere.com/xmlAdd/repetidos') ###### descomentar online#########
        else:
            emitente = cadastrarEmitenteDB(data,usuario)
            nota = cadastrarNotaDB(data,usuario,emitente)
            cadastrarProdutoDB(data,usuario,nota)
            shutil.move('xmlAdd/{}'.format(xml),'xmlAdd/adicionados')
            #shutil.move('santhiagosdp.pythonanywhere.com/xmlAdd/{}'.format(xml),'santhiagosdp.pythonanywhere.com/xmlAdd/adicionados') ###### descomentar online#########
    print (repetidas2)
    print (repetidas)
    #return HttpResponse("adicionados")
    return redirect('consulta_lista')




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


from pyzbar.pyzbar import decode
from PIL import Image
import cv2

def addqrcode(request, mirror=False):
    img = cv2.imread('consulta/qrcodes/qrcode.png')
    result = decode(img)
    for i in result:
       result = i.data.decode("utf-8")

    request = requests.get(result)



    #return HttpResponse(img)
    #return HttpResponse(result)
    print(result)
    return HttpResponse(request)
    #return HttpResponse("concluido")



####### FINAL   - TESTE ADD VIA QRCODE #########################




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
    #path = "santhiagosdp.pythonanywhere.com/xmlAdd/"          ######descomentar online#########
    dir = os.listdir(path)
    for file in dir:
        if file == 'xmlImport.xml':
           # print("file")
           # print(file)
            os.remove('{}/{}'.format(path, "xmlImport.xml"))