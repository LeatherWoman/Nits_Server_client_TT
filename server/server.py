import asyncio
import datetime
import pickle


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = pickle.loads(data)
        print('Data received: {!r}'.format(message.request_for_slow_response.time_in_seconds_to_sleep))
        print(datetime.datetime.now())
        #await asyncio.sleep(message.request_for_slow_response.time_in_seconds_to_sleep)
        #await asyncio.sleep(1)
        print(datetime.datetime.now())

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    # Получаем ссылку на цикл событий, т.к. планируем
    # использовать низкоуровневый API.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
         lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
