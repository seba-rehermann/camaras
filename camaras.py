from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pacientes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hora_llegada = db.Column(db.String(10))
    nombre = db.Column(db.String(100), nullable=False)
    procedencia = db.Column(db.String(100))
    estudio = db.Column(db.String(100))
    hora_inyeccion = db.Column(db.String(10))
    camara = db.Column(db.String(50))
    hora_entrada = db.Column(db.String(10))
    hora_salida = db.Column(db.String(10))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    registros = Registro.query.order_by(Registro.id.desc()).all()
    return render_template('index.html', registros=registros)

@app.route('/guardar', methods=['POST'])
def guardar():
    llegada = f"{request.form['h_llegada']}:{request.form['m_llegada']}"
    nuevo = Registro(
        hora_llegada=llegada,
        nombre=request.form['nombre'],
        procedencia=request.form['procedencia'],
        estudio=request.form['estudio'],
        camara=request.form['camara']
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/inyectar/<int:id>')
def inyectar(id):
    p = Registro.query.get_or_404(id)
    p.hora_inyeccion = datetime.now().strftime('%H:%M')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/entrar/<int:id>')
def entrar_camara(id):
    p = Registro.query.get_or_404(id)
    p.hora_entrada = datetime.now().strftime('%H:%M')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/salir/<int:id>')
def salir_camara(id):
    p = Registro.query.get_or_404(id)
    p.hora_salida = datetime.now().strftime('%H:%M')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    p = Registro.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/vaciar')
def vaciar():
    db.session.query(Registro).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    p = Registro.query.get_or_404(id)
    return render_template('editar.html', p=p)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    p = Registro.query.get_or_404(id)
    p.hora_llegada = request.form['hora_llegada']
    p.nombre = request.form['nombre']
    p.procedencia = request.form['procedencia']
    p.estudio = request.form['estudio']
    p.hora_inyeccion = request.form['hora_inyeccion']
    p.camara = request.form['camara']
    p.hora_entrada = request.form['hora_entrada']
    p.hora_salida = request.form['hora_salida']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
