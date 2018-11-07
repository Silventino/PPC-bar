from threading import Thread, Semaphore, Event
# from termcolor import colored
from cliente import Cliente
from garcom import Garcom
from time import sleep


class Gerenciador(Thread):
    def __init__(self, numClientes, numGarcons, capacidadeAtendimentoGarcons, numRodadas):
        Thread.__init__(self)
        
        self.fechouBar = False
        #~ self.existemClientesNoBar = True
        self.numClientes = numClientes
        self.numGarcons = numGarcons
        self.capacidadeAtendimentoGarcons = capacidadeAtendimentoGarcons
        self.numRodadas = numRodadas
        self.rodada = 0
        self.semaforo = Semaphore()
        self.semaforoGarcons = Semaphore()
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
    
    def run(self):
        while not self.fechouBar:
            self.semaforo.release()
            self.novaRodada.clear()
            print("Rodada " + str(self.rodada) + " em 10s")
            sleep(10)
            self.semaforo.acquire()
            s = ""
            for c in self.clientesEsperandoAtendimento:
                s += str(c.id)
                s += " "
            print("Fechou rodada " + str(self.rodada) + ". Clientes a ser atendidos = " + s)
            self.incrementaRodada()
            self.novaRodada.set()
        
        


    def startClientes(self):
        for i in range(self.numClientes):
            self.clientes[i].start()

    def startGarcons(self):
        for i in range(self.numGarcons):
            self.garcons[i].start()
    
    def incrementaRodada(self):
        self.semaforo.acquire()
        self.rodada += 1
        if(self.rodada >= self.numRodadas):
            self.fechouBar = True
            print("O BAR FECHOU")
        self.semaforo.release()





