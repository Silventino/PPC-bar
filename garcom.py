from threading import Thread, Semaphore, Event
from time import sleep

class Garcom(Thread):
    def __init__(self, gerenciador, id, capacidadeDeAtendimento):
        self.gerenciador = gerenciador
        self.ocupado = False
        self.id = id
        self.clientesParaAtender = []
        self.capacidadeDeAtendimento = capacidadeDeAtendimento
        Thread.__init__(self)

    def run(self):
        while not self.gerenciador.fechouBar:
            if(self.recebeMaximoPedidos()):
                self.registraPedidos()
                self.entregaPedidos()
                self.gerenciador.incrementaRodada()

    def recebeMaximoPedidos(self):
        self.gerenciador.semaforo.acquire()
        if(len(self.gerenciador.clientesEsperandoAtendimento) >= self.capacidadeDeAtendimento):
            for _ in range(self.capacidadeDeAtendimento):
                self.clientesParaAtender.append(self.gerenciador.clientesEsperandoAtendimento.pop())
            self.gerenciador.semaforo.release()
            return True
        else:
            self.gerenciador.semaforo.release()
            return False

    def registraPedidos(self):
        s = ""
        for c in self.clientesParaAtender:
            s += str(c.id)
            s += " "
        print("Garçom " + str(self.id) + " registrando pedidos dos clientes: " + s)
        sleep(2)
    
    def entregaPedidos(self):
        for cliente in self.clientesParaAtender:
            print("cliente " + str(cliente.id) + " recebeu pedido")
            self.gerenciador.semaforo.acquire()
            self.gerenciador.clientesAtendidosNaRodada += 1
            self.gerenciador.semaforo.release()
            cliente.esperarAtendimento.set()
        self.clientesParaAtender.clear()
            


