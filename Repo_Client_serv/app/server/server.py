from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.task import deferLater
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import Deferred
import pr_pb2 as pr
import pickle
import datetime

class Server(Protocol):
    def __init__(self,users):
        self.users = users
    
       
    def connectionMade(self):
        print('connection success!')
        self.users.append(self)
    
    def sleep(self,secs):
        d = Deferred()
        reactor.callLater(secs, d.callback, None)
        return d
    #Событие dataReceived - получение и отправление данных
    def dataReceived(self, data):
        for user in self.users:
            message = pickle.loads(data)
            if type(message)==pr.WrapperMessage:
                pass
            else:
                out = pickle.dumps(ValueError)
            #transport.write - отправка сообщения
                self.transport.write(out)
            if message.request_for_slow_response.time_in_seconds_to_sleep!=0:
                #print(len(message.request_for_slow_response.time_in_seconds_to_sleep))
                sec = int(message.request_for_slow_response.time_in_seconds_to_sleep)
                self.sleep(sec*5000)
                out_put = pr.WrapperMessage()
                out_put.slow_response.connected_client_count = len(self.users)
                out = pickle.dumps(out_put)
                self.transport.write(out)
                print("IN IF")
            else:
                out_put = pr.WrapperMessage()
                out_put.fast_response.current_date_time = str(datetime.datetime.now())
                out = pickle.dumps(out_put)
                self.transport.write(out)
            self.transport.loseConnection()
    
    #Событие connectionLost срабатывает при разрыве соединения с клиентом
    def connectionLost(self, reason):
        self.users.remove(self)
        print('Connection lost!')
        
class ServerFactory(ServFactory):
    def __init__(self):
        self.users = []
        
    
    def buildProtocol(self, addr):
        return Server(self.users)
        #return super().buildProtocol(addr)
        
        
if __name__ =='__main__':
    endpoint = TCP4ServerEndpoint(reactor, 5009)
    endpoint.listen(ServerFactory())
    reactor.run()