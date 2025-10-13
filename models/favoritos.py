from datetime import datetime
from app import db

class Favorito(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    data_favorito = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship("Usuario", backref="favoritos", lazy=True)
    livro = db.relationship("Livro", backref="favoritos", lazy=True)
