
import os
import psycopg

from dotenv import load_dotenv


load_dotenv()


def obter_conexao():
    """Estabelece conexão com o banco PostgreSQL."""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não encontrada.")

    return psycopg.connect(database_url)


def criar_tabelas():
    """Cria as tabelas do sistema, caso ainda não existam."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS palestras (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nome VARCHAR(200) NOT NULL,
                    data TIMESTAMP NOT NULL,
                    local VARCHAR(300) NOT NULL,
                    latitude DOUBLE PRECISION NOT NULL,
                    longitude DOUBLE PRECISION NOT NULL,
                    raio_permitido INTEGER NOT NULL DEFAULT 100
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS presencas (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    palestra_id BIGINT NOT NULL,
                    nome VARCHAR(200) NOT NULL,
                    ra VARCHAR(50) NOT NULL,
                    data_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    CONSTRAINT fk_palestra
                        FOREIGN KEY (palestra_id)
                        REFERENCES palestras(id)
                        ON DELETE CASCADE,

                    CONSTRAINT uq_presenca_palestra_ra
                        UNIQUE (palestra_id, ra)
                );
            """)

            cursor.execute("""
                ALTER TABLE presencas
                ADD COLUMN IF NOT EXISTS device_token TEXT;
            """)

            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS uq_presenca_palestra_device_token
                ON presencas (palestra_id, device_token);
            """)

def verificar_ra(ra, palestra_id):
    """Verifica se o RA já está registrado naquela palestra."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT 1
                FROM presencas
                WHERE ra = %s AND palestra_id = %s
                LIMIT 1;
            """, (ra.strip(), palestra_id))

            return cursor.fetchone() is not None

def verificar_device_token(device_token, palestra_id):
    """Verifica se o dispositivo já registrou presença naquela palestra."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT 1
                FROM presencas
                WHERE device_token = %s
                  AND palestra_id = %s
                LIMIT 1;
            """, (device_token, palestra_id))

            return cursor.fetchone() is not None

def registrar_presenca(nome, ra, palestra_id, device_token):
    """Registra a presença de um participante."""

    try:
        with obter_conexao() as conexao:
            with conexao.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO presencas (nome, ra, palestra_id, device_token)
                    VALUES (%s, %s, %s, %s);
                """, (
                    nome.strip(),
                    ra.strip(),
                    palestra_id,
                    device_token
                ))

        return True

    except psycopg.errors.UniqueViolation:
        return False

def buscar_palestra(palestra_id):
    """Busca os dados de uma palestra pelo ID."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT id, nome, data, local, latitude, longitude, raio_permitido
                FROM palestras
                WHERE id = %s;
            """, (palestra_id,))

            palestra = cursor.fetchone()

            if palestra is None:
                return None

            return {
                "id": palestra[0],
                "nome": palestra[1],
                "data": palestra[2],
                "local": palestra[3],
                "latitude": palestra[4],
                "longitude": palestra[5],
                "raio_permitido": palestra[6]
            }


def criar_palestra(nome, data, local, latitude, longitude, raio_permitido=100):
    """Cadastra uma nova palestra no banco de dados."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                INSERT INTO palestras
                (nome, data, local, latitude, longitude, raio_permitido)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                nome.strip(),
                data,
                local.strip(),
                latitude,
                longitude,
                raio_permitido
            ))

            resultado = cursor.fetchone()
            return resultado[0]


def atualizar_palestra(
    palestra_id,
    nome,
    data,
    local,
    latitude,
    longitude,
    raio_permitido=100
):
    """Atualiza os dados de uma palestra existente."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                UPDATE palestras
                SET
                    nome = %s,
                    data = %s,
                    local = %s,
                    latitude = %s,
                    longitude = %s,
                    raio_permitido = %s
                WHERE id = %s;
            """, (
                nome.strip(),
                data,
                local.strip(),
                latitude,
                longitude,
                raio_permitido,
                palestra_id
            ))

            return cursor.rowcount > 0

def listar_palestras():
    """Retorna todas as palestras cadastradas."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT id, nome, data, local
                FROM palestras
                ORDER BY data DESC;
            """)

            return cursor.fetchall()

def listar_presencas(palestra_id):
    """Retorna as presenças de uma palestra com seus dados."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT
                    palestras.nome,
                    palestras.data,
                    presencas.nome,
                    presencas.ra,
                    presencas.data_registro
                FROM presencas
                INNER JOIN palestras
                    ON presencas.palestra_id = palestras.id
                WHERE palestras.id = %s
                ORDER BY presencas.data_registro ASC;
            """, (palestra_id,))

            return cursor.fetchall()

def listar_relatorio_presencas():
    """Retorna cada palestra com sua quantidade de participantes."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT
                    palestras.id,
                    palestras.nome,
                    palestras.data,
                    COUNT(presencas.id) AS total_presencas
                FROM palestras
                LEFT JOIN presencas
                    ON palestras.id = presencas.palestra_id
                GROUP BY
                    palestras.id,
                    palestras.nome,
                    palestras.data
                ORDER BY total_presencas DESC, palestras.data DESC;
            """)

            return cursor.fetchall()

def excluir_palestra(palestra_id):
    """Exclui uma palestra pelo ID."""

    with obter_conexao() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                DELETE FROM palestras
                WHERE id = %s;
            """, (palestra_id,))

            return cursor.rowcount > 0