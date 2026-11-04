
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

from controllers.presenca_controller import registrar
from controllers.auth_controller import autenticar_usuario
from models.presenca_model import (
    criar_tabelas,
    buscar_palestra,
    listar_palestras
)
from controllers.palestra_controller import cadastrar_palestra
from controllers.endereco_controller import (
    buscar_endereco,
    buscar_endereco_por_coordenadas
)
from controllers.qrcode_controller import gerar_qrcode as criar_imagem_qrcode

app = Flask(
    __name__,
    template_folder="views/templates",
    static_folder="views/static"
)
app.secret_key = "checkme_chave_secreta_2026"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if autenticar_usuario(usuario, senha):
            session["usuario"] = usuario
            return redirect(url_for("painel"))

        return render_template("login.html", erro="Usuário ou senha incorretos.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

import os

from dotenv import load_dotenv

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Cria as tabelas do banco, caso ainda não existam
criar_tabelas()


@app.route("/")
def inicio():
    session.clear()
    return redirect(url_for("login"))


@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect(url_for("login"))

    palestras = listar_palestras()

    return render_template(
        "painel.html",
        palestras=palestras
    )

@app.route("/nova-palestra", methods=["GET", "POST"])
def nova_palestra():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        resultado = cadastrar_palestra(
            nome=request.form.get("nome"),
            data=request.form.get("data"),
            local=request.form.get("local"),
            latitude=request.form.get("latitude"),
            longitude=request.form.get("longitude"),
            raio_permitido=request.form.get("raio_permitido")
        )

        if resultado["status"] == "sucesso":
            return redirect(url_for("painel"))

        return render_template(
            "nova_palestra.html",
            erro=resultado["mensagem"]
        )

    return render_template("nova_palestra.html")


@app.route("/gerar-qrcode")
def gerar_qrcode():
    if "usuario" not in session:
        return redirect(url_for("login"))

    palestras = listar_palestras()

    palestras_com_qrcode = []

    for palestra in palestras:

        url_presenca = url_for(
            "presenca",
            palestra_id=palestra[0],
            _external=True
        )

        imagem_qrcode = criar_imagem_qrcode(url_presenca)

        palestras_com_qrcode.append({
            "id": palestra[0],
            "nome": palestra[1],
            "data": palestra[2],
            "local": palestra[3],
            "url": url_presenca,
            "qrcode": imagem_qrcode
        })

    return render_template(
        "qrcodes.html",
        palestras=palestras_com_qrcode
    )

@app.route("/buscar-endereco", methods=["POST"])
def pesquisar_endereco():
    if "usuario" not in session:
        return jsonify({
            "status": "erro",
            "mensagem": "Acesso não autorizado."
        }), 401

    dados = request.get_json(silent=True) or {}

    resultado = buscar_endereco(dados.get("endereco"))

    if resultado["status"] == "erro":
        return jsonify(resultado), 400

    return jsonify(resultado), 200

@app.route("/buscar-endereco-coordenadas", methods=["POST"])
def buscar_endereco_coordenadas():

    if "usuario" not in session:
        return jsonify({
            "status": "erro",
            "mensagem": "Acesso não autorizado."
        }), 401

    dados = request.get_json()

    latitude = dados.get("latitude")
    longitude = dados.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({
            "status": "erro",
            "mensagem": "Coordenadas não informadas."
        }), 400

    resultado = buscar_endereco_por_coordenadas(
        latitude,
        longitude
    )

    return jsonify(resultado)

@app.route("/presenca/<int:palestra_id>", methods=["GET", "POST"])
def presenca(palestra_id):

    # Busca a palestra no banco
    palestra = buscar_palestra(palestra_id)

    # Verifica se a palestra existe
    if palestra is None:
        resultado = {
            "status": "erro",
            "mensagem": "Palestra não encontrada."
        }

        return render_template(
            "resultado.html",
            resultado=resultado,
            palestra_id=None
        )

    if request.method == "POST":

        nome = request.form.get("nome")
        ra = request.form.get("ra")

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        resultado = registrar(
            nome,
            ra,
            latitude,
            longitude,
            palestra_id
        )

        return render_template(
            "resultado.html",
            resultado=resultado,
            palestra_id=palestra_id
        )

    return render_template(
        "index.html",
        palestra=palestra
    )


if __name__ == "__main__":
    app.run(debug=True)
