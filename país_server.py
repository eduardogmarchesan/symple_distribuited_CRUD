import socket
import sys
from unidecode import unidecode
#1 create
#2 read
#3 update
#4 delete
#5 close connection

class pais:
    def __init__(self, nome, capital, lingua, populacao, area):
        self.nome = nome
        self.capital = capital
        self.lingua = lingua
        self.populacao = populacao
        self.area = area 

    def __str__ (self):
        return f'\nPaís: {self.nome}\nCapital: {self.capital}\nLíngua: {self.lingua}\nPopulação: {self.populacao}\nÁrea: {self.area}\n'

def cria_pais(infoPais):
    info = infoPais.split("*")
    pais1 = pais(info[0],info[1],info[2],int(info[3]),int(info[4]))
    return pais1

def error():
    print('Erro de conexão')
    sys.exit(-1)

def recebe():
    tamByte = socketDados.recv(1)
    if not tamByte: error()

    tam = int.from_bytes(tamByte, byteorder='big', signed=False)
    infoBytes = socketDados.recv(tam)

    if not infoBytes : error()
    return infoBytes.decode()

def envia(info):
    info  = unidecode(info)
    info = info.lower()
        
    info = info.encode()
    tam = len(info)
    tam = tam.to_bytes(length=1, byteorder='big', signed=False)

    socketDados.send(tam + info)

def busca(nome,lista):
    for x in range (len(lista)):
        if lista[x].nome == nome:
            return (x)
        
    return -1


servidorConexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '127.0.0.1'
porta = 55001
endereco = (ip, porta)
servidorConexao.bind(endereco)

servidorConexao.listen(1)
[socketDados, dadosCliente] = servidorConexao.accept()

op = None
op = 1 
listaPais = []

while op != '5':

    op = (socketDados.recv(1)).decode()

    if op == '1':  #create

        try:

            info = recebe()   
            paisAt = cria_pais(info)

            indice = busca(paisAt.nome, listaPais)
            if indice != -1:
                envia("Um pais com esse nome já esta no servidor. pais não adicionado")
                continue
            listaPais.append(paisAt)
                
            ack = paisAt.nome + " adicionado com sucesso"

        except:
            envia("Ocorreu erro ao adicionar país, pais não adicinado")
            continue

        envia(ack)
        

    elif op == '2':  #read
        try:

            info = recebe()
            indice = busca(info, listaPais)
            if indice == -1:
                envia("-1")
                continue

            info = listaPais[indice].nome + "*" + listaPais[indice].capital + "*" + listaPais[indice].lingua + "*" + str(listaPais[indice].populacao) + "*" + str(listaPais[indice].area )
        except:
            envia("-2")
            continue

        envia(info)
       

    elif op == '3':   #update
        try:

            info = recebe()
            info = info.split("*")

            indice = busca(info[0],listaPais)
            if indice == -1:
                envia("Pais não encontrado")
                continue        

            opA = int(info[1])

            if opA > 3:
                infoA = int(info[2])
            else:
                infoA = info[2]

            if opA == 1:
                listaPais[indice].nome = infoA
            elif opA == 2:
                listaPais[indice].capital = infoA
            elif opA == 3:
                listaPais[indice].lingua = infoA
            elif opA == 4:
                listaPais[indice].populacao = infoA
            elif opA == 5:
                listaPais[indice].area = infoA
        
            ack = "Alteração realizada com sucesso\n"
        except:
            envia("Ocorreu erro ao atualizar informação")
            continue

        envia(ack)
    
    elif op == '4':  #delete
        try:

            info = recebe()
            indice = busca(info, listaPais)
            if indice == -1:
                envia("Pais não encontrado")
                continue  

            paisA = listaPais[indice].nome

            del listaPais[indice]

            ack = paisA + " removido com sucesso"
        except:
            envia("Ocorreu erro ao deletar pais")
            continue
            
        envia(ack)
                
socketDados.close()
servidorConexao.close()