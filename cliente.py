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
        t = random() * 10
        sleep(t)
        print("Cliente " + str(self.id) + " entrou no bar")
        while (not self.gerenciador.fechouBar):                 # enquanto o bar está aberto
            self.fazPedido()                                    # se coloca na fila de espera para atendimento
            self.esperarAtendimento.wait()                      # espera a bebida chegar              
            self.consomePedido()                                # consome a bebida
        self.gerenciador.clientes.remove(self)                  # quando o bar fecha, o cliente se retira da lista de clientes
        print('Cliente {} saindo'.format(self.id))


    def fazPedido(self):
        self.gerenciador.semaforo.acquire()
        self.gerenciador.clientesEsperandoAtendimento.append(self)
        self.gerenciador.semaforo.release()
    
    def consomePedido(self):
        t = random() * 10                                       # demora um tempo entre 0 e 10s para beber o drink
        print("cliente " + str(self.id) + " bebendo [" + str(t) + "]")
        sleep(t)
        self.esperarAtendimento.clear()
