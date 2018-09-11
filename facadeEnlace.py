from PIL import Image,ImageDraw
import io,os

EOP = b'/00/00/00/00'
stuffingByte = b'/7a/'


def int_to_byte(values, length):
    result = []
    for i in range(0,length):
        result.append(values >> (i*8)& 0xff)

    result.reverse()

    return bytes(result)

def fromByteToInt(bytes):
    result=0

    for b in bytes:
        result=result*256+int(b)

    return result


def encapsulate(payload, messageType):


    if payload != None:
        txLen = len(payload)
    else:
        txLen = len(int_to_byte(0,1))

    print('txLen: ',txLen)
    '''
        Head = 26 bytes:
            tipo de msg: 1 byte
            pacote atual: 2 bytes
            numero de pacotes: 2bytes
            payloadLen = 5 bytes
            EOP = 12 bytes
            stuffing = 4 bytes
    '''
    payloadfinal = bytes()
    print("EOP stuffing: ",len(stuffingByte))
    if payload != None:
        for i in range(0, len(payload)):
            if EOP == payload[i:i+13]:
                payloadfinal+=stuffingByte
                payloadfinal+=payload[i:i+1]
            else:
                payloadfinal+=payload[i:i+1]
    else:
        payloadfinal = int_to_byte(0,1)

    payloadLen = int_to_byte(txLen,5)

    if messageType == 1:
        head = int_to_byte(1,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Cliente manda pedido de comunicação para servidor
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 2:
        head = int_to_byte(2,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Servidor responde cliente dizendo que recebeu mensagem tipo 1
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 3:
        head = int_to_byte(3,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Cliente responde servidor dizendo que recebeu mensagem tipo 2
        #e servidor sabe que a próxima mensagem é tipo 4
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 4:
        sad = 0
        #Cliente faz efetivamente transmissão para servidor
        listOfPackages = []
        if (len(payload)%90)==0 :
            packTotal =int(len(payload)/90)
        else:
            packTotal =int(1+(len(payload)//90))
        print("packTotal: ",packTotal)
        a = 0
        for i in range(0,packTotal):
            payloadfinal = payload[i*90:(i*90)+90]
            payloadLen = int_to_byte(len(payloadfinal),5)

            head = int_to_byte(4,1)+int_to_byte(i,2)+int_to_byte(packTotal,2)+payloadLen+EOP+stuffingByte

            all = bytes()
            all += head
            all += payloadfinal
            all += EOP
            if a == 0:
                print("messageType   : ",int_to_byte(4,1))
                print("actual package: ",int_to_byte(i,2))
                print("Total packages: ",int_to_byte(packTotal,2))
                print("payloadlen    : ",payloadLen)
                print("EOP           : ",EOP)
                print("stuffingByte  : ",stuffingByte)
            listOfPackages.insert(a,all)
            a+=1


        return listOfPackages

    elif messageType == 5:
        head = int_to_byte(5,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #acknowledge do servidor para cliente confirmando recebimento
        #correto do payload
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 6:
        head = int_to_byte(6,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #nacknowledge do servidor para cliente pedindo reenvio do pacote por
        #erro de transmissão
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 7:
        head = int_to_byte(7,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Pedido de encerramento da mensagem
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 8:
        head = int_to_byte(8,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Erro tipo  1: cliente não recebeu mensagem tipo 2
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 9:
        head = int_to_byte(9,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Erro tipo 2: servidor não recebeu mensagem tipo 3
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    elif messageType == 0:
        head = int_to_byte(0,1)+int_to_byte(0,2)+int_to_byte(0,2)+payloadLen+EOP+stuffingByte
        #Erro tipo 3: não recebeu ack ou nack em 5 segundos
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all
    else:
        head = None
        #messageType fora do protocolo e portanto byte não deve ser formado com HEAD
        all = bytes()
        all += head
        all += payloadfinal
        all += EOP

        return all





def readHeadNAll(receivedAll):
    #print(receivedAll)

    head = receivedAll[0:26]
    messageType = fromByteToInt(head[0:1])
    actualPackage = fromByteToInt(receivedAll[1:3])+1
    totalPackage = fromByteToInt(receivedAll[4:5])
    txLen = fromByteToInt(head[5:10])
    eopSystem = head[10:22]
    stuffByte = head[22:26]

    print(txLen)

    #Leitura do messaType do pacote recebido

    #print("Pacote ",actualPackage," de um total de ",totalPackage)

    sanityCheck = bytearray()
    stuffByteCount = 0
    ack = False

    for i in range(26, len(receivedAll)):
        if receivedAll[i:i+1] == stuffByte:
            sanityCheck += receivedAll[i+1:i+14]
            i +=14
        elif eopSystem == receivedAll[i:i+13]:
            #print('EOP: ',receivedAll[i:i+13])
            break

        else:
            sanityCheck += receivedAll[i:i+1]
            #print("\n yep")
            #print(sanityCheck)
            #print("VERIFICANDO PACOTE RECEBIDO")


    #print('SanityCheck ', sanityCheck)
    if len(sanityCheck) == txLen:

        #print ("sanityCheck = okay")
        ack = True

        return sanityCheck, txLen, messageType, ack, actualPackage, totalPackage

    else:

        #print("Ue")

        return None, None, messageType, ack ,None, None



def teste():
    img = Image.open('circuit.jpg', mode='r')
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()
    testeSubject = encapsulate(imgByteArr,4)
    #receaved, txLenRead, msgTupe = readHeadNAll(testeSubject)
    list = b''
    for i in range(0,len(testeSubject)):
        sanityCheck, txLen, messageType, ack, actualPackage, totalPackage = readHeadNAll(testeSubject[i])
        print(actualPackage," de ",totalPackage)
        list+=sanityCheck
    print(list==imgByteArr)
    '''
    print("Mensagem do tipo: ",msgTupe)
    print("\nFoi enviado um byte no payload igual a: ",int_to_byte(0,1)," e foi recebido um byte igual a: ",receaved)
'''
#print(fromByteToInt(int_to_byte(10000,2)))
teste()
