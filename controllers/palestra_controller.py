
from datetime import datetime

from models.presenca_model import criar_palestra


def cadastrar_palestra(nome, data, local, latitude, longitude, raio_permitido=100):
    """Valida os dados e cadastra uma nova palestra."""

    try:
        if not all([nome, data, local, latitude, longitude]):
            return {
                "status": "erro",
                "mensagem": "Preencha todos os campos."
            }

        data_formatada = datetime.fromisoformat(data)

        latitude = float(latitude)
        longitude = float(longitude)
        raio_permitido = int(raio_permitido)

        if not -90 <= latitude <= 90:
            raise ValueError

        if not -180 <= longitude <= 180:
            raise ValueError

        if raio_permitido <= 0:
            raise ValueError

        palestra_id = criar_palestra(
            nome,
            data_formatada,
            local,
            latitude,
            longitude,
            raio_permitido
        )

        return {
            "status": "sucesso",
            "mensagem": "Palestra cadastrada com sucesso!",
            "palestra_id": palestra_id
        }

    except (ValueError, TypeError):
        return {
            "status": "erro",
            "mensagem": "Verifique os dados informados."
        }
