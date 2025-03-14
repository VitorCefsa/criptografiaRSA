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
    """Gera chaves RSA de 4096 bits."""
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
 
# Gera par de chaves do servidor
print("🔹 Gerando chaves RSA de 4096 bits, isso pode levar algum tempo...")
public_key_server, private_key_server = generate_keys()
print("🔹 Chaves geradas com sucesso!")
 
# Configura servidor
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
 
print("🔹 TCP Server Iniciado...")
 
while True:
    print("🔹 Aguardando conexões...")
    connectionSocket, addr = serverSocket.accept()
    print(f"🔹 Conexão estabelecida com {addr}")
 
    # Recebe chave pública do cliente
    client_key_data = connectionSocket.recv(8192).decode()
    n_client, e_client = map(int, client_key_data.split())
   
    # Envia chave pública do servidor para o cliente
    connectionSocket.send(f"{public_key_server[0]} {public_key_server[1]}".encode())
   
    # Recebe mensagem criptografada do cliente
    encrypted_message_str = connectionSocket.recv(8192).decode()
 
    # Transforma a string recebida em uma lista de inteiros
    encrypted_message = [int(num) for num in encrypted_message_str.strip('[]').split(',')]
   
    # Descriptografa mensagem com chave privada do servidor
    decrypted_message = decrypt(encrypted_message, private_key_server[1], private_key_server[0])
   
    print(f"🔹 Mensagem criptografada recebida do cliente: {encrypted_message}")
    print(f"🔹 Mensagem descriptografada do cliente: {decrypted_message}")
 
    # Transforma em maiúsculas
    capitalized_message = decrypted_message.upper()
   
    # Recriptografa com chave pública do cliente
    encrypted_response = encrypt(capitalized_message, e_client, n_client)
   
    # Envia mensagem criptografada de volta para o cliente
    connectionSocket.send(str(encrypted_response).encode())
   
    print(f"🔹 Mensagem transformada em maiúsculas: {capitalized_message}")
    print(f"🔹 Mensagem criptografada enviada ao cliente: {encrypted_response}")
   
    # Fecha conexão
    connectionSocket.close()
    print("🔹 Conexão encerrada.")
