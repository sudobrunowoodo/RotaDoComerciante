from flask import Flask, render_template, request, redirect, url_for
from db import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import Feirantes, Perfil_feirantes, Produtos, Localizacao
from datetime import datetime
from math import isfinite
import bcrypt as bp


app = Flask(__name__)
app.secret_key = 'RotaDoFeirante'
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db.init_app(app)

@app.route('/')
@login_required
def home():
    feirantes = db.session.query(Feirantes).all()
    return render_template('home.html', feirantes=feirantes)

@lm.user_loader
def user_loader(id):
    feirante = db.session.query(Feirantes).filter_by(id= id).first()
    return feirante

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
        login_user(novo_feirante)
        return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    feirante = db.session.query(Feirantes).filter_by(id=id).first()
    db.session.delete(feirante)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']

        user = db.session.query(Feirantes).filter_by(email= email).first()

        if user and bp.checkpw(senha.encode('utf-8'), user.senha):
            login_user(user)
            return redirect(url_for('home'))

        return 'Email ou senha incorretos.'


@app.route('/logout')
@login_required
def logout():
    logout_user()
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
    
    
