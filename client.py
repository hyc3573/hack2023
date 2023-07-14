import cv2
import numpy as np
import socket
import pickle

cap = cv2.VideoCapture(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.1.155', 12080))

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    data = pickle.dumps(cv2.resize(frame, (500, 500)))
    s.send(len(data).to_bytes(4, 'big')) # byte-length of data
    s.send(len(data).to_bytes(4, 'big')) # x1
    s.send(len(data).to_bytes(4, 'big')) # y1
    s.send(len(data).to_bytes(4, 'big')) # x2
    s.send(len(data).to_bytes(4, 'big')) # y2
    s.sendall(data) # data

s.close()
