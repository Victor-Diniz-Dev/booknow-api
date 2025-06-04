from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)


DATABASE_URL = "postgresql://booknow_db_user:qGqC8626TL2nWm4myDWrQOzOE2ioJxnh@dpg-d0vq8f3ipnbc7386864g-a.oregon-postgres.render.com/booknow_db"
engine = create_engine(DATABASE_URL)

@app.route("/")
def home():
    return jsonify({"mensagem": "API BookNow funcionando com banco de dados!"})

@app.route("/livros")
def listar_livros():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM livros"))
        livros = [dict(row._mapping) for row in result]
        return jsonify(livros)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})