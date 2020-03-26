import numpy as np
import collections as clt
import itertools as it
from scipy.stats import norm
import random
import argparse
import matplotlib.pyplot as plt

class Colecao:
    def __init__(self, len_album, len_pacote, media_compra, desvio_compra):
        self.len_album = len_album
        self.len_pacote = len_pacote
        self.album = set( range(1,len_album+1) ) # Criando o album
        self.deck = clt.Counter() # Definindo o baralho vazio
        self.qtd_pacotes = 0 # Iniciando a quantidade de pacotinhos comprados
        self.dist = norm( media_compra, desvio_compra )

    def compra(self):
        if len(self.album) == 0:
            return None
        pacote = clt.Counter( np.random.randint( 1, self.len_album + 1, size = self.len_pacote ) ) # Realiza a compra de um pacote
        self.qtd_pacotes += 1
        for p in pacote:
            try:
                self.album.remove(p)
                pacote[p] -= 1
            except KeyError:
                pass
        self.deck += pacote

    def compra_n(self):
        n = int( self.dist.rvs() )
        n = n+1 if n <= 1 else 2
        for i in range(1,n):
            self.compra()

class Troca:
    def __init__(self, col_1, col_2):
        self.col_1 = col_1
        self.col_2 = col_2

    def check_deck_album( self, deck, album ):
        return set( deck ) & album

    def check_troca(self):
        self.check_1 = self.check_deck_album( self.col_1.deck, self.col_2.album )
        self.check_2 = self.check_deck_album( self.col_2.deck, self.col_1.album )
        return min( [len(self.check_1), len(self.check_2)] )

    def make_troca(self):
        for i in range( self.check_troca() ):
            self.col_1.deck[ list(self.check_1)[i] ] -= 1
            self.col_2.album -= set( [list(self.check_1)[i]] )
            self.col_1.deck -= clt.Counter()

            self.col_2.deck[ list(self.check_2)[i] ] -= 1
            self.col_1.album -= set( [list(self.check_2)[i]] )
            self.col_2.deck -= clt.Counter()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-N", help="Quantidade de cromos para completar um album", type=int)
    parser.add_argument("-n", help="Quantidade de cromos em um pacote", type=int)
    parser.add_argument("-p", help="Quantidade de participantes na brincadeira", type=int)
    parser.add_argument("--turnos", help="Quantidade de turnos para exeperimentação", type=int)
    args = parser.parse_args()

    # Definindo coleções
    quantidade_rodadas = args.turnos
    participantes = args.p
    pacotes = []

    medias = [np.random.randint(4, 151) for i in range(participantes)]
    desvios = [np.random.randint(1, min( [10, i/2] )) for i in medias ]

    for i in range(quantidade_rodadas):
        colecoes = [ Colecao(args.N, args.n, medias[i], desvios[i]) for i in range(participantes) ]
        trocas = [ Troca(i,j) for i,j in it.combinations( colecoes, 2 ) ]
        while sum( [ len( c.album ) for c in colecoes ] ) > 0:
            
            for c in colecoes:
                c.compra_n()
            
            random.shuffle( trocas )
            for t in trocas:
                t.make_troca()

        pacotes.extend( [c.qtd_pacotes for c in colecoes] )

plt.hist(pacotes, bins=50)
plt.grid(True)
plt.show()
print(np.mean(pacotes))