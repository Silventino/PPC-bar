from threading import Thread, Semaphore, Event
# from termcolor import colored
from cliente import Cliente
from garcom import Garcom
from time import sleep


class Gerenciador(Thread):
    def __init__(self, numClientes, numGarcons, capacidadeAtendimentoGarcons, numRodadas):
        Thread.__init__(self)
        
        self.fechouBar = False
        self.numClientes = numClientes
        self.numGarcons = numGarcons
        self.capacidadeAtendimentoGarcons = capacidadeAtendimentoGarcons
        self.numRodadas = numRodadas
        self.rodada = 0

        self.semaforo = Semaphore()                             # semaforo que impede que outros clientes entrem na fila de espera quando os garcons estao servindo
        self.semaforoGarcons = Semaphore()                      # semaforo que controla o acesso dos garçons aos atributos do gerenciador
        self.novaRodada = Event()                               # evento que sinaliza uma nova rodada de bebidas gratis
        self.todosForamAtendidos = Event()                      # evento que faz o gerenciador esperar todos serem atendidos antes de iniciar uma nova rodada

        self.qntClientesRodadaAtual = 0                         # registra quantos clientes participarao da rodada atual
        self.clientesAtendidosNaRodada = 0                      # registra quantos clientes ja foram atendidos na rodada atual
                                                                # quando esses numeros forem iguais, acabou uma rodada

        self.clientesEsperandoAtendimento = []                  # lista de clientes que entrarao para a rodada de bebidas. Ele é esvaziada a cada rodada.

        self.clientes = []                                      # todos os clientes
        for i in range(numClientes):
            c = Cliente(self, i)
            self.clientes.append(c)

        self.garcons = []                                       # todos os garçons
        for i in range(numGarcons):
            g = Garcom(self, i, self.capacidadeAtendimentoGarcons)
            self.garcons.append(g)
    
    def temClienteNoBar(self):                                  # teste simples para saber se ainda tem clientes sendo atendidos
        if(len(self.clientes) > 0):
            return True                                         
        return False                                            # quando retornar false, os garçons poderão ir embora
    
    def run(self):
        while not self.fechouBar:                               
            self.semaforo.release()
            self.novaRodada.clear()
            print("Rodada " + str(self.rodada) + " em 10s")
            sleep(10)
            self.semaforo.acquire()                             # assim que começa uma rodada, esse semaforo é fechado e impede que novos clientes entrem na fila
            s = ""                                              # eles terão que esperar a proxima rodada para serem atendidos
            for c in self.clientesEsperandoAtendimento:
                s += str(c.id)
                s += " "
            print("Fechou rodada " + str(self.rodada) + ". Clientes a ser atendidos = " + s)
            self.qntClientesRodadaAtual = len(self.clientesEsperandoAtendimento)
            self.incrementaRodada()
            self.novaRodada.set()                               # inicia uma nova rodada
            self.todosForamAtendidos.wait()                     # espera todo mundo ser atendido
        
        


    def startClientes(self):
        for i in range(self.numClientes):
            self.clientes[i].start()

    def startGarcons(self):
        for i in range(self.numGarcons):
            self.garcons[i].start()
    
    def incrementaRodada(self):
        self.semaforo.acquire()
        self.rodada += 1
        self.clientesAtendidosNaRodada = 0
        if(self.rodada >= self.numRodadas):
            self.fechouBar = True
            print("O BAR FECHOU")
        self.semaforo.release()





