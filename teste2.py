from classes import *
import time
import os

def printAviao(classes,classesDisponiveis,quantidadeAssentos,assentosPorFila):
    os.system('clear')
    #print aviao
    for classe in classes:
        print(f'\n\nCLASSE\n[{classe.nomeClasse}]')
        contador = 0
        x = 1
        y = 1
        print('     A    B    C    D   |     |   E    F    G    H  ')
        for assento in classe.assentos:
            if x == 1:
                print(f' {y} ',end='')
            
            if assento.ocupado:
                print(f'[(X)]',end='')
            else:
                print(f'[( )]',end='')

            contador += 1
            
            if contador == int(assentosPorFila / 2):
                print(f' |     | ',end='')
            x += 1
        
            if contador == assentosPorFila:
                contador = 0
                print()
                y += 1
                x = 1

classesDisponiveis = ['classeA','classeB','classe\nEconomica']
classes = []

quantidadeAssentos = 72
assentosPorFila = 8


#encher assentos
for classe in classesDisponiveis:
    classObj = Classe(classe)
    for assento in range(quantidadeAssentos):
        assentoObj = Assento(assento)
        classObj.assentos.append(assentoObj)
    classes.append(classObj)

#ocupar assento
for classe in classes:
    for assento in classe.assentos:
        assento.ocuparAssento(Pessoa('nome pessoa'))
        time.sleep(1)
        printAviao(classes,classesDisponiveis,quantidadeAssentos,assentosPorFila)

print('\n')



