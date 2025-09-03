class Carro:
    def __init__(self, modelo, cor):
        self.modelo = modelo 
        self.cor = cor
        self.velocidade = 0 # o carro começa parado

    def acelerar(self, incremento ):
        self.velocidade += incremento
        print(f' O carro {self.modelo} acelerou para {self.velocidade} Km/h')
#criando o objeto carro
meu_carro = Carro('Mob', 'Cinza')
outro_carro = Carro('Ram',  'Vermelho') 

#criando o objeto carro
meu_carro.acelerar(20)
meu_carro.acelerar(20)
meu_carro.acelerar(20)
meu_carro.desacelerar(10)

    def acelerar(self, incremento):
        self.velocidade += incremento
        print(f' O carro {self.modelo} acelerou para {self.velocidade} Km/h')


#def desacelerar(self, decremento ):
## self.velocidade -= decremento
# print(f' O carro {self.modelo} desacelerando para {self.velocidade} Km/h')


