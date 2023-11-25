# pip install Flask Flask-SQLAlchemy psycopg2
# psycopg2 não é declarado explicitamente mas precisa ser instalado

from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy

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


if __name__ == '__main__':
  app.run(debug=True)
