from unittest import TestCase, main
from client import EchoClientProtocol
from client import main as MAIN
from client import Nado
import asyncio
import pr_pb2 as pr

#def Proto():
    


class EchoClientProtocolTest(TestCase):
    '''Тесты для получения данных с сервера'''
    
    def test_decode_FastResponse(self):
        ip = '127.0.0.1'
        host = 5003
        message = pr.WrapperMessage()
        message.request_for_fast_response.CopyFrom(pr.RequestForFastResponse())
        test = MAIN(message,ip,host)
        asyncio.run(test)
        test_decode_1 = Nado().data_decode
        print('Test decode is ', test_decode_1)
        self.assertEqual(type(test_decode_1),pr.WrapperMessage)
        
    def test_decode_SlowResponse(self):
        ip = '127.0.0.1'
        host = 5003
        message = pr.WrapperMessage()
        message.request_for_slow_response.time_in_seconds_to_sleep = 2
        test = MAIN(message,ip,host)
        asyncio.run(test)
        test_decode_2 = Nado().data_decode
        print('Test decode is ', test_decode_2)
        self.assertEqual(type(test_decode_2),pr.WrapperMessage)
        
        
    def test_decode_NotWrapperMessage(self):
        ip = '127.0.0.1'
        host = 5003
        message = 123
        test = MAIN(message,ip,host)
        asyncio.run(test)
        test_decode_3 = Nado().data_decode
        print('Test decode is ', test_decode_3)
        self.assertEqual(test_decode_3,ValueError)
        

        
if __name__ == '__main__':
    main()