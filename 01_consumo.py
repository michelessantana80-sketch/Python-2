from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random
import config_PythonsDeElite as config
import consultas

caminhoBanco = config.DB_PATH

pio.renderers.default = "browser"
nomeBanco = config.NOMEBANCO
rotas =  config.ROTAS
tabelaA = config.TABELA_A
tabelaB = config.TABELA_B

#Arquivos a serem carregados
dfDrinks = pd.read_csv(f'{caminhoBanco}{tabelaA}')
dfAvengers = pd.read_csv(f'{caminhoBanco}{tabelaB}', encoding= 'latin1')
#outros exemplos de encondigs: utf-8, cp1256

#criamos o banco de dados em SQL caso não exista
conn = sqlite3.connect(f'{caminhoBanco}{nomeBanco}')

dfDrinks.to_sql("bebidas",conn, if_exists="replace", index=False)
dfAvengers.to_sql("vingadores",conn, if_exists="replace", index=False)

conn.commit()
conn.close()
html_template = f'''
    <h1>Dashboards</h1>
    <h2>Parte 01 </h2>
    <ul>
        <li> <a href="{rotas[1]}">Top 10 Paises em consumo</a> </li>
        <li> <a href="{rotas[2]}">Media de consumo por tipo</a> </li>
        <li> <a href="{rotas[3]}">Consumo por região</a> </li>
        <li> <a href="{rotas[4]}">Comparativo entre tipos</a> </li>
    </ul>
   
    <h2>Parte 02</h2>
    <ul>
        <li> <a href="{rotas[5]}">Comparar</a> </li>
        <li> <a href="{rotas[6]}">Upload</a> </li>
        <li> <a href="{rotas[7]}">Apagar tabela</a> </li>
        <li> <a href="{rotas[8]}">Ver tabela</a> </li>
        <li> <a href="{rotas[9]}">V.A.A.</a> </li>
    </ul>
'''
#iniciar o flask
app = Flask(__name__)

def getDoConnect():
    conn = sqlite3.connect(f'{caminhoBanco}{nomeBanco}')
    conn.row_factory = sqlite3.Row
    return conn

@app.route(rotas[0])
def index():
    return render_template_string(html_template)

@app.route(rotas[1])
def grafico1():
    with sqlite3.connect(f'{caminhoBanco}{nomeBanco}') as conn:
        df = pd.read_sql_query(consultas.consulta01, conn)
    figuraGrafico1 = px.bar(
        df,
        x = 'country',
        y = 'total_litres_of_pure_alcohol',
        title = 'Top 10 paises em consumo de alcool!'
    )
    return figuraGrafico1.to_html()
@app.route(rotas[2])
def grafico2():
     with sqlite3.connect(f'{caminhoBanco}{nomeBanco}') as conn:
        df = pd.read_sql_query(consultas.consulta02, conn)
        #transforma as colunas cerveja destilados e vinhos e linhas criando no fim duas colunas, uma chamada 
        #bebidas com os nomes originais das colunas e outra com a media de porções com seus valores correspondentes 
        df_melted = df.melt(var_name= 'Bebidas', value_name = 'Média de Porçoes')
        figuraGrafico2 = px.bar(
        df_melted,
        x = 'Bebidas',
        y = 'Média de Porçoes',
        title = 'Média de consumo global por tipo'     
    )
        return figuraGrafico2.to_html()
@app.route(rotas[3])
def grafico3():
    regioes = {
        "Europa":['France','Germany', 'Spain','Italy','Portugal'],
        "Asia":['China','Japan','India','Thailand'],
        "Africa":['Angola','Nigeria','Egypt','Algeria'],
        "Americas":['USA','Brazil','Canada','Argentina','Mexico'],
    }
    dados = []
    with sqlite3.connect(f'{caminhoBanco}{nomeBanco}') as conn:
        #itera sobre o dicionario de regioes onde cada chave (regiao tem uma lista de paises)
        for regiao, paises in regioes.items():
            #criando a lista de placeholders para os paises dessa região 
            #isso vai ser  usado na consulta sql para filtrar o pais da regiao
            placeholders = ",".join([f"'{p}'"for p in paises])
            query = f"""
                SELECT SUM(total_litres_of_pure_alcohol) AS total
                FROM bebidas
                WHERE country IN ({placeholders})

            """
            total = pd.read_sql_query(query, conn).iloc[0,0]
            dados.append(
            {"Região": regiao,
             "Consumo Total": total
             })
    dfRegioes = pd.DataFrame(dados)
    figuraGrafico3 = px.pie(
        dfRegioes,
        names = "Região",
        values = "Consumo Total",
        title= "Consumo Total por Região"
      
    )
    return figuraGrafico3.to_html() + f"<br><a href= '{rotas[0]}'>Voltar</a>"

@app.route(rotas[4])
def grafico4():
    with sqlite3.connect(f'{caminhoBanco}{nomeBanco}') as conn:
        df = pd.read_sql_query(consultas.consulta03, conn)
        medias = df.mean().reset_index()
        medias.columns = ['Tipo', 'Media']
        figuraGrafico4 = px.pie(
            medias,
            names= "Tipo",
            values= "Media",
            title=  "Proporção média entre os tipos de bebidas!"
              
        )
        return figuraGrafico4.to_html() + f"<br><a href= '{rotas[0]}'>Voltar</a>"
@app.route(rotas[5], methods=["POST","GET"])
def comparar():
    opcoes = [
        'beer_servings',
        'spirit_servings',
        'wine_servings'
    ]

    if request.method == "POST":
        eixoX = request.form.get('eixo_x')
        eixoY = request.form.get('eixo_y')
        if eixoX == eixoY:
            return f"<h3> Selecionar campos diferentes </h3><br><a href= '{rotas[0]}'>Voltar</a>"
        conn = sqlite3.connect(f'{caminhoBanco}{nomeBanco}')
        df = pd.read_sql_query("SELECT country, {},{} FROM bebidas".format(eixoX,eixoY), conn)
        conn.close()
        figuraComparar = px.scatter(
            df,
            x= eixoX,
            y= eixoY,
            title= f"Comparação entre {eixoX} VS {eixoY}"

        )
        figuraComparar.update_traces(textposition = 'top center')
        return figuraComparar.to_html() + f"<br><a href='{rotas[0]}'>Voltar</a>"
    
    return render_template_string('''
        <h2> Comparar campos </h2>
        <form method="POST">
            <label> Eixo X: </label>
            <select name="eixo_x">
                    {% for opcao in opcoes %}
                        <option value='{{opcao}}'>{{opcao}}</option>
                    {% endfor %}


            </select>
            <br><br>
                                  
            <label> Eixo Y: </label>
            <select name="eixo_y">
                     {% for opcao in opcoes %}
                        <option value='{{opcao}}'>{{opcao}}</option>
                    {% endfor %}
                                  
            </select>
            <br><br>
                                  
            <input type="submit" value="-- Comparar --">
        </form>
        <br><a href="{{rotaInterna}}">Voltar</a>
''',opcoes = opcoes, rotaInterna = rotas[0])

@app.route(rotas[6], methods=['GET','POST'])
def upload():
    if request.method == "POST":
        recebido = request.files['c_arquivo']
        if not recebido:
            return f"<h3> Nenhum arquivo enviado </h3><br><a href= '{rotas[6]}'>Voltar</a>"
        dfAvengers = pd.read_csv(recebido, encoding='latin1')
        conn = sqlite3.connect(f'{caminhoBanco}{nomeBanco}')    
        dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        return f"<h3> Upload feito com sucesso </h3><br><a href= '{rotas[6]}'>Voltar</a>"

    return '''
        <h2> Upload da tabela Avengers </h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="c_arquivo" accept=".csv">
            <input type="submit" value="-- Carregar--">
        </form>
    '''
@app.route('/apagar_tabela/<nome_tabela>',methods=['GET'])
def apagarTabela(nome_tabela):
    conn = getDoConnect()
    #realiza o apontamento para o banco que será manipulado
    cursor = conn.cursor()
    #usaremos o try except para controlar possiveis erros
    # confirmar antes se a tabela existe
    cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'")
     #pega o resultado da contagem (0 se não existir e 1 se existir)
    existe = cursor.fetchone()[0] 
    if not existe:
        conn.close()
        return "Tabela não encontrada"
    
    try:
        cursor.execute(f'DROP TABLE "{nome_tabela}"')
        conn.commit()
        conn.close()
        return f"Tabela {nome_tabela} apagada com sucesso"

    except Exception as erro:
        conn.close()
        return f"Não foi possivel apagar a tabela erro:{erro}"
    
@app.route(rotas[8], methods=["POST","GET"])
def ver_tabela():
    if request.method == "POST":
        nome_tabela = request.form.get('tabela')
        if nome_tabela not in ['bebidas','vingadores']:
            return f"<h3>Tabela {nome_tabela} não encontrada</h3><br><a href={rotas[8]}>Voltar</a>"
        
        conn = getDoConnect()
        df = pd.read_sql_query(f"SELECT * from {nome_tabela}", conn)
        conn.close()

        tabela_html = df.to_html(classes='table table-striped')
        return f'''
            <h3>Conteudo da  tabela {nome_tabela}:</h3>
            {tabela_html}
            <br><a href={rotas[8]}>Voltar</a>
        '''
    

    return render_template_string('''
        <h2> Selecione a tabela a ser visualizada:</h2>
        <form  method="POST">
        <label for="tabela"> Escolha a tabela abaixo:</label>
        <select name="tabela">
            <option value= "bebidas">Bebidas</option>
            <option value= "vingadores">Vingadores</option>
        </select>
        <input type="submit" value="Consultar Tabela">
        </form>
        <br><br>
        <br><a href={{rotas[0]}}>Voltar</a>
            
''' ,rotas=rotas)
   
#usar a ver e a exlui criar uma de apagar onde é possivel selecionar a tabela que sera apagada

@app.route(rotas[7], methods=['POST','GET'])
def apagarV2():
    if request.method == "POST":
        nome_tabela = request.form.get('tabela')
        if nome_tabela not in ['bebidas','vingadores']:
         return f"<h3>Tabela {nome_tabela} não permitida para apagar</h3><br><a href={rotas[7]}>Voltar</a>"
        confirmacao = request.form.get('confirmacao')
        
        #objeto de confirmação
        conn= getDoConnect()
        if confirmacao == "Sim":

            try:
                cursor = conn.cursor()
                cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?',(nome_tabela))
                if cursor.fetchone() is None:
                    return f"<h3>Tabela {nome_tabela} não encontrada no banco de dados </h3><br><a href={rotas[7]}>Voltar</a>"
                cursor.execute(f'DROP TABLE IF EXISTS "{nome_tabela}"')
                conn.commit()
                conn.close()
                return f"<h3>Tabela {nome_tabela} excluida com sucesso </h3><br><a href={rotas[7]}>Voltar</a>"

            except Exception as erro:
                conn.close()
                return f"<h3>Erro ao apagar a tabela {nome_tabela}  Erro:{erro}</h3><br><a href={rotas[7]}>Voltar</a>"

    return f'''
        <head>
            <tiltle><marquee> CUIDADO -Apagar Tabela </marquee></tiltle>
        </head>
        <body>    
        <h2> Selecionar a tabela para apagar</h2>
        <form method="POST" id="formApagar">
            <label for="tabela"> Escolha na tabela abaixo: </label>
            <select name="tabela" id="tabela">
            <option value="">Selecione...</option>
            <option value="bebidas">Bebidas</option>
            <option value="vingadores">Vingadores</option>
            </select>
            <input  type="hidden" name="confirmação" value="" id="confirmação">
            <input type="submit" value="-- Apagar--" onclick="return confirmarExclusao();">
        </form>
        <br><a href={{rotas[0]}}>Voltar</a>
        <script type="text/javascript">
            function confirmarExclusao(){{
            var ok = confirm('Tem certeza de que deseja apagar a tabela selecionada?');
            if(ok){{
                document.getElementById
                ('confirmacao').value = 'Sim';
                return true;
            }}
            else {{
                document.getElementById
                ('confirmacao').value = 'Não';
                return false;
            }}
        }}
        </script>
        </body>
        </html>
    '''


#inicia o servidor
if __name__ == '__main__':
    app.run(
        debug= config.FLASK_DEBUG,
        host = config.FLASK_HOST,
        port = config.FLASK_PORT
        )