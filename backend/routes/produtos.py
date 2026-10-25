from flask import render_template, request, redirect, url_for, abort
from db import db
from flask_login import login_required, current_user
from models import Produtos
from validators import validar_produto
from config import app


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
