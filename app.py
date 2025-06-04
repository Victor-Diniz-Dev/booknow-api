from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

# 🔐 Sua string de conexão aqui (copie do Render)
DATABASE_URL = "postgresql://booknow_db_user:senha_aqui@dpg-nomehost.render.com:5432/booknow_db"
engine = create_engine(DATABASE_URL)

@app.route("/")
def home():
    return jsonify({"mensagem": "API BookNow funcionando com banco de dados!"})

@app.route("/livros")
def listar_livros():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM livros"))
        livros = [dict(row) for row in result]
        return jsonify(livros)

if __name__ == "__main__":
    app.run(debug=True)