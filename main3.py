import subprocess
import asyncio
import multiprocessing
import threading
import pandas as pd
import numpy as np
import time 
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from request5.rakuten_rss import rss , rss2 
from lib.ddeclient import DDEClient


if __name__ == "__main__":
    s = 0
    count = 0
    temp=0
    while count <= 17: 
        count += 1
        try:
            with open('file_'+ str(count) + '.txt', 'r') as f:
                a = f.readline()
                a.rstrip("\n")                          
                num = float(a)
                s += num
        except:
            continue
    print(s)