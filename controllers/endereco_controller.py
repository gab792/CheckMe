
import requests


def buscar_endereco(endereco):
    """Pesquisa endereços exclusivamente no Brasil."""

    if not endereco or not endereco.strip():
        return {
            "status": "erro",
            "mensagem": "Informe um endereço para pesquisar."
        }

    url = "https://nominatim.openstreetmap.org/search"

    parametros = {
        "q": endereco.strip(),
        "format": "jsonv2",
        "countrycodes": "br",
        "limit": 5,
        "addressdetails": 1
    }

    cabecalho = {
        "User-Agent": "CheckMe/1.0"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            headers=cabecalho,
            timeout=10
        )

        resposta.raise_for_status()
        resultados = resposta.json()

        enderecos = []

        for resultado in resultados:
            enderecos.append({
                "endereco": resultado.get("display_name"),
                "latitude": float(resultado["lat"]),
                "longitude": float(resultado["lon"])
            })

        return {
            "status": "sucesso",
            "enderecos": enderecos
        }

    except requests.RequestException:
        return {
            "status": "erro",
            "mensagem": "Não foi possível realizar a pesquisa. Tente novamente."
        }

def buscar_endereco_por_coordenadas(latitude, longitude):
    """Converte coordenadas em um endereço no Brasil."""

    url = "https://nominatim.openstreetmap.org/reverse"

    parametros = {
        "lat": latitude,
        "lon": longitude,
        "format": "jsonv2",
        "zoom": 18,
        "addressdetails": 1
    }

    cabecalho = {
        "User-Agent": "CheckMe/1.0"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            headers=cabecalho,
            timeout=10
        )

        resposta.raise_for_status()
        resultado = resposta.json()

        return {
            "status": "sucesso",
            "endereco": resultado.get("display_name", "")
        }

    except requests.RequestException:
        return {
            "status": "erro",
            "mensagem": "Não foi possível identificar o endereço."
        }