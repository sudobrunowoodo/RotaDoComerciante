from db import db

class Contato(db.Model):
    __tablename__ = 'contatos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    local = db.Column(db.String(120), nullable=False)
    produto = db.Column(db.String(120), nullable=False)
    

    def __repr__(self):
        return f"<{self.nome}>"

class perfil_feirantes(db.Model):
    __tablename__ = 'perfil_feirantes'
    id = db.Column(db.Integer, primary_key=True)    
    feirante_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), nullable=False)
    nome_barraca = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    

