from db import db
from flask_login import UserMixin

class Feirantes (db.Model, UserMixin):
    __tablename__ = 'feirantes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='ativo')
    

    def __repr__(self):
        return f"<{self.nome}>"

class Perfil_feirantes(db.Model):
    __tablename__ = 'perfil_feirantes'
    id = db.Column(db.Integer, primary_key=True)    
    feirante_id = db.Column(db.Integer, db.ForeignKey('feirantes.id'), nullable=False)
    nome_barraca = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f"<{self.nome_barraca}>"


class Produtos(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)

    feirante_id = db.Column(
        db.Integer,
        db.ForeignKey('feirantes.id'),
        nullable=False
    )

    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(255), nullable=True)

    feirante = db.relationship(
        'Feirantes',
        backref=db.backref(
            'produtos',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f"<{self.nome}>"
        

class Localizacao(db.Model):
    __tablename__ = 'localizacao'

    id = db.Column(db.Integer, primary_key=True)

    feirante_id = db.Column(
        db.Integer,
        db.ForeignKey('feirantes.id'),
        nullable=False,
        unique=True
    )

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    hora_abertura = db.Column(db.String(5), nullable=False)
    hora_fechamento = db.Column(db.String(5), nullable=False)

    feirante = db.relationship(
        'Feirantes',
        backref=db.backref(
            'localizacao',
            cascade='all, delete-orphan',
            uselist=False,
            single_parent=True
        )
    )

    def __repr__(self):
        return f"<{self.endereco}>"
