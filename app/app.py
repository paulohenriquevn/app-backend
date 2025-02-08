import asyncio
import websockets
import pika
from config import WEBSOCKET_HOST, WEBSOCKET_PORT

# Criamos um loop de eventos global
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Lista global de clientes WebSocket conectados
clients = set()

RABBITMQ_QUEUE = "processa_modelos"
WEBSOCKET_HOST =  "0.0.0.0"
WEBSOCKET_PORT =  8765

async def handler(websocket):
    """ Gerencia conexões WebSocket """
    clients.add(websocket)
    print(f"🔗 Cliente conectado. Total de clientes: {len(clients)}")

    try:
        async for message in websocket:
            print(f"📨 Mensagem recebida do cliente: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("⚠ Cliente desconectado.")
    finally:
        clients.remove(websocket)

async def send_to_clients(message):
    """ Envia mensagens para todos os clientes WebSocket conectados """
    if clients:
        print(f"📤 Enviando para {len(clients)} clientes: {message}")
        # Criar tarefas assíncronas corretamente
        tasks = [asyncio.ensure_future(client.send(message)) for client in clients]
        await asyncio.gather(*tasks, return_exceptions=True)

def callback(ch, method, properties, body):
    """ Função chamada quando uma nova mensagem chega no RabbitMQ """
    message = body.decode("utf-8")
    print(f"📩 Mensagem recebida do RabbitMQ: {message}")

    # Agendamos a execução assíncrona corretamente
    future = asyncio.run_coroutine_threadsafe(send_to_clients(message), loop)
    try:
        future.result()  # Garante que a execução foi bem-sucedida
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem WebSocket: {e}")

def rabbitmq_worker():
    """ Conecta ao RabbitMQ e começa a consumir mensagens (executado em thread separada) """
    credentials = pika.PlainCredentials('paulo', 'paulo@123')
    parameters = pika.ConnectionParameters('95.216.210.178', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

    print("🐇 Aguardando mensagens do RabbitMQ...")
    channel.start_consuming()

async def start_websocket():
    """ Inicia o servidor WebSocket e o consumidor RabbitMQ simultaneamente """
    print(f"🚀 Servidor WebSocket rodando em ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")

    # Inicia o servidor WebSocket
    server = await websockets.serve(handler, WEBSOCKET_HOST, WEBSOCKET_PORT)

    # Inicia o consumo do RabbitMQ em uma thread separada
    loop.run_in_executor(None, rabbitmq_worker)

    await server.wait_closed()

if __name__ == "__main__":
    loop.run_until_complete(start_websocket())
