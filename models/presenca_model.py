import csv
import os

CAMINHO_CSV = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "presencas.csv"
)


def criar_arquivo():
    os.makedirs(os.path.dirname(CAMINHO_CSV), exist_ok=True)

    if not os.path.exists(CAMINHO_CSV):
        with open(CAMINHO_CSV, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["nome", "ra"])


def verificar_ra(ra):
    criar_arquivo()

    with open(CAMINHO_CSV, "r", newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)

        for registro in leitor:
            if registro["ra"].strip() == ra.strip():
                return True

    return False


def registrar_presenca(nome, ra):
    criar_arquivo()

    if verificar_ra(ra):
        return False

    with open(CAMINHO_CSV, "a", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome, ra])

    return True
