import numpy as np
import math
import time
import copy
from itertools import combinations
from sortedcontainers import SortedSet
import matplotlib.pyplot as plt

def distance(a):
	dist = np.zeros((a, a))
	for i in range(len(dist[0])):
		for j in range(len(dist[1])):
			if i < j:
				continue
			else:
				if i == j:
					continue
				else:
					dist[i, j] = np.random.randint(30)
					dist[j, i] = dist[i, j]

	index = []
	index0 = []
	for k in range(0, a):
		index.append(k)
		if k != 0:
			index0.append(k)
	return dist, index, index0


def DP(index):#傳入幾個頂點
	D = {}
	for z in range(1, len(index)+1):#從vk走到v0的距離
		key = str(z)+"SortedSet([])"
		D[key] = dist[z, 0]
		# print(key)
	for k in range(1, len(index)):
		for l in combinations(index, k):#
			for m in range(len(index)+1):
				if m != 0 and m not in l:#子集合不會有0
					l = SortedSet(l)
					arr_min = []
					for n in l: 
						l1 = l.copy()
						l1.remove(n)
						key = str(n)+str(l1)
						arr_min.append(dist[m][n]+D[key])
					key = str(m)+str(l)
					D[key] = (min(arr_min))
	DP_min = []
	for j in range(1, len(index)+1):
		index1 = index.copy()
		index1 = SortedSet(index1)
		index1.remove(j)
		key = str(j)+str(index1)
		DP_min.append(dist[0][j] + D[key])
	return min(DP_min)

t_cost = 0
# visited = np.zeros(len(n))
def Greedy(index, s):
	index.remove(s)
	# visited[s] = 1
	if len(index) == 1:
		return dist[s][index[-1]]
	else:
		dis_arr = dist[s][:]
		# print(dis_arr)
		while True:
			i = np.argmin(dis_arr)
			if i in index:
				return Greedy(index, i) + dist[s][i]
			else:
				dis_arr[i] = 31

if __name__ =="__main__":
	arr_error = []
	arr_time1 = []
	arr_time2 = []
	indicies = []
	for a in range(4, 21):
		indicies.append(a)
		error = 0
		time1 = 0
		time2 = 0
		for b in range(5):
			dist, index, index0 = distance(a)
			start1 = time.perf_counter()
			# print("start1", start1)
			DP_dist = DP(index0)
			# print("%d 個頂點DP距離："%a, DP_dist)
			end1 = time. perf_counter()
			# print("end1", end1)
			DP_time = end1-start1
			# print("%d 個頂點DP的运行时间是：%s"%(a, DP_time))
			start2 = time.perf_counter()
			# print("start2", start2)
			G_dist = Greedy(index, 0)
			# print("%d 個頂點Greedy距離："%a, G_dist)
			end2 = time. perf_counter()
			# print("end2", end2)
			G_time = end2-start2
			# print("%d 個頂點Greedy的运行时间是：%s"%(a, G_time))
			print(G_dist)
			error += (G_dist - DP_dist) / DP_dist
			time1 += DP_time
			time2 += G_time
		mean_e = error/5
		arr_error.append(mean_e)
		mean_time1 = time1/5
		arr_time1.append(mean_time1)
		mean_time2 = time2/5
		arr_time2.append(mean_time2)
		print("%d個點的平均error:"%a, mean_e)
		print("%d個點的平均DP時間:"%a, mean_time1)
		print("%d個點的平均Greedy時間:"%a, mean_time2)	

	# print("")
	# print(arr_error)
	# print(arr_time1)
	# print(arr_time2)
	# print(indicies)
	plt.figure()
	plt.plot(indicies, arr_error)
	plt.scatter(indicies, arr_error)
	plt.title("Mean Error")
	plt.xlabel("index")
	plt.ylabel("error")
	plt.xticks(np.linspace(indicies[0],indicies[-1],len(indicies)))
	plt.figure()
	plt.plot(indicies, arr_time1, color = "blue", label = "DP")
	plt.plot(indicies, arr_time2, color = "orange", label = "Greedy")
	plt.legend()
	plt.title("Time")
	plt.show()

