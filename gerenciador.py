from threading import Thread, Semaphore, Event
# from termcolor import colored
from cliente import Cliente
from garcom import Garcom
from time import sleep


class Gerenciador:
    def __init__(self, numClientes, numGarcons, capacidadeAtendimentoGarcons, numRodadas):
        self.fechouBar = False
        self.existemClientesNoBar = True
        self.numClientes = numClientes
        self.numGarcons = numGarcons
        self.capacidadeAtendimentoGarcons = capacidadeAtendimentoGarcons
        self.numRodadas = numRodadas
        self.rodada = 0
        self.semaforo = Semaphore()
        self.novaRodada = Event()
        self.clientesAtendidosNaRodada = 0

        self.clientesEsperandoAtendimento = []

        self.clientes = []
        for i in range(numClientes):
            c = Cliente(self, i)
            self.clientes.append(c)

        self.garcons = []
        for i in range(numGarcons):
            g = Garcom(self, i, self.capacidadeAtendimentoGarcons)
            self.garcons.append(g)


    def startClientes(self):
        for i in range(self.numClientes):
            self.clientes[i].start()

    def startGarcons(self):
        for i in range(self.numGarcons):
            self.garcons[i].start()
    
    def incrementaRodada(self):
        self.semaforo.acquire()
        self.novaRodada.clear()
        if(self.clientesAtendidosNaRodada == self.numClientes):
            self.rodada += 1
            # print(colored("FIM DA RODADA {}".format(self.rodada), 'red'))
            print("FIM DA RODADA {}".format(self.rodada))
            self.clientesAtendidosNaRodada = 0
            if(self.rodada == self.numRodadas):
                self.fechouBar = True
                # print(colored("FECHOU O BAR", 'red'))
                print("FECHOU O BAR")
                self.novaRodada.set()
                
            else:
                self.novaRodada.set()
        self.semaforo.release()





