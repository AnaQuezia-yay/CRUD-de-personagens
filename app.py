from flask import Flask, request, jsonify
from flask_cors import CORS # Isso permite que seu HTML converse com o Python

app = Flask(__name__)
CORS(app) # Libera a comunicação entre o front e o back

# Nossa "base de dados" temporária (uma lista do Python)
personagens = []
id_atual = 1 # Para gerar IDs únicos para cada personagem

# 1. ROTA READ: Listar todos os personagens
@app.route('/personagens', methods=['GET'])
def listar_personagens():
    return jsonify(personagens)

# 2. ROTA CREATE: Criar um novo personagem
@app.route('/personagens', methods=['POST'])
def criar_personagem():
    global id_atual
    dados = request.json # Pega os dados que vieram do formulário HTML
    
    novo_personagem = {
        "id": id_atual,
        "nome": dados.get("nome"),
        "origem": dados.get("origem"),
        "idade": dados.get("idade"),
        "profissao": dados.get("profissao"),
        "genero": dados.get("genero"),
        "personalidade": dados.get("personalidade")
    }
    
    personagens.append(novo_personagem)
    id_atual += 1
    
    return jsonify(novo_personagem), 201 # 201 significa "Criado com sucesso"

# 3. ROTA UPDATE: Editar um personagem existente
@app.route('/personagens/<int:id>', methods=['PUT'])
def editar_personagem(id):
    dados = request.json
    
    for personagem in personagens:
        if personagem["id"] == id:
            # Atualiza os dados se encontrar o personagem
            personagem["nome"] = dados.get("nome", personagem["nome"])
            personagem["origem"] = dados.get("origem", personagem["origem"])
            personagem["idade"] = dados.get("idade", personagem["idade"])
            personagem["profissao"] = dados.get("profissao", personagem["profissao"])
            personagem["genero"] = dados.get("genero", personagem["genero"])
            personagem["personalidade"] = dados.get("personalidade", personagem["personalidade"])
            return jsonify(personagem)
            
    return jsonify({"erro": "Personagem não encontrado"}), 404

# 4. ROTA DELETE: Excluir um personagem
@app.route('/personagens/<int:id>', methods=['DELETE'])
def excluir_personagem(id):
    global personagens
    # Recria a lista de personagens, mantendo apenas os que NÃO têm o id informado
    personagens = [p for p in personagens if p["id"] != id]
    return jsonify({"mensagem": "Personagem excluído com sucesso"})

# Liga o servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000) # O debug=True atualiza o servidor sozinho quando você salva o arquivo