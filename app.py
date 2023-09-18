from flask import Flask, request, jsonify
# Importando o Flask
from flask_sqlalchemy import SQLAlchemy
# Importando o SQLAlchemy para usar juntamente ao Flask
from marshmallow import Schema, fields

app = Flask(__name__)  # Aplicação principal do Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database3.db"
db = SQLAlchemy(app)
app.app_context().push()
# Configurando o banco de dados do SQLAlchemy


class ItemTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))


class ItemTodoSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str()


itemstodo_schema = ItemTodoSchema(many=True)


# Decorator serve para uma função atribuir uma nova funcionalidade para outra função
# Método route faz com que possamos definir uma rota para uma página
@app.route("/", methods=["GET"])
def index():
    # Buscando todos os objetos ItemTodo existentes no banco de dados
    items = ItemTodo.query.all()
    result = itemstodo_schema.dump(items)
    return {"items": result}


@app.route("/post/", methods=["POST"])
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
            message="Item adicionado com sucesso",
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


if __name__ == "__main__":
    db.create_all()
    app.run()
# Flask só vai rodar se for realmente o arquivo principal de execução
