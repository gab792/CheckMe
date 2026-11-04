
import math

from models.presenca_model import verificar_ra, registrar_presenca
from config.config import LATITUDE, LONGITUDE, RAIO_PERMITIDO


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


def registrar(nome, ra, latitude, longitude):

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

    # Verifica se o local autorizado foi configurado
    if LATITUDE is None or LONGITUDE is None:
        return {
            "status": "erro",
            "mensagem": "A localização do evento ainda não foi configurada."
        }

    # Calcula a distância até o local autorizado
    distancia = calcular_distancia(
        latitude,
        longitude,
        LATITUDE,
        LONGITUDE
    )

    # Verifica se o participante está dentro do raio permitido
    if distancia > RAIO_PERMITIDO:
        return {
            "status": "erro",
            "mensagem": "Você está fora da área permitida para registrar presença."
        }

    # Verifica se o RA já possui presença registrada
    if verificar_ra(ra):
        return {
            "status": "duplicado",
            "mensagem": "Este RA já possui presença registrada."
        }

    # Registra a presença
    registrar_presenca(nome, ra)

    return {
        "status": "sucesso",
        "mensagem": "Presença registrada com sucesso!"
    }
