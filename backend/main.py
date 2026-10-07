from flask import Flask, render_template, request, redirect, url_for 
from db import db 
from models import Contato
import bcrypt as bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db.init_app(app)

@app.route('/')
def home():
    contatos = db.session.query(Contato).all()
    return render_template('home.html', contatos=contatos)

# @app.route('/registrar')
# def registrar():
#     return render_template('registrar_contato.html')

@app.route('/registrar', methods = ['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar_contato.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        telefone = request.form['telefoneForm']
        email = request.form['emailForm']
        local = request.form['localForm']
        senha = request.form['senhaForm']
        produto = request.form['produtoForm']

        senha_hash = bp.hashpw(senha.encode('utf-8'), bp.gensalt())    

        novo_contato = Contato(nome=nome, telefone=telefone, email=email, local=local, produto=produto, senha=senha_hash)
        db.session.add(novo_contato)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    contato = db.session.query(Contato).filter_by(id=id).first()
    db.session.delete(contato)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    contato = db.session.query(Contato).filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('editar_contato.html', contato=contato)
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        telefone = request.form['telefoneForm']
        email = request.form['emailForm']
        local = request.form['localForm']
        produto = request.form['produtoForm']
        contato.nome = nome
        contato.telefone = telefone
        contato.email = email
        contato.local = local
        contato.produto = produto
        db.session.commit()
        return redirect(url_for('home'))

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)