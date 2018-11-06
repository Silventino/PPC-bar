from threading import Thread, Semaphore, Event
from time import sleep
from random import random


class Cliente(Thread):
    def __init__(self, gerenciador, id):
        Thread.__init__(self)
        self.gerenciador = gerenciador
        self.esperarAtendimento = Event()
        self.id = id

    def run(self):
        while (not self.gerenciador.fechouBar):
            # self.gerenciador.novaRodada.clear()
            self.fazPedido()
            self.esperarAtendimento.wait()
            self.consomePedido()
            self.gerenciador.novaRodada.wait()
            if(self.gerenciador.fechouBar):
                print('Cliente {} saindo'.format(self.id))

    def fazPedido(self):
        self.gerenciador.semaforo.acquire()
        self.gerenciador.clientesEsperandoAtendimento.append(self)
        self.gerenciador.semaforo.release()
    
    def consomePedido(self):
        t = random() * 10
        print("cliente " + str(self.id) + " bebendo [" + str(t) + "]")
        sleep(t)
        self.esperarAtendimento.clear()