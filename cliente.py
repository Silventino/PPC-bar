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
        while (not self.gerenciador.fechouBar):
            # self.gerenciador.novaRodada.clear()
            if(self.fazPedido()):
                self.qntBebidasRecebidas += 1
                self.esperarAtendimento.wait()
                self.consomePedido()
            else:
                print('Cliente {} esperando nova rodada'.format(self.id))
                self.gerenciador.novaRodada.wait()
        print('Cliente {} saindo'.format(self.id))


    def fazPedido(self):
        self.gerenciador.semaforo.acquire()
        if(self.qntBebidasRecebidas <= self.gerenciador.rodada):
            self.gerenciador.clientesEsperandoAtendimento.append(self)
            self.gerenciador.semaforo.release()
            return True
        self.gerenciador.semaforo.release()
        return False
    
    def consomePedido(self):
        t = random() * 10
        print("cliente " + str(self.id) + " bebendo [" + str(t) + "]")
        sleep(t)
        self.esperarAtendimento.clear()