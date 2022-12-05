import asyncio
import datetime
import pickle
import socket


async def main(port = 8888):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port)) #Метод используется для связывания сокета с определенным сетевым интерфейсом и номером порта:
    server.listen()
    server.setblocking(False)

    while True:
        client, addr = await loop.sock_accept(server)
        if client:
            print('Connection from {}'.format(addr))
            loop.create_task(handler(client))

async def handler(client):
    with client:
        while True:
            data = await loop.sock_recv(client, 1000)
            if not data:
                break
            message = pickle.loads(data)
            print('Data received: {!r}'.format(message.request_for_slow_response.time_in_seconds_to_sleep))
            if message.request_for_slow_response:
                print(datetime.datetime.now())
                await asyncio.sleep(message.request_for_slow_response.time_in_seconds_to_sleep)
                print(datetime.datetime.now())
            print('Send: {!r}'.format(pickle.loads(data)))
            await loop.sock_sendall(client, data)
    print('Close connection')



if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()


