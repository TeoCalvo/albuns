import numpy as np
import collections as clt
import itertools as it

class Colecao:
    def __init__(self, len_album, len_pacote):
        self.len_album = len_album
        self.len_pacote = len_pacote
        self.album = set( range(1,len_album+1) ) # Criando o album
        self.deck = clt.Counter() # Definindo o baralho vazio
        self.qtd_pacotes = 0 # Iniciando a quantidade de pacotinhos comprados

    def compra(self):
        pacote = clt.Counter( np.random.randint( 1, self.len_album + 1, size = self.len_pacote ) ) # Realiza a compra de um pacote
        self.qtd_pacotes += 1
        for p in pacote:
            try:
                self.album.remove(p)
                pacote[p] -= 1
            except KeyError:
                pass
        self.deck += pacote

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

# Definindo coleções
quantidade_rodadas = 1000
participantes = 3
pacotes = []

for i in range(quantidade_rodadas):
    colecoes = [ Colecao(682, 5) for i in range(participantes) ]
    trocas = [ Troca(i,j) for i,j in it.combinations( colecoes, 2 ) ]
    while sum( [ len( c.album ) for c in colecoes ] ) > 0:
        
        for c in colecoes:
            c.compra()
        
        for t in trocas:
            t.make_troca()
    pacotes.append( colecoes[0].qtd_pacotes )
