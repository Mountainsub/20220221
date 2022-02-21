import subprocess

import pandas as pd
import numpy as np
import time 
import sys
import os
import random
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from request5.rakuten_rss import rss , rss2 
from lib.ddeclient import DDEClient
#並列処理






#dde_ware = []



def calculation(dde_ware, indexes_weight, num):
    calc = rss2("現在値", dde_ware, indexes_weight)

    return calc if calc - num < 10 else calc # 差が大きい時は元の値を取得

if __name__ == '__main__':
    args = sys.argv # コマンドライン引数として開始地点のインデックスを数字で入力する

    count = 0
    if True:
        array =  rss("現在値",int(args[1]))
        dde_ware, weight = array[1], array[2]
            # ware.append(dde_ware)
        with open("OK.txt", "w")as f:
            f.write("OK"+ args[1]+ " ")

        t1 = time.time()
        calc = array[0]
        while True:
            
            count += 1
            try:
                ex = calculation(dde_ware, weight,  calc)
            except Exception:
                ex = Exception
                while ex == Exception:
                    ex = calculation(dde_ware, weight, calc)
            print(ex)
            t2 = time.time()
            with open("time.txt", "a") as f:
                f.write(str(t2-t1) + "\n")
            if t2 - t1 > 1:
                number = random.uniform(3.0, 5.0)
                number *= 100
                number = math.floor(number) /100
                time.sleep(number)
                t1 = time.time()
                calc = ex
                continue


        