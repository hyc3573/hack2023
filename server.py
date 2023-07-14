import cv2
import numpy as np
import socket
import pickle
import threading
import uuid

e = threading.Event()
l = threading.Lock()

imgs = []

def worker(conn, addr, n):
    print(n)
    
    while True:
        bufsize = int.from_bytes(conn.recv(4), 'big')
        xxyy = [int.from_bytes(conn.recv(4), 'big') for i in range(4)]
        data = b""
        while len(data) != bufsize:
            data += conn.recv(min(4096, bufsize - len(data)))

        frame = pickle.loads(data)
        print(xxyy)
        # cv2.imshow(str(n), frame)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     return

        # aquire mutex or just continue (timeout: 0.01s)
        l.aquire(True, 0.01)
        # write video
        imgs[n] = frame[:, :, :]
        # release mutex
        l.release()

        if e.is_set():
            conn.close()
            return

def display():
    while True:
        # acquire mutex and wait indefinitely
        l.acquire(True)
        # draw image
        tup = tuple(filter(lambda x: x is not None, imgs))
        if tup:
            img = np.hstack()
            cv2.imshow("asdf", img)
        # release mutex
        l.release()
        
        if e.is_set():
            return

s = socket.socket()
s.bind(("", 12080))

s.listen(5)

t = threading.Thread(target=display)
t.start()

threads = []
while True:
    conn, addr = s.accept()
    imgs.append(None)
    t = threading.Thread(target=worker, args=(conn, addr, len(threads)))
    t.start()
    threads.append(t)

e.set()
s.close()
cv2.destoryAllWindows()
