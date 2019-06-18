import time
import pickle
import math


def averagedistance(point,points):
# this function calculates the average distance of 'point' from the set 'points'
	if len(points) == 1 and point == points[0]:
		return 0
	avgdist = 0
	count = 0

	for i in points:

		if not(i == point):
			avgdist += Distance[(i,point)]
			count += 1

	avgdist = avgdist/count
	return avgdist

def findsplinter(P):
#this function finds the first member of the splinter cluster
	farthest = 0
	splinter = P[0]

	for i in P:

		d = averagedistance(i,P)
		if d > farthest:
			farthest = d
			splinter = i

	return splinter

def wss(cluster):
	minss = 10e9
	for point in cluster:
		squaredsum = 0
		for ppoint in cluster:
			squaredsum += Distance[(point,ppoint)]
		if squaredsum < minss:
			minss = squaredsum
	return minss


def divisive(P,level,clusters):
#this function recursively computes clusters
	if level == 0:
		return
	clusters.remove(P)
	splinter = findsplinter(P)
	splintercluster = [splinter]
	maincluster = P.copy()
	maincluster.remove(splinter)

	for point in maincluster:
	#putting points	in their respective clusters
		if averagedistance(point,maincluster) > averagedistance(point,splintercluster):
			splintercluster += [point]
			maincluster.remove(point)
		else:
			pass

	clusters += [maincluster,splintercluster]
	# clusterlevel[level] += [(maincluster,splintercluster)]
	# print (maincluster)
	# print (splintercluster)
	# print ('~~~~~~~~~~~~~~~~~~~')

	max1 = 0
	maxcluster = []
	for i in clusters:
		err = wss(i)
		# print(err)
		if err > max1:
			max1 = err
			maxcluster = i
			# print(err)

	if len(maxcluster) > 1:
		divisive(maxcluster,level-1,clusters)
	# fl = 0
	# if len(maincluster) > 1  and wss(maincluster) >= wss(splintercluster):
	# 	divisive(maincluster,level-1,clusters)

	# elif len(splintercluster) > 1:
	# 	divisive(splintercluster,level-1,clusters)

	#if both clusters can't be further broken: terminate
	# global bosslevel
	# if level > bosslevel:
	# 	bosslevel = level



#dummy values ignore
Distance=[[0, 2, 3, 1, 4],
		  [2, 0, 5, 3, 6],
		  [3, 5, 0, 7, 8],
		  [1, 3, 7, 0, 1],
		  [4, 6, 8, 1, 0]]

#loading the distance matrix
with open ('dataset.pkl','rb') as f:
	Distance=pickle.load(f)

PointSet = list(range(310))
clusterlevel={}
# clusters = [PointSet]
bosslevel = 1

#initializing 
for i in range(310):
	clusterlevel[i]=[]

for i in [1,2,4,8,16,32,64,128,256]:
	clusters = [PointSet]
	divisive(PointSet,i,clusters)
	print(clusters)
	error = 0
	p=0
	for j in clusters:
		# print(j)
		error += wss(j)
		p += 1
		if p == i:
			break
	print (error)
print('=====================================')

# print('Error sum of squared: ',end='')
# k = int(input())

error = 0

# for k in [2,4,8,16,32,64,128,256,512]:
# 	levell = int(math.log(k)/math.log(2))
# 	error = 0
# 	for j in clusterlevel[levell]:
# 		error += wss(j[0])
# 		error += wss(j[1])
# 	print (error)

# print (clusterlevel[1])

# print (clusters)
# for k in [1]:#,2,4,8,16,32,64,128,256]:
# 	error = 0
# 	p=0
# 	for j in clusters:
# 		print(j)
# 		error += wss(j)
# 		p += 1
# 		if p == k:
# 			break
# 	print (error)



# def loop():
# 	for i in clusterlevel.keys():
# 		for j in clusterlevel[i]:
# 			global error
# 			global k
# 			if k == 1:
# 				error += wss(j[0])
# 			k -= 1
# 			if k == 0:
# 				return
# 			if k == 1:
# 				error += wss(j[1])
# 			if k == 0:
# 				return
# loop()


# for j in clusterlevel[levell]:
# 	error += wss(j[0])
# 	error += wss(j[1])

# print(error) 
# print('Boss is at level ',end='')
# print(bosslevel)
# print('=====================================')
# print('\n~~~~Ready Player One~~~~\nEnter Level: ',end='')
# lev = int(input())

# if lev > bosslevel:
# 	print('\nGAME OVER\n')
# else:
# 	print('\nClusters at level ',end='')
# 	print(lev)
# 	print (clusterlevel[lev],end='\n\n')
# 	print('\"Alexa, roll credits\"')

