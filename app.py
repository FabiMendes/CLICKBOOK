from flask import Flask, render_template, session,request
from routes.livrosRoutes import livros_blueprint
from routes.usuariosRoutes import usuarios_blueprint
from routes.alugueisRoutes import alugueis_blueprint
from routes.frontRoutes import front_blueprint
from routes.avaliacoesRoutes import avaliacoes_blueprint
from routes.favoritosRoutes import favoritos_blueprint


from decorators.autenticacao import login_required, somente_admin
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "sua-chave-secreta-aqui-32-caracteres"  # Ex: "minha-senha-super-secreta-123"

# Configurações ESSENCIAIS para sessão
app.config.update(
    SESSION_COOKIE_NAME='flask_session',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # True apenas em HTTPS
    SESSION_COOKIE_SAMESITE='Lax',  # Seguro para CSRF
    PERMANENT_SESSION_LIFETIME=3600,  # 1h de duração
)
@app.route("/debug-session")
def debug_session():
    return {
        "session": dict(session),
        "cookies": request.cookies,
        "headers": dict(request.headers)
    }


app.register_blueprint(livros_blueprint)
app.register_blueprint(usuarios_blueprint)
app.register_blueprint(alugueis_blueprint)
app.register_blueprint(front_blueprint)
app.register_blueprint(avaliacoes_blueprint)
app.register_blueprint(favoritos_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

