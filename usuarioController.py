from usuarioModel import Usuario
from filmeModel import Filme  # Importe o modelo Filme aqui
from database import db
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    try:
        dados = request.json
        novo_usuario = Usuario(
            login=dados['login'],
            senha=dados['senha']
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso", "usuario": novo_usuario.to_dict()}), 201
    except Exception as erro:
        return jsonify({"message": f"Falha ao cadastrar usuário: {erro}"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def listar_usuario_por_id(id):
    try:
        usuario = Usuario.query.get(id)
        if usuario is None:
            return jsonify({"message": "Usuário não encontrado"}), 404
        return jsonify(usuario.to_dict()), 200
    except Exception as erro:
        return jsonify({"message": f"{erro} - Falha na requisição do usuário"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    try:
        dados = request.json
        usuario = Usuario.query.get(id)
        if usuario is None:
            return jsonify({"message": "Usuário não encontrado"}), 404
        
        usuario.login = dados.get('login', usuario.login)
        usuario.senha = dados.get('senha', usuario.senha)
        
        db.session.commit()
        return jsonify({"message": "Usuário atualizado", "usuario": usuario.to_dict()}), 200
    except Exception as erro:
        return jsonify({"message": f"{erro} - Falha na atualização do usuário"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        if usuario is None:
            return jsonify({"message": "Usuário não encontrado"}), 404

        filmes_do_usuario = Filme.query.filter_by(usuario_id=id).all()
        for filme in filmes_do_usuario:
            db.session.delete(filme)

        db.session.delete(usuario)
        db.session.commit()

        return jsonify({"message": "Usuário e seus filmes associados foram excluídos com sucesso"}), 200
    except Exception as erro:
        db.session.rollback()
        return jsonify({"message": f"Falha na exclusão do usuário: {erro}"}), 500

@usuario_bp.route('/usuarios/login', methods=['POST'])
def login_usuario():
    try:
        dados = request.json
        login = dados['login']
        senha = dados['senha']

        usuario = Usuario.query.filter_by(login=login, senha=senha).first()

        if usuario:
            session['usuario_id'] = usuario.id
            return jsonify({"message": "Login bem-sucedido", "usuario": usuario.to_dict()}), 200
        else:
            return jsonify({"message": "Credenciais inválidas"}), 401
    except Exception as erro:
        return jsonify({"message": f"Falha no login: {erro}"}), 500
@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(login=login).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            return redirect(url_for('filme_bp.index'))
        else:
            return render_template('login.html', error="Login ou senha incorretos.")
    return render_template('login.html')

@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        login = request.form['login']
        senha = generate_password_hash(request.form['senha'])
        novo_usuario = Usuario(login=login, senha=senha)
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('usuario_bp.login'))
        except Exception as e:
            return render_template('cadastro.html', error="Erro ao cadastrar usuário.")
    return render_template('cadastro.html')

@usuario_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('usuario_bp.login'))
