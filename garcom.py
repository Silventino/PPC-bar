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
            self.gerenciador.novaRodada.wait()
            if(self.recebeMaximoPedidos()):
                self.registraPedidos()
                self.entregaPedidos()

    def recebeMaximoPedidos(self):
        self.gerenciador.semaforoGarcons.acquire()
        
        numClientesAtender = min(len(self.gerenciador.clientesEsperandoAtendimento), self.capacidadeDeAtendimento)
        if(numClientesAtender == 0):
            self.gerenciador.semaforoGarcons.release()
            return False
            
        for i in range(numClientesAtender):
            self.clientesParaAtender.append(self.gerenciador.clientesEsperandoAtendimento.pop(0))
            
        self.gerenciador.semaforoGarcons.release()
        return True

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
            


