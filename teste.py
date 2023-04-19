from classes import *

porta = Porta(1, "esquerda")
print(porta)

pessoa1 = Pessoa("Anne")
pessoa2 = Pessoa("Nico")
pessoa3 = Pessoa("Lara")

pessoa1.passarPelaPorta(porta)
pessoa2.passarPelaPorta(porta)

assento = Assento("001", pessoa1)
assento = Assento("002", pessoa2)
assento = Assento("003", pessoa3)
corredor = Corredor()

pessoa1.passarPeloCorredor(corredor)
pessoa2.passarPeloCorredor(corredor)

pessoa3.passarPelaPorta(porta)

pessoa1.sentarNoBanco(corredor)
pessoa2.sentarNoBanco(corredor)

pessoa3.passarPeloCorredor(corredor)
pessoa3.sentarNoBanco(corredor)

print(pessoa1.getTime())
print(pessoa2.getTime())
print(pessoa3.getTime())
