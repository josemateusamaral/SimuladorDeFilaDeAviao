from classes import *
import time
import os
import random

class Assento:

    def __init__(self, numeroAssento):
        self.numero = numeroAssento
        self.ocupado = False

    def ocuparAssento(self, pessoa):
        self.passageiro = pessoa
        self.ocupado = True
   
class Classe:

    quantidadeAssentos = 72
    assentosPorFila = 8 

    def __init__(self,nome):
        self.nomeClasse = nome
        self.assentos = []
        self.assentosDisponiveis = []
        self.lotada = False

    def ocuparAssento(self,passageiro,numero = None):

        if self.assentosDisponiveis == []:
            self.lotada = True
            return

        if numero == None:
            numero = random.choice(self.assentosDisponiveis)

        for assento in self.assentos:
            if assento.numero == numero:
                assento.ocuparAssento(passageiro)

        self.assentosDisponiveis.remove(numero)

class Aviao:

    classesDisponiveis = ['1° Classe','2° Classe','Classe Economica']
    filas = ['A','B','C','D','E','F','G','H']

    def __init__(self):
        
        self.classes = []

        self.corredor = []
        for i in range( int(Classe.quantidadeAssentos / Classe.assentosPorFila) ):
            self.corredor.append('VAZIO')

        for classe in self.classesDisponiveis:
            
            x = 0
            y = 1
            classObj = Classe(classe)
            
            for assento in range(classObj.quantidadeAssentos):
                
                numeroAssento = f'{self.filas[x]}{y}' 
                x += 1
                if(x == len(self.filas)):
                    x = 0
                    y += 1

                classObj.assentosDisponiveis.append(numeroAssento)
                classObj.assentos.append(Assento(numeroAssento))
                print(numeroAssento)
            
            self.classes.append(classObj)

    def __str__(self):
        string = ''
        for classe in self.classes:
            string += f'\n\nCLASSE [{classe.nomeClasse}]'
            #string += f'\n    A    B    C    D   |  |   E    F    G    H  '
            string += f'\n\n   [A.][B.][C.][D.] | {self.corredor[0]} | [E.][F.][G.][H.]'
            contador = 0
            x = 1
            y = 1
            for assento in classe.assentos:
                if x == 1:
                    string += f'\n {y} '
                if assento.ocupado:
                    string += f'<{assento.passageiro.nome}>'
                else:
                    #string += '[   ]'
                    string += f'[{assento.numero}]'
                contador += 1
                if contador == int( classe.assentosPorFila / 2 ):
                    string += f' | {self.corredor[0]} | '
                x += 1
                if contador == classe.assentosPorFila:
                    contador = 0
                    y += 1
                    x = 1
        return string

aviao = Aviao()
print(aviao)

filaDeEmbarque = ['F6','A2','G4','B5']
contadorEntrada = 0

for classe in aviao.classes:

    while not classe.lotada and filaDeEmbarque != []:

        nome = ''
        if(contadorEntrada < 10):
            nome = '0' + str(contadorEntrada)
        else:
            nome = str(contadorEntrada)
        
        posicao = filaDeEmbarque.pop(0)
        passageiro = Pessoa(nome,posicao)
        classe.ocuparAssento( passageiro = passageiro , numero = passageiro.assento )
        time.sleep(0.1)
        os.system('clear')
        print(aviao)

        contadorEntrada += 1

print('\n')




