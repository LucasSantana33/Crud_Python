from database import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.login}>'

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            # Não incluí a senha no to_dict por questões de segurança
        }
