import cv2
import numpy as np
import socket
import pickle
import threading
import uuid

N = 5
bigimg = np.zeros((500, 500*N, 3), dtype="uint8")

e = threading.Event()
l = threading.Lock()

DEBUG = True

def worker(conn, addr, n):
    print(n)
    
    while True:
        bufsize = int.from_bytes(conn.recv(4), 'big')
        xxyy = [int.from_bytes(conn.recv(4), 'big') for i in range(4)]
        data = b""
        while len(data) != bufsize:
            data += conn.recv(min(4096, bufsize - len(data)))

        frame = pickle.loads(data)

        if -1 not in xxyy or debug:
            frame = cv2.rectangle(frame, (0, 0), (499, 499), (255, 255, 0), 5)
        # cv2.imshow(str(n), frame)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     return

        # aquire mutex or just continue (timeout: 0.01s)
        if l.acquire(True, 0.01):
            # write video
            bigimg[:, 500*n:500*(n+1), :] = frame[:, :, :]
            # release mutex
            l.release()

        if e.is_set():
            conn.close()
            return

def display():
    while True:
        # acquire mutex and wait indefinitely
        l.acquire(True)
        cv2.imshow("af", bigimg)
        l.release()
        cv2.waitKey(10)
        
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
    t = threading.Thread(target=worker, args=(conn, addr, len(threads)))
    t.start()
    threads.append(t)

e.set()
s.close()
cv2.destoryAllWindows()
