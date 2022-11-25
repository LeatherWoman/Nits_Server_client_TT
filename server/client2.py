import asyncio
import datetime
import pickle
import socket
import pr_pb2 as pr

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8888  # The port used by the server
message = pr.WrapperMessage()
#message.request_for_slow_response.time_in_seconds_to_sleep = 3
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(message))
    data = s.recv(1024)

print('Received {!r}'.format(pickle.loads(data)))


