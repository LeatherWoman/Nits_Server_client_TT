import asyncio
import datetime
import pickle
import socket
import pr_pb2 as pr


async def main(port = 5004):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port)) #Метод используется для связывания сокета с определенным сетевым интерфейсом и номером порта:
    server.listen()
    server.setblocking(False)

    while True:
        client, addr = await loop.sock_accept(server)
        if client:
            global client_count
            client_count += 1
            print('Connection from {}'.format(addr))
            loop.create_task(handler(client))

async def handler(client):
    global client_count
    with client:
        while True:
            data = await loop.sock_recv(client, 1000)
            if not data:
                break
            message = pickle.loads(data)
            print('Data received: {!r}'.format(message))
            print(type(message))
            print(message.request_for_slow_response)
            print(message.request_for_slow_response!='')
            print(type(message.request_for_slow_response))
            if message.request_for_slow_response.time_in_seconds_to_sleep!=0:
                print(datetime.datetime.now())
                await asyncio.sleep(message.request_for_slow_response.time_in_seconds_to_sleep)
                print(datetime.datetime.now())
                glob_glob = pr.WrapperMessage()
                glob_glob.slow_response.connected_client_count = client_count
                print("IN IF")
            else:
                print(datetime.datetime.now())
                glob_glob = pr.WrapperMessage()
                glob_glob.fast_response.current_date_time = str(datetime.datetime.now())
                print("IN ELIF")
            data2 = pickle.dumps(glob_glob)
            print('Send: {!r}'.format(data2))
            await loop.sock_sendall(client, data2)
            client_count-=1
            loop.close()
    print('Close connection')



if __name__ == '__main__':
    global client_count
    client_count = 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()