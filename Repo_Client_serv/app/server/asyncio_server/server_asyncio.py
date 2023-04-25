import asyncio
import datetime
import socket
import logging

from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.message import DecodeError

from app.server.common import pr_pb2 as pr
from app.server.common.read_config import read_ini

#reading and decoding the message
async def read_mes(data, pos, typeMes):
    msg_len, pos = _DecodeVarint32(data, pos)
    try:
        msg_buf = data[pos:(pos + msg_len)]
        #msg_buf = data[1000]
    except IndexError:
        logging.error('An incomplete message was received')
        return 0, 0
    message = typeMes
    try:
        message.ParseFromString(msg_buf)
    except DecodeError:
        logging.error('The message could not be decoded')
        return 0, 0
    pos += msg_len
    return message, pos

#reading all received messages
async def collect_mes(data):
    pos = 0
    messages = []
    while pos < len(data):
        message, pos = await read_mes(data, pos, pr.WrapperMessage())
        if message:
            messages.append(message)
        else:
            return messages
    return messages

#encoding of the message
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

            # data processing
            messages = await collect_mes(data)
            for message in messages:
                if type(message) == pr.WrapperMessage:
                    if message.HasField('slow_response') or message.HasField('fast_response'):
                        client_count -= 1
                        break
                else:
                    client_count -= 1
                    break
                if message.HasField('request_for_slow_response'):
                    resp = pr.WrapperMessage()
                    resp.slow_response.connected_client_count = client_count
                    await asyncio.sleep(message.request_for_slow_response.time_in_seconds_to_sleep)
                elif message.HasField('request_for_fast_response'):
                    resp = pr.WrapperMessage()
                    s = str(datetime.datetime.now().isoformat()).replace('-', '')
                    s = s.replace(':', '')
                    resp.fast_response.current_date_time = s

                # sending data
                resp = await send_mes(resp)
                await loop.sock_sendall(client, resp)
            client_count-=1
            break
    logging.info('Close connection from {}\n'.format(addr))


if __name__ == '__main__':
    global client_count
    client_count = 0
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.basicConfig(level=logging.INFO, filename="./logs_asyncio.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    port = read_ini('../../configs/config.ini', 'asyncio')
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