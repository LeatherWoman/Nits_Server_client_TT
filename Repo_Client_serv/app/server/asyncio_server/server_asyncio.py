import asyncio
import datetime
import socket
import logging

from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32

import pr_pb2 as pr
import app.server.common.read_config as conf

#чтение и декодирование сообщения
async def read_mes(data, pos):
    msg_len, new_pos = _DecodeVarint32(data, pos)
    pos = new_pos
    msg_buf = data[pos:(pos + msg_len)]
    pos += msg_len
    message = pr.WrapperMessage()
    message.ParseFromString(msg_buf)
    return message, pos

#кодирование сообщения
async def send_mes(resp):
    size = resp.ByteSize()
    packed_len = _VarintBytes(size)
    data2 = resp.SerializeToString()
    return packed_len+data2

#create socket and connect with the client
async def main(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port))
    server.listen(1)
    server.setblocking(False)

    while True:
        client, addr = await loop.sock_accept(server)
        if client:
            global client_count
            client_count += 1
            logging.info('Connection from {}\n'.format(addr))
            loop.create_task(handler(client, addr))


#receiving and sending data
async def handler(client, addr):
    global client_count
    with client:
        while True:
            #receiving data
            data = await loop.sock_recv(client, 1000)
            if not data:
                break
            pos = 0
            while pos < len(data):
                message, pos = await read_mes(data, pos)
                if type(message) == pr.WrapperMessage:
                    if message.HasField('slow_response') or message.HasField('fast_response'):
                        await loop.sock_sendall(client, data)
                        client_count -= 1
                        break
                    else:
                         pass
                else:
                    await loop.sock_sendall(client, data)
                    client_count -= 1
                    break

                #data processing
                if message.HasField('request_for_slow_response'):
                    resp = pr.WrapperMessage()
                    resp.slow_response.connected_client_count = client_count
                    await asyncio.sleep(message.request_for_slow_response.time_in_seconds_to_sleep)
                elif message.HasField('request_for_fast_response'):
                    resp = pr.WrapperMessage()
                    s = str(datetime.datetime.now().isoformat()).replace('-', '')
                    s = s.replace(':', '')
                    resp.fast_response.current_date_time = s

                #sending data
                resp = await send_mes(resp)
                print('send')
                await loop.sock_sendall(client, resp)
            client_count-=1
            break
        print('end while')
    logging.info('Close connection from {}\n'.format(addr))



if __name__ == '__main__':
    global client_count
    client_count = 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.basicConfig(level=logging.INFO, filename="logs_asyncio.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    port = conf.read_ini('../../configs/config.ini', 'asyncio')
    loop.create_task(main(port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()