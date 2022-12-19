from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import pickle
import datetime
import logging
import pr_pb2 as pr
import server.common.read_config as conf


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
            message = pickle.loads(data)
            if type(message) == pr.WrapperMessage:
                if message.slow_response.connected_client_count !=0 or len(message.fast_response.current_date_time)!=0:
                    out = pickle.dumps(ValueError)
                    self.transport.write(out)
                    self.transport.loseConnection()
                    break
                else:
                    pass
            else:
                out = pickle.dumps(ValueError)
                self.transport.write(out)
                self.transport.loseConnection()
                break
            if message.request_for_slow_response.time_in_seconds_to_sleep != 0:
                sec = int(message.request_for_slow_response.time_in_seconds_to_sleep)
                reactor.callLater(sec, self.wake_up)
            else:
                out_put = pr.WrapperMessage()
                s = str(datetime.datetime.now().isoformat()).replace('-', '')
                s = s.replace(':', '')
                out_put.fast_response.current_date_time = s
                out = pickle.dumps(out_put)
                self.transport.write(out)
                self.transport.loseConnection()

    def wake_up(self):
        out_put = pr.WrapperMessage()
        out_put.slow_response.connected_client_count = len(self.users)
        out = pickle.dumps(out_put)
        self.transport.write(out)
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
