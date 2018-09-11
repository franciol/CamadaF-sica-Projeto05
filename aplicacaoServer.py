
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Fisica da Computacao
# Carareto
# 17/02/2018
# Aplicacao SERVIDOR
# Aveiro & Otofuji
# 13 de setembro de 2018
####################################################

from enlace import *
import time
from PIL import Image,ImageDraw
import io,os


####################################################
# CHECK DE PORTAS:
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta
####################################################

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem1421" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)

####################################################

def fromByteToInt(bytes):
    result=0

    for b in bytes:
        result=result*256+int(b)

    return result

def sistemaRecebimento(com):
    com.enable()
    print("porta COM aberta com sucesso")

    ouvindoMensagem1 = True
    ouvindoMensagem3 = True
    ouvindoMensagem4 = True
    pacoteAtual = 0
    esperandoPacotes = 0
    InsperTor = 1 
    comecou = False
    erro4 = 0

    while ouvindoMensagem1:
        
        print("OUVINDO MENSAGEM 1")
        bytesSeremLidos = com.rx.getBufferLen(False)

        payload, lenPayload, messageType, ack, numeroPacote, totalPacote = com.getData(bytesSeremLidos)
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
            payload, lenPayload, messageType, ack, numeroPacote, totalPacote = com.getData(bytesSeremLidos)

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
            payload, lenPayload, messageType, ack, numeroPacote, totalPacote = com.getData(bytesSeremLidos)

            if numeroPacote == 1:
                pacoteAtual = numeroPacote
                esperandoPacotes = totalPacote
                comecou = True
                InsperTor += 1 


            else:
                if esperandoPacotes == totalPacote:
                    if comecou == True:
                        if InsperTor == numeroPacote:
                            continue
                        else:
                            if erro4 <= 3:
                                print("ERRO TIPO 4: PACOTE INESPERADO")
                                print("ERRO NA TRANSMISSÃO – MANDE DE NOVO")
                                print("ENVIANDO MENSAGEM TIPO 6: NACKNOWLEDGE")
                                com.sendData(None,6)
                                ouvindoMensagem4 = False
                                InsperTor = 1
                                pacoteAtual = 0
                                esperandoPacotes = 0
                                comecou = False
                                erro4 += 1
                                break
                           
                            else:
                                ouvindoMensagem4 = False
                                InsperTor = 1
                                pacoteAtual = 0
                                esperandoPacotes = 0
                                comecou = False

                                com.sendData(None,7)
                                print("MANDOU MENSAGEM TIPO 7")
                                time.sleep(4)
                                com.disable()
                                print("-------------------------")
                                print("ERRO FATAL DESCONHECIDO – RECOMECE TRANSMISSÃO")
                                print("-------------------------")


                else:
                    ouvindoMensagem4 = False
                    InsperTor = 1
                    pacoteAtual = 0
                    esperandoPacotes = 0
                    comecou = False

                    com.sendData(None,7)
                    print("MANDOU MENSAGEM TIPO 7")
                    time.sleep(4)
                    com.disable()
                    print("-------------------------")
                    print("ERRO FATAL DESCONHECIDO – RECOMECE TRANSMISSÃO")
                    print("-------------------------")

                pacoteAtual = numeroPacote

            if ack == True:
                print("Recebeu tudo certo")
                print("ENVIANDO MENSAGEM TIPO 5: ACKNOWLEDGE")
                arquivo += payload
                print("Pacote número ", pacoteAtual, " recebido, contendo payload de ", len(payload), " bytes")
                print(InsperTor, " pacotes recebidos de um total de ", esperandoPacotes)
                InsperTor += 1
                com.sendData(None,5)
                ouvindoMensagem4 = False
                break
            
            else:
                print("ERRO NA TRANSMISSÃO – MANDE DE NOVO")
                print("ENVIANDO MENSAGEM TIPO 6: NACKNOWLEDGE")
                com.sendData(None,6)
                ouvindoMensagem4 = False
                continue


        time.sleep(5)

        if pacoteAtual == esperandoPacotes:
            comecou == False
            print("Tamanho total do payload do arquivo recebido: " len(arquivo))
            break

        else:
            print("Recomeçando protocolo de comunicação para receber o pacote número ", InsperTor)
            continue


        
    
    time.sleep(2)
    com.sendData(None,7)
    print("MANDOU MENSAGEM TIPO 7")
    time.sleep(2)
    com.disable()
    print("-------------------------")
    print("Comunicacao encerrada")
    print("-------------------------")
    rxBuff = io.BytesIO(arquivo)
    img = Image.open(rxBuff)
    draw = ImageDraw.Draw(img)
    img.show()



def main():

    com = enlace(serialName)
    sistemaRecebimento(com)
    
if __name__ == "__main__":
    main()



























