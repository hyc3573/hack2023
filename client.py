import cv2
import numpy as np
import socket
import pickle

cap = cv2.VideoCapture(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12080))

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    data = pickle.dumps(frame)
    s.send(len(data).to_bytes(4, 'big'))
    s.sendall(data)
