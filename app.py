from flask import Flask, render_template
from routes.livrosRoutes import livros_blueprint


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/listar')
def listar():
    return render_template('listar.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


app.register_blueprint(livros_blueprint)

if __name__ == "__main__":
    app.run(debug=True)