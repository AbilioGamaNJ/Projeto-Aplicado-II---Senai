from flask import Flask, jsonify, request, abort, render_template, redirect, url_for 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required 
from models import app, db, User, Aluno

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Usuário ou senha incorreto')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/email', methods=['GET'])
@login_required
def get_email():
    return jsonify({'email': current_user.email})

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

@app.route('/pesquisarColaborador', methods=['GET'])
@login_required
def pesquisar_colaborador():
    nome = request.args.get('nome')
    colaborador = User.query.filter_by(username=nome).first()
    if colaborador:
        return jsonify({'id': colaborador.id, 'username': colaborador.username, 'email': colaborador.email})
    else:
        return jsonify({'message': 'Colaborador não encontrado'}), 404

@app.route('/validarAluno', methods=['POST'])
@login_required
def validar_aluno():
    data = request.get_json()
    nome = data.get('nome')
    aluno = Aluno.query.filter_by(nome=nome).first()
    if aluno:
        return jsonify({'id': aluno.id, 'nome': aluno.nome, 'apto': aluno.apto})
    else:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@app.route('/puxarExcel', methods=['POST'])
@login_required
def puxar_excel():
    file = request.files.get('file')
    if not file:
        return jsonify({'message': 'No file uploaded'}), 400

    if file.filename != 'Treinamentos_Colaborador.xlsx':
        return jsonify({'message': 'Nome do arquivo incorreto'}), 400

    try:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            colaborador = Aluno(
                nome=row['Nome'],
                cpf=row['CPF'],
                sexo=row['Sexo'],
                email=row['Email'],
                data_nascimento=row['Data de Nascimento']
            )
            db.session.add(colaborador)
        db.session.commit()
        return jsonify({'message': 'Dados importados com sucesso'}), 201
    except Exception as e:
        return jsonify({'message': 'Erro ao processar o arquivo', 'error': str(e)}), 500

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
