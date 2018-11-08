from gerenciador import Gerenciador
import sys

def main():
    if len(sys.argv) != 5:
        print('{} <num_clientes> <num_garçons> <capacidade_garçom> <num_rodadas>'.format(sys.argv[0]))
        exit(-1)

    g = Gerenciador(
        int(sys.argv[1]), # num clientes
        int(sys.argv[2]), # num garçons
        int(sys.argv[3]), # capacidade garçom
        int(sys.argv[4])  # num rodadas
    )
    g.startGarcons()
    g.startClientes()
    g.start()

main()
