from filmeModel import Filme
from usuarioModel import Usuario
from database import db
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
filme_bp = Blueprint('filme_bp', __name__)

@filme_bp.route('/filmes', methods=['GET'])
def listar_filmes():
    try:
        filmes = Filme.query.all()
        filmes_lista = [filme.to_dict() for filme in filmes]
        return jsonify(filmes_lista), 200
    except Exception as erro:
        return jsonify({"message": f"{erro} - Falha na requisição"}), 500

@filme_bp.route('/filmes/<int:id>', methods=['GET'])
def listar_filme_por_id(id):
    try:
        filme = Filme.query.get(id)
        if filme is None:
            return jsonify({"message": "Filme não encontrado"}), 404
        return jsonify(filme.to_dict()), 200
    except Exception as erro:
        return jsonify({"message": f"{erro} - Falha na requisição do filme"}), 500

@filme_bp.route('/filmes', methods=['POST'])
def cadastrar_filme():
    try:
        dados = request.json
        usuario_id = dados.get('usuario_id')  # Supondo que você passe o ID do usuário junto com os dados do filme

        # Verifica se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"message": "Usuário não encontrado"}), 404

        novo_filme = Filme(
            titulo=dados['titulo'],
            diretor=dados['diretor'],
            ano=dados['ano'],
            genero=dados['genero'],
            usuario_id=usuario_id  # Associa o filme ao usuário pelo ID
        )

        db.session.add(novo_filme)
        db.session.commit()

        # Retornando a resposta com informações do filme e do usuário associado
        return jsonify({
            "message": "Filme criado com sucesso",
            "filme": novo_filme.to_dict(),
            "usuario": usuario.to_dict()
        }), 201
    except Exception as erro:
        return jsonify({"message": f"Falha ao cadastrar filme: {erro}"}), 500
    
@filme_bp.route('/filmes/<int:id>', methods=['PUT'])
def atualizar_filme(id):
    try:
        dados = request.json
        filme = Filme.query.get(id)
        if filme is None:
            return jsonify({"message": "Filme não encontrado"}), 404
        
        filme.titulo = dados['titulo']
        filme.diretor = dados['diretor']
        filme.ano = dados['ano']
        filme.genero = dados['genero']

        db.session.commit()
        return jsonify({"message": "Filme atualizado"}), 200
    except Exception as erro:
        return jsonify({"message": f"{erro} - Falha na atualização"}), 500

@filme_bp.route('/filmes/<int:id>', methods=['DELETE'])
def excluir_filme(id):
    try:
        filme = Filme.query.get(id)
        if filme is None:
            return jsonify({"message": "Filme não encontrado"}), 404
        
        db.session.delete(filme)
        db.session.commit()
        return jsonify({"message": "Filme excluído com sucesso"}), 200
    except Exception as erro:
        return jsonify({"message": f"{erro} - Falha na exclusão"}), 500
@filme_bp.route('/add_filme', methods=['POST'])
def add_filme():
    if 'usuario_id' not in session:
        return redirect(url_for('usuario_bp.login'))
    titulo = request.form['titulo']
    diretor = request.form['diretor']
    ano = request.form['ano']
    genero = request.form['genero']
    usuario_id = session['usuario_id']
    novo_filme = Filme(titulo=titulo, diretor=diretor, ano=ano, genero=genero, usuario_id=usuario_id)
    db.session.add(novo_filme)
    db.session.commit()
    return redirect(url_for('filme_bp.index'))

@filme_bp.route('/edit_filme/<int:filme_id>', methods=['GET', 'POST'])
def edit_filme(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    if request.method == 'POST':
        filme.titulo = request.form['titulo']
        filme.diretor = request.form['diretor']
        filme.ano = request.form['ano']
        filme.genero = request.form['genero']
        db.session.commit()
        return redirect(url_for('filme_bp.index'))
    return render_template('edit_filme.html', filme=filme)

@filme_bp.route('/delete_filme/<int:filme_id>', methods=['POST'])
def delete_filme(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    db.session.delete(filme)
    db.session.commit()
    return redirect(url_for('filme_bp.index'))

@filme_bp.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('usuario_bp.login'))
    usuario_id = session['usuario_id']
    filmes = Filme.query.filter_by(usuario_id=usuario_id).all()
    return render_template('index.html', filmes=filmes)
