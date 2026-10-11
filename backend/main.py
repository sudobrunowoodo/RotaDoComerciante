from flask import Flask, render_template, request, redirect, url_for 
from db import db 
from models import Feirantes, Perfil_feirantes
import bcrypt as bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db.init_app(app)

@app.route('/')
def home():
    feirantes = db.session.query(Feirantes).all()
    return render_template('home.html', feirantes=feirantes)

# @app.route('/registrar')
# def registrar():
#     return render_template('registrar_contato.html')

@app.route('/registrar', methods = ['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar_feirante.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        status = request.form['statusForm']

        senha_hash = bp.hashpw(senha.encode('utf-8'), bp.gensalt())    

        novo_feirante = Feirantes (nome=nome, email=email, senha=senha_hash, status=status)
        db.session.add(novo_feirante)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    feirante = db.session.query(Feirantes).filter_by(id=id).first()
    db.session.delete(feirante)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    feirante = db.session.query(Feirantes).filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('editar_feirante.html', feirante=feirante)
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        status = request.form['statusForm']
        
        feirante.nome = nome
        feirante.email = email
        feirante.status = status
        db.session.commit()
        return redirect(url_for('home'))

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)
    