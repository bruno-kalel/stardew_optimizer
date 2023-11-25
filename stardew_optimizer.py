# pip install Flask Flask-SQLAlchemy psycopg2 ortools
# psycopg2 não é declarado explicitamente mas precisa ser instalado

from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from ortools.linear_solver import pywraplp

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


class Stardew(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  nome_fruto = db.Column(db.String(255))
  inverno = db.Column(db.Boolean)
  outono = db.Column(db.Boolean)
  primavera = db.Column(db.Boolean)
  verão = db.Column(db.Boolean)
  preço_compra = db.Column(db.Integer)
  local_compra = db.Column(db.String(255))
  preço_venda_comum = db.Column(db.Integer)
  preço_venda_incomum = db.Column(db.Integer)
  dias_para_amadurecer = db.Column(db.Integer)
  dias_até_colher_novamente = db.Column(db.Integer)


@app.route('/')
def index():
  frutas = Stardew.query.order_by(Stardew.id)
  
  return render_template('index.html',
                         title='stardew_optimizer',
                         frutas=frutas)


@app.route('/static/<path:filename>')
def static_images(filename):
  return send_from_directory('static', filename)


@app.route('/form')
def form():
  return render_template('form.html')


@app.route('/otimizar', methods=['POST', ])
def otimizar():
  estação = request.form['estação']
  frutas = Stardew.query.filter(getattr(Stardew, estação)).all()
  
  return render_template('otimizar.html', frutas=frutas)


@app.route('/otimizar2', methods=['POST', ])
def otimizar2():
  quantidade_dias = request.form['quantidade_dias']
  quantidade_ouro = request.form['quantidade_ouro']
  estação = request.form['estação']
  lista_de_frutos_da_estação = Stardew.query.filter(getattr(Stardew, estação)).all()
  
  solver = pywraplp.Solver.CreateSolver('SCIP')
  infinity = solver.infinity()
  variáveis_iniciais = dict()
  
  for fruto in lista_de_frutos_da_estação:
    variáveis_iniciais[fruto.nome_fruto] = solver.IntVar(0,
                                                         infinity,
                                                         f'quantidade_sementes{fruto.nome_fruto}')
    solver.Add(fruto.dias_para_amadurecer * variáveis_iniciais[fruto.nome_fruto] <= quantidade_dias)
  
  soma_custo_ouro = solver.Sum(([fruto.preço_compra * variáveis_iniciais[fruto.nome_fruto]
                                 for fruto
                                 in lista_de_frutos_da_estação]))
  
  solver.Add(soma_custo_ouro <= quantidade_ouro)
  
  objective_terms = solver.Sum([fruto.preço_venda_comum * variáveis_iniciais[fruto.nome_fruto]
                                for fruto
                                in lista_de_frutos_da_estação]) - solver.Sum(
    fruto.preço_compra * variáveis_iniciais[fruto.nome_fruto]
    for fruto
    in lista_de_frutos_da_estação)
  solver.Maximize(solver.Sum(objective_terms))
  status = solver.Solve()
  
  if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    lucro_máximo = solver.Objective().Value()
    variáveis_finais = dict()
    
    for fruto in lista_de_frutos_da_estação:
      variáveis_finais[fruto.nome_fruto] = int(variáveis_iniciais[fruto.fruto.nome_fruto].solution_value())
      
    return render_template('resultado.html', lucro_máximo=lucro_máximo, variáveis_finais=variáveis_finais)


if __name__ == '__main__':
  app.run(debug=True)
