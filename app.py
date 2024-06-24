# app.py
from flask import Flask
from database import db
from filmeController import filme_bp
from usuarioController import usuario_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmes.db'
app.config['SECRET_KEY'] = 'secret!'

# Inicializar o banco de dados com a aplicação
db.init_app(app)

# Registrar os Blueprints
app.register_blueprint(filme_bp)
app.register_blueprint(usuario_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Certifique-se de criar as tabelas
    app.run(debug=True)
