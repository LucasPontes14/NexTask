from app import app
from flask import render_template, redirect, flash, request, url_for
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
import markdown
import bleach

from .models.conteudo import Conteudo

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/sobre.html')
def sobre():
    return render_template('sobre.html')

@app.route('/periodos.html')
def santuario():
    return render_template('periodos.html')

@app.route('/lugares.html')
def verde_nasce():
    return render_template('lugares.html')

@app.route('/pesquisadores.html')
def solar_antunes():
    return render_template('pesquisadores.html')

@app.route('/visitas.html')
def sao_francisco():
    return render_template('visitas.html')

@app.route('/mercado-publico.html')
def mercado_publico():
    return render_template('mercado-publico.html')

@app.route('/biblioteca-municipal.html')
def biblioteca_municipal():
    return render_template('biblioteca-municipal.html')

@app.route('/museu-nilo-pereira.html')
def museu_nilo_pereira():
    return render_template('museu-nilo-pereira.html')

@app.route('/estacao-ferroviaria.html')
def estacao_ferroviaria():
    return render_template('estacao-ferroviaria.html')