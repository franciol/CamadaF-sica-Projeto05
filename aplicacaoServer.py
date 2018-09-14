
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
serialName = "/dev/cu.usbmodem1411" # Mac    (variacao de)
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
    InsperTor = 0 
    comecou = False
    erro4 = 0
    arquivo = bytes()

    while ouvindoMensagem1:
        
        print("OUVINDO MENSAGEM 1")
        bytesSeremLidos = com.rx.getBufferLen(False)

        payload, lenPayload, messageType, ack, numeroPacote, totalPacote = com.getData(bytesSeremLidos)
        
        
        if messageType == 1:
            print("RECEBEU MENSAGEM 1")
            ouvindoMensagem1 = False
            
        
        else:
            continue


        while ouvindoMensagem3:
            
            print("OUVINDO MENSAGEM 3")
            com.sendData(facadeEnlace.encapsulate(None, 2))
            print("MANDOU MENSAGEM 2")
        
            bytesSeremLidos = com.rx.getBufferLen(True)
            if bytesSeremLidos == 0:
                print("ERRO TIPO II: NÃO RECEBEU MENSAGEM 3")
            payload, lenPayload, messageType, ack, numeroPacote, totalPacote = com.getData(bytesSeremLidos)

            if messageType == 3:
                print("RECEBEU MENSAGEM 3")
                ouvindoMensagem3 = False
                print("OUVINDO MENSAGEM 4")
                
            
            else:
                continue



        while ouvindoMensagem4:
            print("OUVINDO MENSAGEM 4")
            #com.sendData(facadeEnlace.encapsulate(None, 3))
            #print("MANDOU MENSAGEM 3")
        
            bytesSeremLidos = com.rx.getBufferLen(False)
            payload, lenPayload, messageType, ack, numeroPacote, totalPacote = com.getData(bytesSeremLidos)

            if numeroPacote == 1:
                pacoteAtual = numeroPacote
                esperandoPacotes = totalPacote
                comecou = True
                InsperTor += 1 


            else:
                if esperandoPacotes == totalPacote:
                    if comecou == True:
                        if InsperTor != numeroPacote:
                        
                            print("ERRO TIPO 4: PACOTE INESPERADO")
                            print("ERRO NA TRANSMISSÃO – MANDE DE NOVO")
                            print("ENVIANDO MENSAGEM TIPO 6: NACKNOWLEDGE")
                            com.sendData(facadeEnlace.encapsulate(None, 6))
                            ouvindoMensagem4 = False
                            InsperTor = 1
                            pacoteAtual = 0
                            esperandoPacotes = 0
                            comecou = False
                                

                else:
                    ouvindoMensagem4 = False
                    InsperTor = 1
                    pacoteAtual = 0
                    esperandoPacotes = 0
                    comecou = False

                    com.sendData(facadeEnlace.encapsulate(None, 7))
                    print("MANDOU MENSAGEM TIPO 7")
                    time.sleep(4)
                    com.disable()
                    print("-------------------------")
                    print("ERRO FATAL DESCONHECIDO – RECOMECE TRANSMISSÃO")
                    print("-------------------------")

                pacoteAtual = numeroPacote

            if ack == True:
                print("ENVIANDO MENSAGEM TIPO 5: ACKNOWLEDGE")
                arquivo += payload
                print("Pacote número ", pacoteAtual, " recebido, contendo payload de ", len(payload), " bytes")
                print(InsperTor, " pacotes recebidos de um total de ", esperandoPacotes)
                InsperTor += 1
                com.sendData(facadeEnlace.encapsulate(None, 5))
                
                
            
            else:
                print("ERRO NA TRANSMISSÃO – MANDE DE NOVO")
                print("ENVIANDO MENSAGEM TIPO 6: NACKNOWLEDGE")
                com.sendData(facadeEnlace.encapsulate(None, 6))
                
                continue


            time.sleep(5)

            if pacoteAtual == esperandoPacotes:
                comecou == False
                print("Tamanho total do payload do arquivo recebido: ", len(arquivo))
                time.sleep(5)
                com.sendData(facadeEnlace.encapsulate(None, 5))
                print("MANDOU MENSAGEM TIPO 7")
                time.sleep(5)
                com.disable()
                print("-------------------------")
                print("Comunicacao encerrada")
                print("-------------------------")
                rxBuff = io.BytesIO(arquivo)
                img = Image.open(rxBuff)
                draw = ImageDraw.Draw(img)
                img.show()
 

            else:
                print("Ouvindo pacote ", InsperTor)
                


        
    
    



def main():

    com = enlace(serialName)
    sistemaRecebimento(com)
    
if __name__ == "__main__":
    main()



























