@ -0,0 +1,109 @@
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senha@localhost/produtos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)
    endereco_fornecedor = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'

with app.app_context():
    db.create_all()

def popular_banco():
    produtos = [
        Produto(nome="Produto 1", fornecedor="Fornecedor 1", endereco_fornecedor="Rua 1, 100", quantidade=10, endereco="Rua 1, 100", preco_unitario=10.5),
        Produto(nome="Produto 2", fornecedor="Fornecedor 2", endereco_fornecedor="Rua 2, 200", quantidade=20, endereco="Rua 2, 200", preco_unitario=20.5),
        Produto(nome="Produto 3", fornecedor="Fornecedor 3", endereco_fornecedor="Rua 3, 300", quantidade=30, endereco="Rua 3, 300", preco_unitario=30.5),
        Produto(nome="Produto 4", fornecedor="Fornecedor 4", endereco_fornecedor="Rua 4, 400", quantidade=40, endereco="Rua 4, 400", preco_unitario=40.5)
    ]
    db.session.add_all(produtos)
    db.session.commit()

with app.app_context():
    if Produto.query.count() == 0:
        popular_banco()

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'fornecedor': p.fornecedor,
        'endereco_fornecedor': p.endereco_fornecedor,
        'quantidade': p.quantidade,
        'endereco': p.endereco,
        'preco_unitario': p.preco_unitario
    } for p in produtos]), 200

@app.route('/produtos', methods=['POST'])
def add_produto():
    data = request.get_json()
    novo_produto = Produto(
        nome=data['nome'],
        fornecedor=data['fornecedor'],
        endereco_fornecedor=data['endereco_fornecedor'],
        quantidade=data['quantidade'],
        endereco=data['endereco'],
        preco_unitario=data['preco_unitario']
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 200

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'message': 'Produto não encontrado!'}), 404
    data = request.get_json()
    produto.nome = data.get('nome', produto.nome)
    produto.fornecedor = data.get('fornecedor', produto.fornecedor)
    produto.endereco_fornecedor = data.get('endereco_fornecedor', produto.endereco_fornecedor)
    produto.quantidade = data.get('quantidade', produto.quantidade)
    produto.endereco = data.get('endereco', produto.endereco)
    produto.preco_unitario = data.get('preco_unitario', produto.preco_unitario)
    db.session.commit()
    return jsonify({'message': 'Produto atualizado com sucesso!'}), 200

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'message': 'Produto não encontrado!'}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto deletado com sucesso!'}), 200

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Recurso não encontrado!'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Erro interno no servidor!'}), 500

@app.errorhandler(502)
def bad_gateway_error(error):
    return jsonify({'message': 'Erro de gateway externo!'}), 502

@app.errorhandler(501)
def not_implemented_error(error):
    return jsonify({'message': 'Método não implementado!'}), 501

if __name__ == '__main__':
    app.run(debug=True)

    