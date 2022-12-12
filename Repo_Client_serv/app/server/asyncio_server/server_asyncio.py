import asyncio
import datetime
import pickle
import socket
import logging
import pr_pb2 as pr
import server.common.read_config as conf

async def main(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port)) #Метод используется для связывания сокета с определенным сетевым интерфейсом и номером порта
    server.listen(1)
    server.setblocking(False)

    while True:
        client, addr = await loop.sock_accept(server)
        if client:
            global client_count
            client_count += 1
            logging.info('Connection from {}\n'.format(addr))
            loop.create_task(handler(client, addr))



async def handler(client, addr):
    global client_count
    with client:
        while True:
            data = await loop.sock_recv(client, 1000)
            if not data:
                break
            message = pickle.loads(data)
            print('Data received:\n{!r}'.format(message))
            if type(message)==pr.WrapperMessage:
                if message.slow_response.connected_client_count !=0 or len(message.fast_response.current_date_time)!=0:
                    data2 = pickle.dumps(ValueError)
                    print('Send: {!r}'.format(data2))
                    await loop.sock_sendall(client, data2)
                    client_count-=1
                    break
                else:
                    pass
            else:
                data2 = pickle.dumps(ValueError)
                print('Send: {!r}'.format(data2))
                await loop.sock_sendall(client, data2)
                client_count-=1
                break
            if message.request_for_slow_response.time_in_seconds_to_sleep != 0:
                resp = pr.WrapperMessage()
                resp.slow_response.connected_client_count = client_count
                await asyncio.sleep(message.request_for_slow_response.time_in_seconds_to_sleep)
            else:
                resp = pr.WrapperMessage()
                s = str(datetime.datetime.now().isoformat()).replace('-', '')
                s = s.replace(':', '')
                resp.fast_response.current_date_time = s
            data2 = pickle.dumps(resp)
            print('Send: {!r}'.format(data2))
            await loop.sock_sendall(client, data2)
            client_count-=1
            break
    logging.info('Close connection from {}\n'.format(addr))



if __name__ == '__main__':
    global client_count
    client_count = 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.basicConfig(level=logging.INFO, filename="logs_asyncio.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    port = conf.read_ini('../../configs/config.ini', 'asyncio')
    print(port)
    loop.create_task(main(port))
    loop.run_forever()
