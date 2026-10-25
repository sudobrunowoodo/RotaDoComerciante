from flask import render_template, request, redirect, url_for, abort
from db import db
from flask_login import login_required, current_user
from models import Localizacao
from validators import validar_localizacao
from config import app


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
