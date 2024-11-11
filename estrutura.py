import threading
import queue
import time
import random
import matplotlib.pyplot as plt

# Configurações de simulação
BUFFER_SIZE = 5       # Tamanho máximo do buffer
NUM_OPERACOES = 20    # Total de operações de produção e consumo
NUM_PRODUTORES = 3    # Número de threads produtoras
NUM_CONSUMIDORES = 3  # Número de threads consumidoras

# Criando o buffer com capacidade limitada
buffer = queue.Queue(BUFFER_SIZE)

# Semáforos para controle de produção e consumo
sem_vazio = threading.Semaphore(BUFFER_SIZE)  # Limite de espaço no buffer
sem_cheio = threading.Semaphore(0)             # Quantidade de itens no buffer

# Mutex para controlar o acesso ao buffer
mutex = threading.Lock()

# Dados para análise
historico_buffer = []  # Quantidade de itens no buffer ao longo do tempo
tempo_eventos = []     # Tempo em que cada evento ocorreu

# Função do Produtor
def produtor(id_produtor):
    for _ in range(NUM_OPERACOES // NUM_PRODUTORES):
        # Produz uma "peça"
        peca = f"Peça-{id_produtor}-{random.randint(1, 100)}"
        sem_vazio.acquire()  # Espera que haja espaço no buffer
        with mutex:
            buffer.put(peca)  # Adiciona a peça no buffer
            historico_buffer.append(buffer.qsize())  # Armazena o tamanho atual do buffer
            tempo_eventos.append(time.time())        # Armazena o timestamp
            print(f"Produtor {id_produtor} produziu {peca}")
        sem_cheio.release()  # Sinaliza que há mais um item disponível no buffer
        time.sleep(random.uniform(0.5, 1.5))  # Tempo de produção

# Função do Consumidor
def consumidor(id_consumidor):
    for _ in range(NUM_OPERACOES // NUM_CONSUMIDORES):
        sem_cheio.acquire()  # Espera que haja item no buffer
        with mutex:
            peca = buffer.get()  # Remove uma peça do buffer
            historico_buffer.append(buffer.qsize())  # Armazena o tamanho atual do buffer
            tempo_eventos.append(time.time())        # Armazena o timestamp
            print(f"Consumidor {id_consumidor} consumiu {peca}")
        sem_vazio.release()  # Sinaliza que há espaço no buffer
        time.sleep(random.uniform(0.5, 1.5))  # Tempo de consumo

# Criando e inicializando threads de produtores e consumidores
produtores = [threading.Thread(target=produtor, args=(i,)) for i in range(NUM_PRODUTORES)]
consumidores = [threading.Thread(target=consumidor, args=(i,)) for i in range(NUM_CONSUMIDORES)]

# Iniciando threads dos produtores e consumidores
for p in produtores:
    p.start()
for c in consumidores:
    c.start()

# Aguardando o término das threads
for p in produtores:
    p.join()
for c in consumidores:
    c.join()

# Gráfico de quantidade de itens no buffer ao longo do tempo
plt.plot(tempo_eventos, historico_buffer)
plt.xlabel("Tempo")
plt.ylabel("Quantidade de Itens no Buffer")
plt.title("Produção e Consumo de Itens no Buffer ao Longo do Tempo")
plt.show()
