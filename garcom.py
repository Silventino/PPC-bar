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
        while self.gerenciador.temClienteNoBar():                                                                   # enquanto existem client
            self.gerenciador.semaforoGarcons.acquire()                                                              

            if(self.gerenciador.clientesAtendidosNaRodada == self.gerenciador.qntClientesRodadaAtual):              # se ja atendemos todos os clientes da rodada:
                if(self.gerenciador.fechouBar):                                                                     # checamos se o bar ja fechou
                    return                                                                                          # se estiver fechado, garcom vai embora
                self.gerenciador.todosForamAtendidos.set()                                                          # se estiver aberto, informamos que todos foram atendidos
                self.gerenciador.semaforoGarcons.release()                                                          # para que uma nova rodada começe
                self.gerenciador.novaRodada.wait()

            self.gerenciador.semaforoGarcons.release()
            if(self.recebeMaximoPedidos()):                                                                         # se conseguiu receber clientes da fila:
                self.registraPedidos()                                                                              # registra os pedidos
                self.entregaPedidos()                                                                               # após um tempo de preparo, entrega os pedidos


    def recebeMaximoPedidos(self):
        self.gerenciador.semaforoGarcons.acquire()
        
        numClientesAtender = min(len(self.gerenciador.clientesEsperandoAtendimento), self.capacidadeDeAtendimento)  # o num de clientes a atender é a capacidade do garcom
                                                                                                                    # ou o restante da fila de espera (o que for menor)
        if(numClientesAtender == 0):                                                                                # se esse numero for 0, o garçom nao precisa fazer pedidos                                                              
            self.gerenciador.semaforoGarcons.release()
            return False
            
        for i in range(numClientesAtender):                                                                         # se nao for 0, o garcom atende cada cliente
            self.clientesParaAtender.append(self.gerenciador.clientesEsperandoAtendimento.pop(0))                   # colocando-os na sua lista de clientes
            
        self.gerenciador.semaforoGarcons.release()
        return True

    def registraPedidos(self):
        s = ""
        for c in self.clientesParaAtender:
            self.gerenciador.semaforoGarcons.acquire()
            self.gerenciador.clientesAtendidosNaRodada += 1                             # incrementa os clientes atendidos
            self.gerenciador.semaforoGarcons.release()

            s += str(c.id)
            s += " "
        print("Garçom " + str(self.id) + " registrando pedidos dos clientes: " + s)
        sleep(2)                                                                        # demora 2s para pedir as bebidas ao bartender
    
    def entregaPedidos(self):
        for cliente in self.clientesParaAtender:
            print("cliente " + str(cliente.id) + " recebeu pedido")
            cliente.esperarAtendimento.set()                                            # entrega a bebida ao cliente
        self.clientesParaAtender.clear()
            


