from flask import Flask, request, redirect
# Importando o Flask
from flask_sqlalchemy import SQLAlchemy
# Importando o SQLAlchemy para usar juntamente ao Flask

app = Flask(__name__)  # Aplicação principal do Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database3.db"
db = SQLAlchemy(app)
app.app_context().push()
# Configurando o banco de dados do SQLAlchemy


class ItemTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

    def __repr__(self):
        return f'ItemTodo {self.id}'


# Decorator serve para uma função atribuir uma nova funcionalidade para outra função
# Método route faz com que possamos definir uma rota para uma página
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Criando um novo objeto ItemTodo e adicionando no banco de dados
        content = request.form['content']
        if content.strip != '':
            new_item = ItemTodo(content=content)
            db.session.add(new_item)
            db.session.commit()
        return redirect("/")
    else:
        # Buscando todos os objetos ItemTodo existentes no banco de dados
        items = ItemTodo.query.all()
        return items


if __name__ == "__main__":
    db.create_all()
    app.run()
# Flask só vai rodar se for realmente o arquivo principal de execução
