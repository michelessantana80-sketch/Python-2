import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import sqlite3
import datetime

#headers para simular que somos um navegador real
#camuflagem no modo sniper
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebkit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}
baseURL = "https://www.adorocinema.com/filmes/melhores/"
filmes = [] #lista que vai armazenar os dados coletor de cada filme
data_hoje = datetime.date.today().strftime("%d-%m-%Y")
inicio = datetime.datetime.now()

card_temp_min = 1
card_temp_max = 3
pag_temp_min = 2
pag_temp_max = 4
paginaLimite = 2 #limite de paginas
bancoDados = "filmes.db"
saidaCSV = f"filmes_adorocinema_{data_hoje}.csv"

for pagina in range(1, paginaLimite + 1):
    url = f"{baseURL}?page={pagina}"
    print(f"Coletando dado da pagina {pagina}\n URL: {url}")
    resposta = requests.get(url, headers=headers)

    if resposta.status_code != 200:
        print(f"Erro ao carregar a pagina {pagina}.Codigo do erro é: {resposta.status_code}")
    
    soup = BeautifulSoup(resposta.text, "html.parser")

    cards = soup.find_all("div", class_="card entity-card entity-card-list cf")

    for card in cards:
        try:
            #captura o titulo do filme e hiperlik da pagina do filme
            titulo_tag = card.find("a", class_="meta-title-link")
            titulo = title_tag.text.strip() if titulo_tag else "N/A"
            link = "https://www.adorocinema.com/" + titulo_tag['href'] if titulo_tag else None

            #captura a note do filme
            nota_tag = card.find("span", class_="stareval-note")
            nota = nota_tag.text.strip().replace(',','.') if nota_tag else "N/A"

            diretor = "N/A"
            genero_block = None

            #caso exista um link, acessar a pag individual do filme e capturar os dados
            if link:
                filme_resposta = request.get(link, headers=headers)
                if filme_resposta.status_code == 200:
                    filme_soup = BeautifulSoup(filme_resposta.text, "html.parser")

                    #bora capturar o diretor:
                    diretor_tag = filme_soup.find("div", class_="meta-body-item meta-body-direction meta-body-oneline")
                    if diretor_tag: 
                        diretor = (
                            diretor_tag.text
                            .strip()
                            .replace('Direção','')
                            .replace(',','')
                            .replace('|','')
                            .replace('\n','')
                            .replace('\r','')
                            .strip()
                        )
                        #capturar os generos
                        genero_block = filme_soup.find('div',
                        class_= 'meta-body-info')
                #captura dos generos (fallback se não acessou o link)
                if genero_block:
                    genero_links = genero_block.find_all('a')
                    generos = [g.text.strip() for g in genero_links]
                    categoria = ", ".join(generos[:3] if generos else "N/A")
                else:
                    categoria = "N/A"

                #captura do ano de lançamento do filem
                # dica: a tag span e o nome da classe é date
                ano_tag = genero_block.find('span', class_='date') if genero_block else None
                ano = ano_tag.text.strip() if ano_tag else "N/A"

                #só add o filme se todos os dados principais existirem
                if titulo != "N/A" and link is not None and nota != "N/A":
                    filmes.append({
                        "Titulo": titulo,
                        "Direção": diretor,
                        "Nota": nota,
                        "Link":link,
                        "Ano": ano,
                        "Categoria": categoria
                    })
                else:
                    print(f"Filme incompleto ou erro de coleta de dados {titulo}")  
                #aguardar um tempo aleatorio para não sobrecarregar o site
                tempo = random.uniform(card_temp_min,card_temp_max)
                print(f"Tempo de espera entre cartão: {tempo:.1f}s")
                time.sleep(tempo)
        except Exception as erro:
            print(f"Erro ao processsar o filme {titulo}. Erro: {erro}")
#antes de passarpara a proxima pagina, vamos esperar um tempo
        tempo = random.uniform(pag_temp_min,pag_temp_max)
        print(f"Tempo de espera entre páginas: {tempo:.1f}s")
        time.sleep(tempo)
#converter os dados em um dataframe do pandas
df = pd.DataFrame(filmes)
print(df.head())

#vamos salvar os dados em um arquivo csv
df.to_csv(saidaCSV, index=False, encoding='utf-8-sig', quotechar="'", quoting=1)

termino = datetime.datetime.now()
print("---------------------------------------------")
print("Dados raspados e salvos com sucesso")
print(f"\nArquivo CSV salvo em: {saidaCSV}")
print("\nObrigada por usar o Sistema de Bot CineBot")
print(f"\nIniciado em: {inicio.strftime('%H:%M:%S')} ")
print(f"\nFinalizado em: {termino.strftime('%H:%M:%S')} ")
print("----------------------------------------------")
