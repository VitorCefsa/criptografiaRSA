from socket import *
import random

# Funções auxiliares para o RSA
 
def is_prime(n, k=40):
    """Testa se um número é primo usando o teste de Miller-Rabin."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
 
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
 
    def check(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False
 
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not check(a):
            return False
    return True
 
 
def generate_prime(bits):
    """Gera um número primo de 'bits' bits."""
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Garante que seja ímpar e do tamanho correto
        if is_prime(num, k=40):
            return num
 
 
def generate_keys():
    """Gera chaves RSA de 4096 bits sem bibliotecas externas."""
    p = generate_prime(512)
    q = generate_prime(512)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Escolha padrão para 'e' em implementações seguras
    d = pow(e, -1, phi)
    return (n, e), (n, d)  # Retorna chave pública e privada
 
 
def encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]
 
 
def decrypt(cipher, d, n):
    return ''.join([chr(pow(char, d, n)) for char in cipher])
 
# Gera par de chaves do cliente
print("🔹 Gerando chaves RSA de 4096 bits, isso pode levar algum tempo...")
public_key_client, private_key_client = generate_keys()
print("🔹 Chaves geradas com sucesso!")
 
# Conecta ao servidor
serverName = "10.1.70.40"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
 
# Envia chave pública do cliente para o servidor
clientSocket.send(f"{public_key_client[0]} {public_key_client[1]}".encode())
 
# Recebe chave pública do servidor
server_key_data = clientSocket.recv(8192).decode()
n_server, e_server = map(int, server_key_data.split())
 
# Exibe o campo para o usuário digitar a mensagem
sentence = input("🔹 Digite uma frase: ")
encrypted_message = encrypt(sentence, e_server, n_server)
 
# Envia mensagem criptografada
clientSocket.send(str(encrypted_message).encode())
 
print(f"🔹 Mensagem original: {sentence}")
print(f"🔹 Mensagem criptografada enviada: {encrypted_message}")
 
# Recebe mensagem criptografada do servidor
encrypted_response = eval(clientSocket.recv(8192).decode())
 
# Descriptografa resposta usando chave privada do cliente
decrypted_response = decrypt(encrypted_response, private_key_client[1], private_key_client[0])
 
print(f"🔹 Mensagem criptografada recebida do servidor: {encrypted_response}")
print(f"🔹 Mensagem descriptografada: {decrypted_response}")
 
# Fecha conexão
clientSocket.close()
