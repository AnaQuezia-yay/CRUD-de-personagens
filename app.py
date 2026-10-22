from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Cria um arquivo chamado personagens.db na sua pasta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personagens.db'
db = SQLAlchemy(app)

# O "Molde" do Banco de Dados
class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    origem = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    profissao = db.Column(db.String(100))
    genero = db.Column(db.String(50))
    personalidade = db.Column(db.Text)

# Gera o arquivo do banco automaticamente
with app.app_context():
    db.create_all()

@app.route('/personagens', methods=['GET'])
def listar():
    personagens = Personagem.query.all()
    # Converte os objetos do banco para JSON
    return jsonify([{"id": p.id, "nome": p.nome, "origem": p.origem, "idade": p.idade, "profissao": p.profissao, "genero": p.genero, "personalidade": p.personalidade} for p in personagens])

@app.route('/personagens', methods=['POST'])
def criar():
    dados = request.json
    novo_personagem = Personagem(**dados)
    db.session.add(novo_personagem)
    db.session.commit()
    return jsonify({"mensagem": "Personagem criado com sucesso!"}), 201

@app.route('/personagens/<int:id>', methods=['PUT'])
def editar(id):
    personagem = Personagem.query.get(id)
    dados = request.json
    for chave, valor in dados.items():
        setattr(personagem, chave, valor)
    db.session.commit()
    return jsonify({"mensagem": "Atualizado!"})

@app.route('/personagens/<int:id>', methods=['DELETE'])
def excluir(id):
    Personagem.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"mensagem": "Excluído!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)