
from flask import Flask, render_template, request

from controllers.presenca_controller import registrar
from models.presenca_model import criar_arquivo


app = Flask(
    __name__,
    template_folder="views/templates",
    static_folder="views/static"
)


# Cria o CSV caso ainda não exista
criar_arquivo()


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        nome = request.form.get("nome")
        ra = request.form.get("ra")

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        resultado = registrar(
            nome,
            ra,
            latitude,
            longitude
        )

        return render_template(
            "resultado.html",
            resultado=resultado
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
