from database import db

class Filme(db.Model):
    __tablename__ = 'filme'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    diretor = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(80), nullable=False)

    # Chave estrangeira para usuário
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('filmes', lazy=True))
    def __repr__(self):
        return f'<Filme {self.titulo}>'
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'diretor': self.diretor,
            'ano': self.ano,
            'genero': self.genero,
            'usuario_id': self.usuario_id  # Adicionando o ID do usuário para referência
        }
