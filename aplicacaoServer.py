
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Fisica da Computacao
#Carareto
#17/02/2018
#  Aplicacao
####################################################

def fromByteToInt(bytes):
    result=0

    for b in bytes:
        result=result*256+int(b)

    return result

def sistemaRecebimento(com):
    com.enable()
    print("porta COM aberta com sucesso")


    #Variaveis
    ouvindoMensagem1 = True
    ouvindoMensagem3 = True
    ouvindoMensagem4 = True
    
    



    while ouvindoMensagem1:
        print("OUVINDO MENSAGEM 1")
        bytesSeremLidos = com.rx.getBufferLen(False)

        payload, lenPayload, messageType, ack = com.getData(bytesSeremLidos)
        print("messageType ", messageType)
        
        if messageType == 1:
            print("RECEBEU MENSAGEM 1")
            ouvindoMensagem1 = False
            break
        
        else:
            continue


    while ouvindoMensagem3:
        print("OUVINDO MENSAGEM 3")
        com.sendData(None,2)
        print("MANDOU MENSAGEM 2")
    

    
        bytesSeremLidos = com.rx.getBufferLen(True)
        if bytesSeremLidos == 0:
            print("ERRO TIPO II: NÃO RECEBEU MENSAGEM 3")
        payload, lenPayload, messageType, ack = com.getData(bytesSeremLidos)

        if messageType == 3:
            print("RECEBEU MENSAGEM 3")
            ouvindoMensagem3 = False
            print("OUVINDO MENSAGEM 4")
            break
        
        else:
            continue

    while ouvindoMensagem4:
        print("OUVINDO MENSAGEM 4")
        com.sendData(None,3)
        print("MANDOU MENSAGEM 3")
    

    
        bytesSeremLidos = com.rx.getBufferLen(True)

        payload, lenPayload, messageType, ack = com.getData(bytesSeremLidos)

        if ack == True:
            print("Recebeu tudo certo")
            print("ENVIANDO MENSAGEM TIPO 5: ACKNOWLEDGE")
            com.sendData(None,5)
            ouvindoMensagem4 = False
            break
        
        else:
            print("ERRO NA TRANSMISSÃO – MANDE DE NOVO")
            print("ENVIANDO MENSAGEM TIPO 6: NACKNOWLEDGE")
            com.sendData(None,6)
            ouvindoMensagem4 = False
            continue

    while ouvindoMensagem4:
        
    
        bytesSeremLidos = com.rx.getBufferLen(False)
        

        if messageType == 3:
            print("RECEBEU MENSAGEM 3")
            ouvindoMensagem3 = False
            print("OUVINDO MENSAGEM 4")
            break
        
        else:
            continue

    time.sleep(5)
    
    print("-------------------------")
    print("Comunicacao encerrada")
    print("-------------------------")
    
    com.sendData(None,7)
    print("MANDOU MENSAGEM TIPO 7")
    time.sleep(2)
    com.disable()
    rxBuff = io.BytesIO(payload)
    img = Image.open(rxBuff)
    draw = ImageDraw.Draw(img)
    img.show()





    '''
    bytesSeremLidos = None
    while time.time() < SentMessage1 + 5 or bytesSeremLidos != None:
        bytesSeremLidos=com.rx.getBufferLen()
    if bytesSeremLidos != None:
        resultData, resultDataLen, messageType = com.getData(bytesSeremLidos)
        if messageType == 2:
            ouvindoresposta1 = False
            print("comunicacao aberta")
            break
    print("Resposta do servidor não recebida, reenvio do mensagem de tipo 1")

'''
    print("Enviando mensagem para confirmar que ouviu")
    com.sendData(None,3)

    time.sleep(2)

    #print("tentado transmitir .... {} bytes".format(txLen))
    com.sendData(payload,4)





print("comecou")

from enlace import *
import time
from PIL import Image,ImageDraw
import io,os


# voce deveradescomentar e configurar a porta com atraves da qual ira fazer a
# comunicacao
# Serial Com Port
#  para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem1421" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)



print("porta COM aberta com sucesso")



def main():


    com = enlace(serialName)

    # Ativa comunicacao
    #com.enable()

    sistemaRecebimento(com)
    #verificar que a comunicacao foi aberta
    print("comunicacao aberta")

    '''


    # Faz a recepcao dos dados

    #A FAZER: listener de pacotes
    #SE RECEBEU 1,

     com.sendData(None, 2)
    

    SentMessage2 = time.time()

    while time.time() < SentMessage2 + 5:
        resultData, resultDataLen, messageType = com.getData();
        if messageType == 3:
            pass

        #A FAZER: receber message3
        #SE RECEBIDO: goto recebendo dados

    if time.time() > SentMessage2 + 5:
        com.sendData(None, 9)
    

    #confirmar que se trata de message4



    #A FAZER: LISTENER MENSAGEM
    #SE recebeu Message7, goto ComEnd
    '''
    # Encerra comunicacao
    '''
    print("-------------------------")
    print("Comunicacao encerrada")
    print("-------------------------")
    com.disable()
    rxBuff = io.BytesIO(rxBuffer)
    img = Image.open(rxBuff)
    draw = ImageDraw.Draw(img)
    img.show()
    #img.save('/home/francisco/Documentos/Insper /Semestre4/Camada Física da Computação/Projeto02/SalvarArquivo/ImagemEnviadaFinal.jpg')
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
    '''
if __name__ == "__main__":
    main()
