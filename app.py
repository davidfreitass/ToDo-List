from flask import Flask 
# Importando o Flask

app = Flask(__name__)
# Aplicação principal do Flask


# Decorator serve para uma função atribuir uma nova funcionalidade para outra função
@app.route("/") # Método route faz com que possamos definir uma rota para uma página
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
# Flask só vai rodar se for realmente o arquivo principal de execução
