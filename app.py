from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


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


#endpoint generos /generos
@app.route("/generos")
def listar_generos():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM generos"))
        generos = [dict(row._mapping) for row in result]
        return jsonify(generos)
    
#endpoint livro pelo id /livros/<id>
@app.route("/livros/<int:livro_id>")
def detalhes_livro(livro_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM livros WHERE id = :id"),
            {"id": livro_id}
        )
        livro = result.fetchone()
        if livro:
            return jsonify(dict(livro._mapping))
        else:
            return jsonify({"erro": "Livro não encontrado"}), 404
        

#retorna todos de um genero espec.  /generos/<id>/livros 
@app.route("/generos/<int:genero_id>/livros")
def livros_por_genero(genero_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM livros WHERE genero_id = :id"),
            {"id": genero_id}
        )
        livros = [dict(row._mapping) for row in result]
        return jsonify(livros)
    

#endpoint cadastro user    
@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()
    print(data)

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Campos obrigatórios: nome, email e senha"}), 400

    try:
        senha_hash = generate_password_hash(senha)

        with engine.connect() as connection:
            connection.execute(
                text("""
                    INSERT INTO usuarios (nome, email, senha_hash)
                    VALUES (:nome, :email, :senha_hash)
                """),
                {"nome": nome, "email": email, "senha_hash": senha_hash}
            )

        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": "Erro ao cadastrar usuário", "detalhe": str(e)}), 500
    
#verifica se email+senha bate com o banco
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Informe email e senha"}), 400

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM usuarios WHERE email = :email"),
            {"email": email}
        )
        usuario = result.fetchone()

        if usuario and check_password_hash(usuario._mapping["senha_hash"], senha):
            return jsonify({"mensagem": "Login bem-sucedido", "nome": usuario._mapping["nome"]})
        else:
            return jsonify({"erro": "Credenciais inválidas"}), 401


#uptime robot - serviço que nao deixa a api dormir
@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})