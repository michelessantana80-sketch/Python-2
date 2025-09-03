#  ____        _   _                           _        _____ _ _ _       
# |  _ \ _   _| |_| |__   ___  _ __  ___    __| | ___  | ____| (_) |_ ___ 
# | |_) | | | | __| '_ \ / _ \| '_ \/ __|  / _` |/ _ \ |  _| | | | __/ _ \
# |  __/| |_| | |_| | | | (_) | | | \__ \ | (_| |  __/ | |___| | | ||  __/
# |_|    \__, |\__|_| |_|\___/|_| |_|___/  \__,_|\___| |_____|_|_|\__\___|
#        |___/                                                            

#Autor: Michele Santos
# Versão 0.00.1v 09-2025
#Caminho da pasta

DB_PATH = "C:/Users/noturno/Desktop/Python 2 Michele/"
NOMEBANCO = "bancoDeElite.db"
TABELA_A = 'drinks.csv'
TABELA_B = 'avengers.csv'

#definições do servidor
FLASK_DEBUG = True
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000

#rotas (caminho de cada pagina)
ROTAS = [
    '/',                        #rota 00
    '/grafico1',                #rota 01
    '/grafico2',                #rota 02
    '/grafico3',                #rota 03 
    '/grafico4',                #rota 04
    '/comparar',                #rota 05
    '/upload',                  #rota 06   
    '/apagar',                  #rota 07
    '/ver',                     #rota 08
    '/final'                    #rota 09

]
#
#_________________________
# Consultas SQL
#_________________________
