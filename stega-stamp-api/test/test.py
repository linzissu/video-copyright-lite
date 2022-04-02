import os
from mapper.Stega import Stegastamp
from config import *

stega = Stegastamp()
sess, model = stega.load_model(MODEL_PATH)

def encode():
    res = stega.encode('I am Delin Qu, comes from HNU , a beautiful campus with lots of flows and student......', './video/test.mp4', sess, model)

def decode():
    res = stega.decode('./video/test.mp4', sess, model)

if __name__ == '__main__':
    encode()
    decode()