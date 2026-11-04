
from models.presenca_model import (
    criar_arquivo,
    verificar_ra,
    registrar_presenca
)

print("=== TESTE DO MODEL ===")

# Teste 1: criação do CSV
criar_arquivo()
print("\n1. Arquivo CSV criado com sucesso!")

# Teste 2: registro de estudante
resultado = registrar_presenca("Maria Silva", "123456")

if resultado:
    print("2. Estudante registrado com sucesso!")
else:
    print("2. Estudante já estava registrado.")

# Teste 3: verificação de matrícula
resultado = verificar_ra("123456")

if resultado:
    print("3. RA encontrado no arquivo CSV!")
else:
    print("3. RA não encontrado.")

# Teste 4: tentativa de duplicidade
resultado = registrar_presenca("Maria Silva", "123456")

if resultado:
    print("4. ERRO: matrícula duplicada foi aceita!")
else:
    print("4. Sucesso: matrícula duplicada bloqueada!")

print("\n=== TESTES FINALIZADOS ===")
