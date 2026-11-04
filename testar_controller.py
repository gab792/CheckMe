
import controllers.presenca_controller as controller

print("=== TESTE COMPLETO DO CONTROLLER ===")

# Coordenadas fictícias para os testes
controller.LATITUDE = -23.5500
controller.LONGITUDE = -46.6300

# Teste 1: participante dentro do raio permitido
resultado = controller.registrar(
    "Aluno Teste",
    "TESTE987654",
    -23.5500,
    -46.6300
)

print("\n1. Registro dentro da área:")
print(resultado)

# Teste 2: tentativa de registro duplicado
resultado = controller.registrar(
    "Aluno Teste",
    "TESTE987654",
    -23.5500,
    -46.6300
)

print("\n2. Tentativa de duplicidade:")
print(resultado)

# Teste 3: participante fora do raio permitido
resultado = controller.registrar(
    "Outro Aluno",
    "TESTE987655",
    -23.5510,
    -46.6300
)

print("\n3. Registro fora da área:")
print(resultado)

print("\n=== TESTES FINALIZADOS ===")
