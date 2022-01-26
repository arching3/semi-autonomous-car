import cv2 as cv
import socket
from concurrent.futures import ThreadPoolExecutor
import numpy
from time import sleep


sock = socket.socket()
sock.bind(('',8888))
sock.listen(0)
