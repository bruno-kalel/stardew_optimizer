from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from ortools.linear_solver import pywraplp
from datetime import datetime

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


class Consultas(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  quantidade_dias = db.Column(db.Integer)
  quantidade_ouro = db.Column(db.Integer)
  quantidade_solo = db.Column(db.Integer)
  estação = db.Column(db.String(10))
  lucro_máximo = db.Column(db.Numeric)
  data_hora = db.Column(db.DateTime)


@app.route('/')
def index():
  frutas = Stardew.query.order_by(Stardew.nome_fruto)
  return render_template('index.html',
                         title='Todas as lavouras',
                         frutas=frutas)


@app.route('/static/<path:filename>')
def static_images(filename):
  return send_from_directory('static', filename)


@app.route('/form')
def form():
  return render_template('form.html',
                         title='Otimizar agora')


@app.route('/otimizar', methods=['POST', ])
def otimizar():
  quantidade_dias = int(request.form['quantidade_dias'])
  quantidade_ouro = int(request.form['quantidade_ouro'])
  quantidade_solo = int(request.form['quantidade_solo'])
  estação = request.form['estação']
  lista_de_frutos_da_estação = Stardew.query.filter(getattr(Stardew, estação)).all()
  
  solver = pywraplp.Solver.CreateSolver('SCIP')
  infinity = solver.infinity()
  variáveis_iniciais = dict()
  orçamento = dict()
  variáveis_finais = dict()
  somatória = 0
  valor_venda = 0
  valor_compra = 0
  alicerce = 0
  
  for fruto in lista_de_frutos_da_estação:
    variáveis_iniciais[fruto.nome_fruto] = solver.IntVar(0,
                                                         infinity,
                                                         fruto.nome_fruto)
    
    alicerce += fruto.dias_para_amadurecer * variáveis_iniciais[fruto.nome_fruto]
    
    solver.Add(alicerce <= (quantidade_dias * quantidade_solo))
    
    # restrição de orçamento
    orçamento[fruto.nome_fruto] = fruto.preço_compra * variáveis_iniciais[fruto.nome_fruto]
    somatória += orçamento[fruto.nome_fruto]
  
  solver.Add(somatória <= quantidade_ouro)
  
  # função objetiva
  for fruto in lista_de_frutos_da_estação:
    valor_venda += fruto.preço_venda_comum * variáveis_iniciais[fruto.nome_fruto]
    valor_compra += fruto.preço_compra * variáveis_iniciais[fruto.nome_fruto]
  
  objective_terms = [valor_venda - valor_compra]
  solver.Maximize(solver.Sum(objective_terms))
  
  # resolver problema de otimização
  status = solver.Solve()
  
  # exibir resultados e cadastrar no banco de dados
  if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    flash('Otimização deu certo!')
    lucro_máximo = solver.Objective().Value()
    
    for fruto in lista_de_frutos_da_estação:
      variáveis_finais[fruto.nome_fruto] = int(variáveis_iniciais[fruto.nome_fruto].solution_value())
    
    # consulta já foi realizada anteriormente? não criar novamente no banco
    if Consultas.query.filter_by(quantidade_dias=quantidade_dias,
                                 quantidade_ouro=quantidade_ouro,
                                 quantidade_solo=quantidade_solo,
                                 estação=estação).first():
      flash('Otimização realizada anteriormente. Não será cadastrada no banco de dados.')
    
    # criar consulta nova no banco
    else:
      db.session.add(Consultas(quantidade_dias=quantidade_dias,
                               quantidade_ouro=quantidade_ouro,
                               quantidade_solo=quantidade_solo,
                               estação=estação,
                               lucro_máximo=int(round(lucro_máximo)),
                               data_hora=datetime.now()))
      db.session.commit()
      flash('Otimização adicionada às suas consultas.')
    
    return render_template('otimizar.html',
                           title='Resultados',
                           lucro_máximo=lucro_máximo,
                           quantidade_dias=quantidade_dias,
                           quantidade_ouro=quantidade_ouro,
                           quantidade_solo=quantidade_solo,
                           estação=estação,
                           frutas=lista_de_frutos_da_estação,
                           variáveis_finais=variáveis_finais)
  else:
    flash('Otimização falhou!')
    return redirect(url_for('index'))


@app.route('/consultas')
def consultas():
  lista_consultas = Consultas.query.order_by(desc(Consultas.data_hora)).all()
  return render_template('consultas.html',
                         title='Suas consultas',
                         consultas=lista_consultas)


# deletar uma única consulta
@app.route('/deletar_uma_consulta/<int:identificador>')
def deletar_uma_consulta(identificador):
  Consultas.query.filter_by(id=identificador).delete()
  db.session.commit()
  flash('A consulta selecionada foi deletada.')
  return redirect(url_for('consultas'))


# deletar todas as consultas
@app.route('/deletar_todas_as_consultas')
def deletar_todas_as_consultas():
  db.session.query(Consultas).delete()
  db.session.commit()
  flash('Todas as consultas foram deletadas.')
  return redirect(url_for('consultas'))


if __name__ == '__main__':
  app.run(debug=True)
