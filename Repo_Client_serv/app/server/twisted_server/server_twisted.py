from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
import datetime
import logging
import pr_pb2 as pr
import app.server.common.read_config as conf


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
            pos = 0
            while pos < len(data):
                message, pos = self.read_mes(data, pos)
                #добавить исключение, если сообщение пришло не полностью
                if type(message) == pr.WrapperMessage:
                    if message.HasField('slow_response') or message.HasField('fast_response'):
                        self.transport.write(data)
                        self.transport.loseConnection()
                        break
                    else:
                        pass
                else:
                    self.transport.write(data)
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

    #чтение и декодирование сообщения
    def read_mes(self, data, pos):
        msg_len, new_pos = _DecodeVarint32(data, pos)
        pos = new_pos
        #добавит проверку на выход за границы
        msg_buf = data[pos:(pos + msg_len)]
        pos += msg_len
        message = pr.WrapperMessage()
        message.ParseFromString(msg_buf)
        return message, pos

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
    port = conf.read_ini('../../configs/config.ini', 'twisted')
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(ServerFactory())
    logging.basicConfig(level=logging.INFO, filename="logs_twisted.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    reactor.run()
