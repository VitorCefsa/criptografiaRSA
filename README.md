# Documentação do Código RSA (Cliente e Servidor)

## Descrição Geral

Este código implementa um sistema de comunicação segura utilizando o algoritmo RSA, onde um cliente se conecta a um servidor e troca mensagens de forma criptografada. O cliente e o servidor geram suas chaves RSA de 4096 bits e trocam chaves públicas para encriptar e descriptografar mensagens. O código foi implementado sem o uso de bibliotecas externas para o cálculo das chaves, criptografia e decriptação.

---

## Estrutura do Código

O sistema é composto por dois scripts principais:

1. **clientRSA.py**: Representa o cliente que se conecta ao servidor, envia uma mensagem criptografada e recebe a resposta também criptografada.
2. **serverRSA.py**: Representa o servidor que recebe a mensagem do cliente, processa e envia uma resposta de volta ao cliente.

---

## 1. `clientRSA.py`

### Funções:

  - Testa se um número `n` é primo usando o teste de Miller-Rabin. Este teste é probabilístico e é executado `k` vezes para aumentar a certeza do resultado.

  - Gera um número primo de `bits` bits. O número gerado será ímpar e de tamanho específico, e passa pelo teste de primalidade.

  - Gera um par de chaves RSA: pública e privada. A chave pública é composta por `(n, e)` e a chave privada é composta por `(n, d)`. O algoritmo utiliza números primos gerados com 512 bits cada para formar a chave RSA.

  - Criptografa uma mensagem utilizando a chave pública `(e, n)` através do algoritmo RSA.

  - Descriptografa uma mensagem utilizando a chave privada `(d, n)`.

### Fluxo:

1. Geração de chaves RSA para o cliente.
2. O cliente se conecta ao servidor via socket TCP e envia sua chave pública.
3. O cliente recebe a chave pública do servidor.
4. O cliente pede uma mensagem ao usuário, criptografa a mensagem usando a chave pública do servidor e envia para o servidor.
5. O cliente recebe uma mensagem criptografada do servidor, descriptografa utilizando sua chave privada e exibe o resultado.

---

## 2. `serverRSA.py`

### Funções:

  - Similar ao cliente, testa se um número `n` é primo usando o teste de Miller-Rabin.

  - Gera números primos de `bits` bits para uso na geração das chaves RSA.

  - Gera um par de chaves RSA para o servidor. O processo é similar ao do cliente, com a criação de números primos e o cálculo das chaves.

  - Criptografa uma mensagem utilizando a chave pública `(e, n)`.

  - Descriptografa uma mensagem utilizando a chave privada `(d, n)`.

### Fluxo:

1. Geração de chaves RSA para o servidor.
2. O servidor aguarda uma conexão de cliente e aceita a conexão.
3. O servidor recebe a chave pública do cliente e envia sua própria chave pública para o cliente.
4. O servidor recebe uma mensagem criptografada do cliente, descriptografa usando sua chave privada e transforma a mensagem para letras maiúsculas.
5. O servidor recriptografa a resposta com a chave pública do cliente e envia a mensagem criptografada de volta ao cliente.

---

## Detalhamento do Processo RSA

1. **Geração de Chaves**:
   - O processo de geração das chaves é realizado no momento da execução do código. A chave pública é composta pelos valores `(n, e)` e a chave privada é composta por `(n, d)`.
   - O valor `n` é o produto de dois números primos `p` e `q`.
   - O valor `e` é escolhido como 65537, um valor padrão em implementações seguras.
   - O valor `d` é o inverso modular de `e` em relação a `(p - 1) * (q - 1)`.

2. **Criptografia**:
   - Para criptografar uma mensagem, utiliza-se a fórmula:
     \[
     C = M^e \mod n
     \]
     Onde `M` é o valor numérico de cada caractere da mensagem.

3. **Descriptografia**:
   - Para descriptografar, utiliza-se a fórmula:
     \[
     M = C^d \mod n
     \]
     Onde `C` é a mensagem criptografada e `M` é a mensagem original.

4. **Troca de Chaves e Mensagens**:
   - O cliente e o servidor trocam suas chaves públicas via socket.
   - O cliente criptografa a mensagem com a chave pública do servidor e a envia.
   - O servidor descriptografa a mensagem com sua chave privada, processa e envia a resposta, criptografada com a chave pública do cliente.

---

## Considerações Finais

- **Segurança**: A segurança do algoritmo RSA depende da dificuldade de fatorar números grandes. Para garantir uma comunicação segura, as chaves devem ser suficientemente grandes (no código, 4096 bits são utilizados).
- **Desempenho**: O uso de chaves de 4096 bits pode impactar o desempenho, especialmente para operações de criptografia e descriptografia.
- **Sockets**: A comunicação entre o cliente e o servidor é feita utilizando a biblioteca `socket`, configurando um servidor TCP que escuta na porta 1300 e aceita conexões de clientes.

---

## Exemplo de Execução

**Cliente**:

