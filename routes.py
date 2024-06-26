from flask import Flask, jsonify, request, abort, render_template, redirect, url_for 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required 
from models import app, db, User, Aluno

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    alunos = Aluno.query.all()
    return render_template('index.html', alunos=alunos)

@app.route('/aptos')
def aptos():
    alunos = Aluno.query.filter_by(apto=True).all()
    return render_template('aptos.html', alunos=alunos)

@app.route('/inaptos')
def inaptos():
    alunos = Aluno.query.filter_by(apto=False).all()
    return render_template('inaptos.html', alunos=alunos)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401
    login_user(user)
    return jsonify({'message': 'Logged in successfully'})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/alunos', methods=['POST'])
@login_required
def add_aluno():
    data = request.get_json()
    nome = data.get('nome')
    aluno = Aluno(nome=nome)
    db.session.add(aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno added successfully'}), 201

@app.route('/alunos/<int:id>', methods=['GET'])
@login_required
def get_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return jsonify({'id': aluno.id, 'nome': aluno.nome, 'apto': aluno.apto})

@app.route('/alunos/<int:id>', methods=['PUT'])
@login_required
def update_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    data = request.get_json()
    aluno.nome = data.get('nome', aluno.nome)
    aluno.apto = data.get('apto', aluno.apto)
    db.session.commit()
    return jsonify({'message': 'Aluno updated successfully'})

@app.route('/alunos/<int:id>/toggle_apto', methods=['PUT'])
@login_required
def toggle_apto(id):
    aluno = Aluno.query.get_or_404(id)
    aluno.apto = not aluno.apto
    db.session.commit()
    return jsonify({'message': 'Aluno status toggled successfully'})

@app.route('/alunos/<int:id>/remove', methods=['POST'])
@login_required
def remove_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/alunos/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno removed successfully'})
