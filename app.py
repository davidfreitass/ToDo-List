import os
from flask import Flask, request, jsonify
# Importando o Flask
from flask_sqlalchemy import SQLAlchemy
# Importando o SQLAlchemy para usar juntamente ao Flask
from marshmallow import Schema, fields, ValidationError
# Schema é uma biblioteca para validação de estruturas de dados em Python, fields é uma classe que recebe vários tipos de dados
from sqlalchemy import URL

url_object = URL.create(
    "postgresql",
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),  # plain (unescaped) text
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
)

app = Flask(__name__)  # Aplicação principal do Flask
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database3.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@db:5432/app"
db = SQLAlchemy(app)
app.app_context().push()
# Configurando o banco de dados do SQLAlchemy


class ItemTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))


# Classe que serve para realizar a serialização do objeto
class ItemTodoSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str()


itemstodo_schema = ItemTodoSchema(many=True)
itemtodo_schema = ItemTodoSchema()


# Decorator serve para uma função atribuir uma nova funcionalidade para outra função
# Método route faz com que possamos definir uma rota para uma página
@app.route("/", methods=["GET"])
@app.route("/todo", methods=["GET"])
@app.route("/todo/", methods=["GET"])
def index():
    # Buscando todos os objetos ItemTodo existentes no banco de dados
    items = ItemTodo.query.all()
    # dump() é usado para escrever objetos serializados Python como dados formatados em JSON em um arquivo
    result = itemstodo_schema.dump(items)
    return {"items": result}


@app.route("/todo/<int:id>", methods=["GET"])
def get_id(id):
    item_id = ItemTodo.query.get(id)
    result = itemtodo_schema.dump(item_id)
    return {"item": result}


@app.route("/post", methods=["POST"])
def post():
    # Criando um novo objeto ItemTodo e adicionando no banco de dados
    dados_request = request.get_json()  # Recebendo todo um objeto enviado no POST
    print(dados_request)
    if dados_request is not None:
        # Tratando esse objeto e captando somente o necessário
        new_item = ItemTodo(content=dados_request['content'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(
            message="Tarefa adicionada com sucesso",
            category="success",
            data=dados_request,
            status=200
        )
    else:
        return jsonify(
            message="No send content data",
            category="error",
            status=404
        )


@app.route("/todo/<int:id>", methods=["PUT"])
def update_todo(id):
    # Recebendo todo um objeto JSON enviado no body
    dados_request = request.get_json()
    if not dados_request:
        # Retornando um erro se nada for enviado
        return {"message": "No input data provided"}, 400
    try:
        # Desserializando JSON em um objeto python para manipulação
        dados = itemtodo_schema.load(dados_request)
    except ValidationError as err:
        return err.messages, 422

    # Captando apenas o item específico através do ID
    item_updated = ItemTodo.query.get(id)
    # Atualizando seu conteúdo por meio do objeto python adquirido anteriormente
    item_updated.content = dados["content"]

    # Retornando o item atualizado para o banco de dados
    db.session.add(item_updated)
    db.session.commit()
    # Serializando o objeto python em JSON novamente para ser exibido
    result = itemtodo_schema.dump(ItemTodo.query.get(item_updated.id))
    return {"message": "Tarefa atualizada.", "tarefa": result}


@app.route("/todo/<int:id>", methods=["DELETE"])
def delete_todo(id):
    item = ItemTodo.query.get(id)  # Captando um item específico através do ID
    db.session.delete(item)  # Deletando este item
    db.session.commit()
    result = itemtodo_schema.dump(item)
    # Exibindo mensagem de sucesso e o item deletado
    return {"message": "Tarefa deletada com sucesso.", "tarefa": result}


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=5000, threaded=True)
# Flask só vai rodar se for realmente o arquivo principal de execução
