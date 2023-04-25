from google.protobuf.message import DecodeError
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
import datetime
import logging

from app.server.common import pr_pb2 as pr
from app.server.common.read_config import read_ini


class Server(Protocol):
    def __init__(self, users):
        self.users = users

    def connectionMade(self):
        d = self.transport.getPeer()
        logging.info('Connection from {}\n'.format((d.host, d.port)))
        self.users.append(self)

    # Событие dataReceived - получение и отправление данных
    def dataReceived(self, data):
        for user in self.users:
            messages = self.collect_mes(data)
            if messages:
                for message in messages:
                    if type(message) == pr.WrapperMessage:
                        if message.HasField('slow_response') or message.HasField('fast_response'):
                            self.transport.loseConnection()
                            break
                    else:
                        self.transport.loseConnection()
                        break

                    if message.HasField('request_for_slow_response'):
                        sec = int(message.request_for_slow_response.time_in_seconds_to_sleep)
                        reactor.callLater(sec, self.wake_up)
                    elif message.HasField('request_for_fast_response'):
                        out_put = pr.WrapperMessage()
                        s = str(datetime.datetime.now().isoformat()).replace('-', '')
                        s = s.replace(':', '')
                        out_put.fast_response.current_date_time = s
                        self.transport.write(self.send_mes(out_put))
                        self.transport.loseConnection()
            else:
                self.transport.loseConnection()


    #чтение и декодирование сообщения
    def read_mes(self, data, pos, typeMes):
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

    def collect_mes(self, data):
        pos = 0
        messages = []
        while pos < len(data):
            message, pos = self.read_mes(data, pos, pr.WrapperMessage())
            if message:
                messages.append(message)
            else:
                return messages
        return messages

    #кодирование сообщения
    def send_mes(self, resp):
        size = resp.ByteSize()
        packed_len = _VarintBytes(size)
        data2 = resp.SerializeToString()
        return packed_len+data2

    def wake_up(self):
        out_put = pr.WrapperMessage()
        out_put.slow_response.connected_client_count = len(self.users)
        self.transport.write(self.send_mes(out_put))
        self.transport.loseConnection()

    # Событие connectionLost срабатывает при разрыве соединения с клиентом
    def connectionLost(self, reason):
        self.users.remove(self)
        d = self.transport.getPeer()
        logging.info('Close connection from {}\n'.format((d.host, d.port)))

class ServerFactory(ServFactory):
    def __init__(self):
        self.users = []

    def buildProtocol(self, addr):
        return Server(self.users)


if __name__ == '__main__':
    port = read_ini('../../configs/config.ini', 'twisted')
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(ServerFactory())
    logging.basicConfig(level=logging.INFO, filename="./logs_twisted.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    reactor.run()
