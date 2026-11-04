
import math

from models.presenca_model import (
    verificar_ra,
    registrar_presenca,
    buscar_palestra
)


def calcular_distancia(lat1, lon1, lat2, lon2):

    # Raio médio da Terra em metros
    raio_terra = 6371000

    # Converte graus para radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferenças entre as coordenadas
    diferenca_lat = lat2 - lat1
    diferenca_lon = lon2 - lon1

    # Fórmula de Haversine
    a = (
        math.sin(diferenca_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(diferenca_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia = raio_terra * c

    return distancia


def registrar(nome, ra, latitude, longitude, palestra_id):

    # Verifica se os campos foram preenchidos
    if not nome or not ra:
        return {
            "status": "erro",
            "mensagem": "Preencha todos os campos."
        }

    nome = nome.strip()
    ra = ra.strip()

    if not nome or not ra:
        return {
            "status": "erro",
            "mensagem": "Preencha todos os campos."
        }

    # Busca a palestra no banco de dados
    try:
        palestra = buscar_palestra(palestra_id)
    except (TypeError, ValueError):
        palestra = None

    if palestra is None:
        return {
            "status": "erro",
            "mensagem": "Palestra não encontrada."
        }

    # Verifica se a localização foi recebida
    try:
        latitude = float(latitude)
        longitude = float(longitude)

    except (TypeError, ValueError):
        return {
            "status": "erro",
            "mensagem": "Não foi possível identificar sua localização."
        }

    # Verifica se as coordenadas são válidas
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return {
            "status": "erro",
            "mensagem": "As coordenadas informadas são inválidas."
        }

    # Calcula a distância até o local da palestra
    distancia = calcular_distancia(
        latitude,
        longitude,
        palestra["latitude"],
        palestra["longitude"]
    )

    # Verifica se está dentro do raio permitido
    if distancia > palestra["raio_permitido"]:
        return {
            "status": "erro",
            "mensagem": "Você está fora da área permitida para registrar presença."
        }

    # Verifica se o RA já está registrado naquela palestra
    if verificar_ra(ra, palestra_id):
        return {
            "status": "duplicado",
            "mensagem": "Este RA já possui presença registrada nesta palestra."
        }

    # Registra a presença
    sucesso = registrar_presenca(nome, ra, palestra_id)

    if not sucesso:
        return {
            "status": "duplicado",
            "mensagem": "Este RA já possui presença registrada nesta palestra."
        }

    return {
        "status": "sucesso",
        "mensagem": "Presença registrada com sucesso!"
    }
