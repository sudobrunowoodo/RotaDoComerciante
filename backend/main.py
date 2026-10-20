from flask import Flask, render_template, request, redirect, url_for, abort
from db import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import Feirantes, Perfil_feirantes, Produtos, Localizacao
from datetime import datetime
from math import isfinite
import bcrypt as bp
from utils import verificar_cnpj
import os
from jinja2 import ChoiceLoader, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    FileSystemLoader(os.path.join(BASE_DIR, '..', 'frontend'))
])
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

@app.route('/registrar', methods = ['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        cnpj = request.form['cnpjForm']

        status_bol = verificar_cnpj(cnpj)
        if status_bol:
            status = "ativo"
        else:
            status = "inativo"

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

def validar_produto(nome, descricao, preco_texto, foto):

    if nome == "":
        return "Informe o nome do produto."

    if len(nome) > 80:
        return "O nome deve ter no máximo 80 caracteres."

    if len(descricao) > 200:
        return "A descrição deve ter no máximo 200 caracteres."

    if len(foto) > 255:
        return "A foto deve ter no máximo 255 caracteres."

    try:
        preco = float(preco_texto.replace(",", "."))
    except ValueError:
        return "Preço inválido."

    if not isfinite(preco) or preco <= 0:
        return "O preço deve ser maior que zero."

    return None


def hora_valida(texto):

    try:
        datetime.strptime(texto, "%H:%M")
        return True
    except (ValueError, TypeError):
        return False


def validar_localizacao(
    latitude_texto,
    longitude_texto,
    endereco,
    hora_abertura,
    hora_fechamento
):

    try:
        latitude = float(latitude_texto.replace(",", "."))
        longitude = float(longitude_texto.replace(",", "."))
    except ValueError:
        return "Latitude e longitude devem ser números."

    if not isfinite(latitude) or not -90 <= latitude <= 90:
        return "Latitude inválida."

    if not isfinite(longitude) or not -180 <= longitude <= 180:
        return "Longitude inválida."

    if endereco == "":
        return "Informe o endereço."

    if len(endereco) > 200:
        return "O endereço deve ter no máximo 200 caracteres."

    if not hora_valida(hora_abertura):
        return "Horário de abertura inválido. Use HH:MM."

    if not hora_valida(hora_fechamento):
        return "Horário de fechamento inválido. Use HH:MM."

    abertura = datetime.strptime(hora_abertura, "%H:%M").time()
    fechamento = datetime.strptime(hora_fechamento, "%H:%M").time()

    if abertura >= fechamento:
        return "A abertura deve ser anterior ao fechamento."

    return None

@app.route("/produtos")
@login_required
def produtos():

    lista = Produtos.query.filter_by(
        feirante_id=current_user.id
    ).order_by(Produtos.id).all()

    return render_template(
        "produtos.html",
        produtos=lista
    )


@app.route("/produtos/registrar", methods=["GET", "POST"])
@login_required
def registrar_produto():

    if request.method == "GET":
        return render_template(
            "form_produto.html",
            produto=None,
            dados={},
            erro=None
        )

    nome = request.form.get("nomeForm", "").strip()
    descricao = request.form.get("descricaoForm", "").strip()
    preco_texto = request.form.get("precoForm", "").strip()
    foto = request.form.get("fotoForm", "").strip()

    erro = validar_produto(
        nome,
        descricao,
        preco_texto,
        foto
    )

    if erro:
        return render_template(
            "form_produto.html",
            produto=None,
            dados=request.form,
            erro=erro
        ), 400

    novo_produto = Produtos(
        feirante_id=current_user.id,
        nome=nome,
        descricao=descricao or None,
        preco=float(preco_texto.replace(",", ".")),
        foto=foto or None
    )

    db.session.add(novo_produto)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

        return render_template(
            "form_produto.html",
            produto=None,
            dados=request.form,
            erro="Não foi possível cadastrar o produto."
        ), 500

    return redirect(url_for("produtos"))


@app.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_produto(id):

    produto = Produtos.query.filter_by(
        id=id,
        feirante_id=current_user.id
    ).first()

    if produto is None:
        abort(404)

    if request.method == "GET":
        dados = {
            "nomeForm": produto.nome,
            "descricaoForm": produto.descricao or "",
            "precoForm": produto.preco,
            "fotoForm": produto.foto or ""
        }

        return render_template(
            "form_produto.html",
            produto=produto,
            dados=dados,
            erro=None
        )

    nome = request.form.get("nomeForm", "").strip()
    descricao = request.form.get("descricaoForm", "").strip()
    preco_texto = request.form.get("precoForm", "").strip()
    foto = request.form.get("fotoForm", "").strip()

    erro = validar_produto(
        nome,
        descricao,
        preco_texto,
        foto
    )

    if erro:
        return render_template(
            "form_produto.html",
            produto=produto,
            dados=request.form,
            erro=erro
        ), 400

    produto.nome = nome
    produto.descricao = descricao or None
    produto.preco = float(preco_texto.replace(",", "."))
    produto.foto = foto or None

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

        return render_template(
            "form_produto.html",
            produto=produto,
            dados=request.form,
            erro="Não foi possível alterar o produto."
        ), 500

    return redirect(url_for("produtos"))


@app.route("/produtos/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_produto(id):

    produto = Produtos.query.filter_by(
        id=id,
        feirante_id=current_user.id
    ).first()

    if produto is None:
        abort(404)

    db.session.delete(produto)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500)

    return redirect(url_for("produtos"))

@app.route("/localizacoes")
@login_required
def localizacoes():

    lista = Localizacao.query.filter_by(
        feirante_id=current_user.id
    ).order_by(Localizacao.id).all()

    return render_template(
        "localizacoes.html",
        localizacoes=lista
    )


@app.route("/localizacoes/registrar", methods=["GET", "POST"])
@login_required
def registrar_localizacao():

    existente = Localizacao.query.filter_by(
        feirante_id=current_user.id
    ).first()

    if existente is not None:
        return redirect(
            url_for("editar_localizacao", id=existente.id)
        )

    if request.method == "GET":
        return render_template(
            "form_localizacao.html",
            localizacao=None,
            dados={},
            erro=None
        )

    latitude_texto = request.form.get(
        "latitudeForm", ""
    ).strip()

    longitude_texto = request.form.get(
        "longitudeForm", ""
    ).strip()

    endereco = request.form.get(
        "enderecoForm", ""
    ).strip()

    hora_abertura = request.form.get(
        "aberturaForm", ""
    ).strip()

    hora_fechamento = request.form.get(
        "fechamentoForm", ""
    ).strip()

    erro = validar_localizacao(
        latitude_texto,
        longitude_texto,
        endereco,
        hora_abertura,
        hora_fechamento
    )

    if erro:
        return render_template(
            "form_localizacao.html",
            localizacao=None,
            dados=request.form,
            erro=erro
        ), 400

    nova_localizacao = Localizacao(
        feirante_id=current_user.id,
        latitude=float(latitude_texto.replace(",", ".")),
        longitude=float(longitude_texto.replace(",", ".")),
        endereco=endereco,
        hora_abertura=hora_abertura,
        hora_fechamento=hora_fechamento
    )

    db.session.add(nova_localizacao)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

        return render_template(
            "form_localizacao.html",
            localizacao=None,
            dados=request.form,
            erro="Não foi possível cadastrar a localização."
        ), 500

    return redirect(url_for("localizacoes"))


@app.route("/localizacoes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_localizacao(id):

    localizacao = Localizacao.query.filter_by(
        id=id,
        feirante_id=current_user.id
    ).first()

    if localizacao is None:
        abort(404)

    if request.method == "GET":
        dados = {
            "latitudeForm": localizacao.latitude,
            "longitudeForm": localizacao.longitude,
            "enderecoForm": localizacao.endereco,
            "aberturaForm": localizacao.hora_abertura,
            "fechamentoForm": localizacao.hora_fechamento
        }

        return render_template(
            "form_localizacao.html",
            localizacao=localizacao,
            dados=dados,
            erro=None
        )

    latitude_texto = request.form.get(
        "latitudeForm", ""
    ).strip()

    longitude_texto = request.form.get(
        "longitudeForm", ""
    ).strip()

    endereco = request.form.get(
        "enderecoForm", ""
    ).strip()

    hora_abertura = request.form.get(
        "aberturaForm", ""
    ).strip()

    hora_fechamento = request.form.get(
        "fechamentoForm", ""
    ).strip()

    erro = validar_localizacao(
        latitude_texto,
        longitude_texto,
        endereco,
        hora_abertura,
        hora_fechamento
    )

    if erro:
        return render_template(
            "form_localizacao.html",
            localizacao=localizacao,
            dados=request.form,
            erro=erro
        ), 400

    localizacao.latitude = float(
        latitude_texto.replace(",", ".")
    )

    localizacao.longitude = float(
        longitude_texto.replace(",", ".")
    )

    localizacao.endereco = endereco
    localizacao.hora_abertura = hora_abertura
    localizacao.hora_fechamento = hora_fechamento

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

        return render_template(
            "form_localizacao.html",
            localizacao=localizacao,
            dados=request.form,
            erro="Não foi possível alterar a localização."
        ), 500

    return redirect(url_for("localizacoes"))


@app.route("/localizacoes/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_localizacao(id):

    localizacao = Localizacao.query.filter_by(
        id=id,
        feirante_id=current_user.id
    ).first()

    if localizacao is None:
        abort(404)

    db.session.delete(localizacao)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500)

    return redirect(url_for("localizacoes"))
    
if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)
    
    
