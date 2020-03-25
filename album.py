import numpy as np
import collections as clt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', help='Quantidade de cromos para completar o álbum', default=682, type=int)
parser.add_argument('-n', help='Quantidade de cromos por pacote', default=5, type=int)
parser.add_argument('-m', help='Número de experimentos que deseja realizar', default=10000, type=int)
args = parser.parse_args()


# especificações do álbum
N = 682#args.N # Tamanho do album
n = 5 # args.n # Tamanho do pacote
n_albums = 1000 # args.m
pacotes = []
decks = []

print("\n\n Processando...")
for i in range(n_albums):
    album = set( range(1,N+1) ) # estrutura do album
    pacotes.append(0)
    decks.append( clt.Counter() )
    while len(album) > 0:
        pacote = np.random.randint( 1,N+1, size=n )
        decks[-1] += clt.Counter( pacote )
        album -= set( pacote )
        pacotes[-1] += 1
print( "Ok.")

print("\n\n Em média são necessários {pacotes} pacotes para completar uma álbum".format( pacotes=np.mean(pacotes) ) )