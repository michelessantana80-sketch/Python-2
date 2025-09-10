#rota inicial com dois botoes um levando para o grafico e 
from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio

DB_PATH = "filmes.db"


app = Flask(__name__)

def carregar_df():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM filmes", conn)
    return df


@app.route("/")
def index():
    #aqui rota inicial
    html = """
        <h1>Analise de Filmes</h1>
        <p>Escolha uma das opções no menu abaixo: </p>
        <br><a href="/tabela"><button>Ver Tabela </button></a>
        <br><a href="/grafico"><button> Filmes por Diretor por Notas </button></a>
        <br><a href="/filmes_diretor"><button> Total de filmes por Diretor </button></a>
    
    """
    return render_template_string(html)

@app.route("/grafico")
def grafico():
    #aqui rota que constroi e mostra grafico
    df = carregar_df()
    #tira as notas nulas e arredonda para reduzir o ruido
    df = df.dropna(subset=["Nota"].copy())
    df ["Nota_arred"] = df["Nota"].round(1)
    base = (
        df.groupby("Nota_arred", as_index="False").agg(Qtd = ("Titulo", "count")).sort_values("Nota_arred")
    )
#se a tabela esta vazia cai nesse return
    if base.empty:
        return render_template_string("<h2>Sem dados de notas para plotas</h2>")
    
    fig = px.scatter(
        base,
        x = "Nota_arred",
        y ="Qtd",
        title = "Quantidade de filmes por Notas",
        size = "Qtd",
        labels = {
            "Nota_arred":"Nota",
            "Qtd":"Quantidade de filmes"
        },
        hover_data = ["Nota_arred", "Qtd"]
    )
    grafico_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    html = """
        <h1>Grafico</h1>
        <div>{{grafico|safe}}</div>
        <br>
    """

    return render_template_string(html, grafico = grafico_html)

@app.route("/tabela")
def tabela():
    #aqui rota que constroi e mostra tabela
    df = carregar_df()
    total_filmes = len(df)
    notas_validas = df['Nota'].dropna() if "Nota" in df.columns else pd.Series([])

    media_nota = roud(notas.validas.mean(),2) if not notas_validas.empty else  None
    mediana_nota = roud(notas.validas.median(),2) if not notas_validas.empty else  None
    min_nota = roud(notas.validas.min(),2) if not notas_validas.empty else  None
    max_nota = roud(notas.validas.max(),2) if not notas_validas.empty else  None

    stats_html = "<ul>"
    stats_html = f"<li><b> Total de Filmes </b>{total_filmes if total_filmes is not None else 'N/A'}</li>"
    stats_html = f"<li><b>Media das Notas: </b>{media_nota if media_nota is not None else 'N/A'}</li>"
    stats_html = f"<li><b>Mediana das notas</b>{mediana_nota if mediana_nota is not None else 'N/A'}</li>"
    stats_html = f"<li><b>Menor nota:</b>{min_nota if min_nota is not None else 'N/A'}</li>"
    stats_html = f"<li><b>Maior nota</b>{max_nota if max_nota is not None else 'N/A'}</li>"
    stats_html = "</ul>"

    tabela_html = df.to_html(index=False)

    html = """
        <h1>Tabela e Estatisticas</h1>
        <h3>Estatisticas rapidas:</h3>
        <div>{{stats|safe}}</div>
        <h3>Tabela Completa:</h3>
        <div>{{tabela|safe}}</div>
    """
    return render_template_string(html,  stats=stats_html , tabela=tabela_html)
@app.route('/filmes_diretor')
def filmes_diretor():
    df = carregar_df()
        if "Direcao" not in df.columns and "Direção" in df.columns:
        df = df.rename(columns={"Direção": "Direcao"})

        g = (
            df['Direcao'].fillna("").astype(str).strip().replace({"N/A":""})
        )
        g = g[g.ne("")]
        g = g.value_counts().reset.index()
        g.columns = ["Diretor","Quantidade"]
        g = g.sort_values("Quantidade", ascending =True)

        fig = px.bar(
            g,
            x = "Diretor",
            y = "Quantidade"
            title = "Total de filmes por diretor"
            template = "plotly_dark"
        )
        fig.update_layout(
            title_x = 0.5,
            height = 520,
            bargap = 0.3,
            margin = dict(1=30, r=30, t=60, b=120),
            paper_bgcolor = "#111", 
            plot_bgcolor = "#111",
            xaxis_tickangle = -45
        )
        grafico_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    html = """
        <style>
            body{margin:0; background: #111; color: #eee;}
            #bloquinho{max-width:1200px; margin: 0 auto;}
            .blocao{margin: 0;}
        </style>
        <div id='bloquinho'>
            <div class='blocao'>
                {{grafico|safe}}
                </div>
            <//div>
        """

    return render_template_string(html, grafico = grafico_html)
if __name__=='__main__':
    app.run(debug=True)


    
