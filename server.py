import cv2
import numpy as np
import socket
import pickle

s = socket.socket()
s.bind(("", 12080))

s.listen(5)

conn, addr = s.accept()

while True:
    bufsize = int.from_bytes(conn .recv(4), 'big')
    data = b""
    while len(data) != bufsize:
        data += conn.recv(min(4096, bufsize - len(data)))

    frame = pickle.loads(data)
    cv2.imshow("asdf", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
