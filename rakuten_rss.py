"""楽天RSS用モジュール
"""
from lib.ddeclient import DDEClient
import pandas as pd
import numpy as np
import time 


def ind():
	indexes = pd.read_csv("TOPIX_weight_jp.csv")

	indexes["コード"] = pd.to_numeric(indexes["コード"], errors='coerce')


	indexes_code = indexes["コード"].astype(int)
	
	for i,j in enumerate(indexes_code):
		indexes_code[i] = str(j) + ".T"
	indexes_code = np.array(indexes_code)
	indexes_code = indexes_code.flatten()

	for i,j in indexes.iterrows():
		# % を除去
		indexes.at[i, "TOPIXに占める個別銘柄のウェイト"] = indexes.loc[i, "TOPIXに占める個別銘柄のウェイト"].replace("%", "")
	return [indexes_code, indexes]


def rss(item, k):
	dde_ware = []

	count = 0
	calc = 0
	
	# 以下csvファイルを都合いいようにエディット

	inde = ind()
	indexes_code, indexes = inde[0], inde[1] 
	
	# ddeを取得、格納、ウエイトをかけて計算

	for i,j in enumerate(indexes_code, start = k): 
		count += 1
		
		if k==2142 and count == 24:
			True
		#print(count)
		try:
			dde = DDEClient("rss", indexes_code[i])
		except Exception:
			continue
		dde_ware.append(dde)
		
		if True:	
			try:
				val = dde.request(item).decode("sjis")
			except Exception:
				try:
					val = dde.request("始値").decode("sjis")
				except Exception:
					val = 0
					pass
				else:
					name = dde.request("銘柄名称").decode("sjis")
					with open("check4.txt", "a", newline= "\n") as f:
						f.write(name+"\n")
					pass
			finally:
				calc += float(val) * float(indexes["TOPIXに占める個別銘柄のウェイト"][i] )* 0.01
				with open("check3.txt", "a", newline= "\n") as f:
					tup = (val,indexes["TOPIXに占める個別銘柄のウェイト"][i] )
					f.write(str(tup)+"\n")
				del dde
				if count >= 126:
					break
				if k == 2142:
					if count == 44:
						continue 

	pocket = [calc, dde_ware, indexes["TOPIXに占める個別銘柄のウェイト"], k+count]
	
	
	return pocket
	

def rss2(item, dde_ware, weights):
	
	"""
	すでに使ったddeのデータで再度指数を計算
	"""
	
	calc = 0
	count = 0
	check_num = 0
	for i,j in enumerate(dde_ware):
		dde = dde_ware[i]
		double_check = False
		while True:	
			try:
				calc += float(dde.request(item).decode("sjis")) * float(weights[i] )* 0.01
				
			except Exception:
				if double_check:
					with open("check2.txt", "a") as f :
						try:
							f.write(dde.request("銘柄コード").decode("sjis"))
						except:
							f.write(str(i))

					break
				else:
					double_check = True
				pass
			else:
				break
		count += 1
		if count >= 126:
			break	
		else:
			continue
	return calc


def rss_dict(code, *args):
	"""
	楽天RSSから辞書形式で情報を取り出す(複数の詳細情報問い合わせ可）
	Parameters
	----------
	code : str
	args : *str
	Returns
	-------
	dict
	Examples
	----------
	>>>rss_dict('9502.T', '始値','銘柄名称','現在値')
	{'始値': '1739.50', '現在値': '1661.50', '銘柄名称': '中部電力'}
	"""

	dde = DDEClient("rss", str(code))

	
	values ={}
	element = []

	res = {}
	try:
		for item in args:
			res[item] = dde.request(item).decode('sjis').strip()
	except:
		print('fail: code@', code)
		res = {}
	finally:
		dde.__del__()
	return res

def fetch_open(code):
	""" 始値を返す（SQ計算用に関数切り出し,入力int）
	Parameters
	----------
	code : int
	Examples
	---------
	>>> fetch_open(9551)
	50050
	"""

	return float(rss(str(code) + '.T', '始値'))
