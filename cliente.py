from threading import Thread, Semaphore, Event
from time import sleep
from random import random


class Cliente(Thread):
    def __init__(self, gerenciador, id):
        Thread.__init__(self)
        self.gerenciador = gerenciador
        self.esperarAtendimento = Event()
        self.id = id
        self.qntBebidasRecebidas = 0

    def run(self):
        t = random() * 10
        sleep(t)
        print("Cliente " + str(self.id) + " entrou no bar")
        while (not self.gerenciador.fechouBar):
            self.fazPedido()
            self.qntBebidasRecebidas += 1
            self.esperarAtendimento.wait()
            self.consomePedido()

        print('Cliente {} saindo'.format(self.id))


    def fazPedido(self):
        self.gerenciador.semaforo.acquire()
        #~ if(self.qntBebidasRecebidas <= self.gerenciador.rodada):
        self.gerenciador.clientesEsperandoAtendimento.append(self)
        self.gerenciador.semaforo.release()
    
    def consomePedido(self):
        t = random() * 10
        print("cliente " + str(self.id) + " bebendo [" + str(t) + "]")
        sleep(t)
        self.esperarAtendimento.clear()
