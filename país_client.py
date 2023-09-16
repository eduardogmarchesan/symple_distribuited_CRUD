import socket
import sys
from unidecode import unidecode


class pais:
    def __init__(self, nome, capital, lingua, populacao, area):
        self.nome = nome
        self.capital = capital
        self.lingua = lingua
        self.populacao = populacao
        self.area = area 

    def __str__ (self):
        return f'\nPaís: {self.nome}\nCapital: {self.capital}\nLíngua: {self.lingua}\nPopulação: {self.populacao}\nÁrea: {self.area}\n'

def error():
    print('Erro de conexão')
    sys.exit(-1)

def envia(info):
    info  = unidecode(info)
    info = info.lower()
        
    info = info.encode()
    tam = len(info)
    tam = tam.to_bytes(length=1, byteorder='big', signed=False)

    socketDados.send(op.encode() + tam + info)

def recebe():
    tamByte = socketDados.recv(1)
    if not tamByte: error()

    tam = int.from_bytes(tamByte, byteorder='big', signed=False)
    infoBytes = socketDados.recv(tam)

    if not infoBytes : error()
    return infoBytes.decode()


def cria_pais(infoPais):
    info = infoPais.split("*")
    pais1 = pais(info[0],info[1],info[2],int(info[3]),int(info[4]))
    return pais1

socketDados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = ('127.0.0.1',55001)
socketDados.connect(destino)



op = None

while op != '5':

    op = input('Digite: \n1 para Adicionar um País\n2 para buscar um país\n3 para alterar a informação de um país\n4 para deletar um país\n5 para sair\n')

    if op == '1':
        nome = input('Digite o nome do país: ')
        capital = input('Digite a capital do país: ')
        lingua = input('Digite a língua oficial do país: ')
        populacao = input('Digite a população do país: ')
        area = input('Digite a área do país: ')

        info = str(nome) + '*' +  str(capital) + '*' + str(lingua) + '*' + str(populacao) + '*' + str(area)
        envia(info)

        ack = recebe()

        print("\n"+ ack)

    elif op == '2': #read

        info = input('Digite o nome do país a ser buscado: ')
        envia(info)

        info = recebe()
        if info == '-1':
            print('\nPaís não encontrado\n')
            continue
        elif info == '-2':
            print('\nerro ao buscar pais\n')
            continue


        paisAt = cria_pais(info)
        print(paisAt)

    
    elif op == '3':     #update
        nome = input('Digite o nome do país que deseja alterar: ')
        opA = input('\nDigite:\n1 para alterar o nome\n2 para alterar a capital\n3 para alterar a língua\n4 para alterar a populaçao\n5 para alterar a area\n')
        nInfo = input('Nova informação:')

        info = str(nome) + '*' + str(opA) + '*' + str(nInfo)

        envia (info) 

        ack = recebe()
        print("\n"+ ack)

    elif op =='4':  #delete
        nome = input('Digite o nome do país que deseja excluir: ')
        confirmation = input("Você tem certeza que deseja excluir o(a) " + nome +"?  Digite 's' ou 'n' ")
        confirmation = confirmation.lower()
        if confirmation != 's' : continue

        envia(nome)
        ack = recebe()

        print("\n"+ ack)
    elif op == '5': envia("encera")

socketDados.close()
