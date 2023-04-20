import random
import time

class Porta():

    def __init__(self, situacao, posicao):
        self.posicao = posicao
        self.setSituacao(situacao)
    
    def setSituacao(self, situacao):
        if (situacao>=0 and situacao<2):
            self.situacao = situacao
        else:
            print("Condicao invalida!")
    
    def getSituacao(self):
        if self.situacao == 1:
            return "aberta"
        elif self.situacao == 0:
            return "fechada"
        else:
            return "indeterminado"

    def __str__(self):
        return f"A porta está {self.getSituacao()}"


#-------------------------------------------------------------
class Corredor():

    def __init__(self):
        self.qtdPessoas = 0
        self.pessoas = []
    
    def getQTD(self):
        return self.qtdPessoas
    
    def addCorredor(self):
        self.qtdPessoas +=1
    
    def remCorredor(self):
        self.qtdPessoas-=1


#-------------------------------------------------------------
class Pessoa():

    def __init__(self,nome,assento=None):
        self.nome = nome
        self.setPosicao(1)
        self.time = 0
        self.assento = assento
        self.entrada = None

    def getNome(self):
        return self.nome
    
    def passarPeloCorredor(self, corredor):
        self.setPosicao(3)
        print(f"{self.nome} está no corredor!")

        corredor.addCorredor()

        count = corredor.getQTD()
        i=0
        while i<count:
            self.time+=2
            i+=1
    
    def passarPelaPorta(self, porta):
        self.setPosicao(2)
        if porta.situacao == 1:
            print(f"{self.nome} passou pela porta {porta.posicao}!")
        self.time+=1

    def setPosicao(self, posicao):
        if (posicao>=1 and posicao<=4):
            self.posicao = posicao
        else:
            print("Posicao invalida!")
        # 1 = fila, 2 = porta, 3=corredor, 4 = banco

    def getPosicao(self):
        if self.posicao == 1:
            return "na fila"
        elif self.posicao == 2:
            return "na porta"
        elif self.posicao == 3:
            return "no corredor"
        elif self.posicao == 4:
            return "no banco"
        else:
            return "indefinido"

    def sentarNoBanco(self, corredor):
        corredor.remCorredor()
        self.setPosicao(4)
        print(f"Passageiro {self.getNome()} esta sentado!")
        self.time+= 1
    
    def getTime(self):
        return self.time

    def __str__(self):
        return f"{self.getNome()} está {self.getPosicao()}"


#-------------------------------------------------------------


        
        