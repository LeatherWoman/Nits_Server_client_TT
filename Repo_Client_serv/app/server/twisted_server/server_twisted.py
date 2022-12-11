from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.task import deferLater
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import Deferred
from autobahn.twisted.util import sleep
import pickle
import datetime
import logging
import pr_pb2 as pr
import server.common.read_config as conf


class Server(Protocol):
    def __init__(self, users):
        self.users = users

    def connectionMade(self):
        #print('connection success!')
        d = self.transport.getPeer()
        logging.info('Connection from {}\n'.format((d.host, d.port)))
        self.users.append(self)

    """@inlineCallbacks
    def slow_resp(self, secs):
        yield sleep(secs)
        return datetime.datetime.now()
        #d = Deferred()
        #reactor.callLater(secs, d.callback, None)
        #return d"""

    # Событие dataReceived - получение и отправление данных

    def dataReceived(self, data):
        for user in self.users:
            message = pickle.loads(data)
            if type(message) == pr.WrapperMessage:
                print('WrapperMessage')
            else:
                out = pickle.dumps(ValueError)
                # transport.write - отправка сообщения
                self.transport.write(out)
            if message.request_for_slow_response.time_in_seconds_to_sleep != 0:
                # print(len(message.request_for_slow_response.time_in_seconds_to_sleep))
                sec = int(message.request_for_slow_response.time_in_seconds_to_sleep)
                print(datetime.datetime.now())
                d = Deferred()
                reactor.callLater(5000, d.callback, None)
                #print(res)
                #print(datetime.datetime.now())
                out_put = pr.WrapperMessage()
                out_put.slow_response.connected_client_count = len(self.users)
                out = pickle.dumps(out_put)
                self.transport.write(out)
                #print("IN IF")
            else:
                #print('else')
                out_put = pr.WrapperMessage()
                out_put.fast_response.current_date_time = str(datetime.datetime.now())
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
        # return super().buildProtocol(addr)


if __name__ == '__main__':
    port = conf.read_ini('../../configs/config.ini', 'twisted')
    print(port)
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(ServerFactory())
    logging.basicConfig(level=logging.INFO, filename="logs_twisted.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    reactor.run()
