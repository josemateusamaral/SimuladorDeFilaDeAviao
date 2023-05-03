import random
import time
import os
import sqlite3

class Simulador:
    def pegarSimulacoesTestadas(self):
        
        if 'simulacoes.db' not in os.listdir():
            con = sqlite3.connect("simulacoes.db")
            cursor = con.cursor()
            cursor.execute('''
                CREATE TABLE simulacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    simulacao TEXT,
                    tempo INTEGER
                )
            ''')
            con.commit()
            con.close()

        print('-----------TABELA---------------')
        con = sqlite3.connect("simulacoes.db")
        cursor = con.cursor()
        cursor.execute('SELECT * FROM simulacoes')
        resultados = cursor.fetchall()
        simulacoes = []
        melhorSequencia = None
        melhorTempo = None
        for resultado in resultados:
            if melhorTempo == None:
                melhorTempo = resultado[2]
                melhorSequencia = resultado[1]
            
            elif resultado[2] < melhorTempo:
                melhorTempo = resultado[2]
                melhorSequencia = resultado[1]

            simulacoes.append(resultado[1])
        con.close()

        matrixSimulacoes = []
        for i in simulacoes:
            sim = []
            for cada in i.split('_'):
                if cada != '':
                    sim.append(cada)
            matrixSimulacoes.append(sim)

        return {'matrix':matrixSimulacoes,'melhorTempo':melhorTempo,'melhorSequencia':melhorSequencia}

    def rodarSimulacoes(self,quantidadeSimulacoes):
        sequencias = self.pegarSimulacoesTestadas()
        sequenciasTestadas = sequencias['matrix']
        #print('sequencia testadas:',sequenciasTestadas)
        #print('quantidadeDeTestadas:',len(sequenciasTestadas))
        melhorSequencia = sequencias['melhorSequencia']
        melhorTempo = sequencias['melhorTempo']
        
        con = sqlite3.connect("simulacoes.db")
        cursor = con.cursor()
        
        sequenciasTestes = []

        for index,i in enumerate(range(quantidadeSimulacoes)):

            aviao = Aviao()
            tempo = 0
            contadorEntrada = 0

            filaDeEmbarque2 = []
            sequencia = []
            
            while True:
                
                filaDeEmbarque2 = []
                sequencia = []
                posicoes = []
                for i in ['A','B','C','D','E','F','G','H']:
                    for numero in range(1,10):
                        posicoes.append(f'{i}{numero}')
                
                while posicoes != []:
                    posicao = random.choice(posicoes)
                    filaDeEmbarque2.append(Pessoa('nome',posicao,random.choice([True])))
                    sequencia.append(posicao)
                    posicoes.remove(posicao)
                    
                if filaDeEmbarque2 not in sequenciasTestadas:
                    sequenciasTestadas.append(filaDeEmbarque2)
                    break

            for _ in aviao.classes:

                while filaDeEmbarque2 != [] or not aviao.corredorVazio():

                    aviao.andarFila()
                    
                    ordem = ''
                    if(contadorEntrada < 10):
                        ordem = '0' + str(contadorEntrada)
                    else:
                        ordem = str(contadorEntrada)
                    
                    if filaDeEmbarque2 != []:
                        passageiro = filaDeEmbarque2[0]
                        passageiro.ordemEntrada = ordem

                        if aviao.colocarfila(passageiro):
                            filaDeEmbarque2.pop(0)    
                            contadorEntrada += 1    
                    
                    tempo += 1
                    continue
                    
                    time.sleep(0.1)
                    os.system('clear')
                    print(f'simulação: {index + 1} de {quantidadeSimulacoes}')
                    print('melhor tempo:',melhorTempo)
                    print('faltando embarcar:',len(filaDeEmbarque2))
                    print('tempo:',tempo)
                    print(aviao)

            if melhorTempo == None or tempo < melhorTempo:
                melhorTempo = tempo
                melhorSequencia = sequencia

            sequenciasTestadas.append(sequencia)
            
            stringSequencia = ''
            for cada in sequencia:
                stringSequencia += cada + '_'
            
            cursor.execute('INSERT INTO simulacoes (simulacao, tempo) VALUES (?, ?)', (stringSequencia,tempo))
                
        print('melhor sequencia:',melhorSequencia)
        print('melhorTempo:',melhorTempo)

        con.commit()
        con.close()

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

    classesDisponiveis = ['Classe Economica']
    filas = ['A','B','C','D','E','F','G','H']

    def __init__(self):
        
        self.classes = []

        self.corredor = []
        for i in range( int(Classe.quantidadeAssentos / Classe.assentosPorFila) ):
            self.corredor.append(None)

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
                # print(numeroAssento)
            
            self.classes.append(classObj)

    def corredorVazio(self):
        for i in self.corredor:
            if i !=None:
                return False
        return True
            
        
    def colocarfila(self, passageiro):
        if self.corredor[0]==None:
            self.corredor[0] = passageiro
            return True
        else:
            return False
    
    def andarFila(self):
        
        for index, passageiro in enumerate(reversed(self.corredor)):

            if passageiro==None:
                continue

            posicao = len(self.corredor)-1 - index

            #ta na fila certa
            if posicao+1 == passageiro.numFila:
                if not passageiro.tempoBagagem or not passageiro.temBagagem:
                    self.classes[0].ocuparAssento( passageiro = passageiro , numero = passageiro.assento)
                    self.corredor[posicao] = None
                    passageiro.colocandoBagagem = False
                    continue
                else:
                    passageiro.tempoBagagem-=1
                    passageiro.colocandoBagagem = True
                    continue
   
            if posicao >= len(self.corredor)-1:
                continue

            if self.corredor[posicao+1] == None:
                self.corredor[posicao+1], self.corredor[posicao] = self.corredor[posicao], self.corredor[posicao+1]
    

    def __str__(self):
        string = ''
        for classe in self.classes:
            #string += f'\nCLASSE [{classe.nomeClasse}]'
            string += f'\n[---AVIÃO---]'
            string += f'\n\n   [A.][B.][C.][D.] |      | [E.][F.][G.][H.]'
            contador = 0
            x = 1
            y = 1
            for assento in classe.assentos:
                if x == 1:
                    string += f'\n {y} '
                if assento.ocupado:
                    string += f'<{assento.passageiro.ordemEntrada}>'
                else:
                    string += f'[{assento.numero}]'
                contador += 1
                if contador == int( classe.assentosPorFila / 2 ):
                    if self.corredor[y-1]!=None:
                        if self.corredor[y-1].temBagagem:
                            if self.corredor[y-1].colocandoBagagem:
                                string += f' |  {self.corredor[y-1].ordemEntrada}- | '
                            else:
                                string += f' |  {self.corredor[y-1].ordemEntrada}+ | '
                        else:
                            string += f' |  {self.corredor[y-1].ordemEntrada}  | '
                    else:
                        string += f' | {self.corredor[y-1]} | '
                x += 1
                if contador == classe.assentosPorFila:
                    contador = 0
                    y += 1
                    x = 1
        return string

class Porta:

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

class Corredor: 

    def __init__(self):
        self.qtdPessoas = 0
        self.pessoas = []
    
    def getQTD(self):
        return self.qtdPessoas
    
    def addCorredor(self):
        self.qtdPessoas +=1
    
    def remCorredor(self):
        self.qtdPessoas-=1

class Pessoa:

    def __init__(self,nome,assento=None, temBagagem = False):
        self.nome = nome
        self.setPosicao(1)
        self.time = 0
        self.assento = assento
        self.numFila = int(assento[1:])
        self.entrada = None
        self.ordemEntrada = 0
        self.temBagagem = temBagagem
        self.tempoBagagem = 3
        self.colocandoBagagem = False

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