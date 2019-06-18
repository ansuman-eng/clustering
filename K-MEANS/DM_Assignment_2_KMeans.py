#!/usr/bin/env python
# coding: utf-8

# In[1]:


gap=2
match=0
replace=1
'''
Using the same penalties as in the reference
'''


# In[2]:


#The function to caluculate distance between sequences. 
#Distance = Global Alignment
#We use DP to make it more efficient.
def distance(seq1,seq2):
    DP=[]
    for i in range(len(seq1)+1):
        temp=[]
        for j in range(len(seq2)+1):
            temp.append(0)
        DP.append(temp)
    
    for i in range(1,len(seq1)+1):
        DP[i][0] = DP[i-1][0] + gap
    for j in range(1,len(seq2)+1):
        DP[0][j] = DP[0][j-1] + gap
    
    for i in range(1,len(seq1)+1):
        for j in range(1,len(seq2)+1):
            if(seq1[i-1]==seq2[j-1]):
                scorediag = DP[i-1][j-1]
            else:
                scorediag = DP[i-1][j-1] + 1
            
            scoreleft = DP[i][j-1] + 2
            scoreup = DP[i-1][j] + 2
            
            DP[i][j] = min(min(scoreleft,scoreup),scorediag)
    
    return DP[len(seq1)][len(seq2)]


# In[21]:


#Code for preprocessing the data
#The code is commented out here
'''
seq=[]
with open('dataset.txt') as f:
    for line in f:
        #print(line)
        seq.append(line)
print(len(seq))
'''


# In[22]:


'''
dist={}

from time import time
t1 = time()
for i in range(len(seq)):
    for j in range(len(seq)):
        print(i,j)
        if(j==i):
            dist[(i,j)]=0
        else:
            dist[(i,j)]=distance(seq[i],seq[j])
for key in dist.keys():
    print(key,dist[key])
print(time()-t1)
'''


# In[23]:


#Load the preprocessed dataset
with open('dataset.pkl','rb') as f:
    dist = pickle.load(f)


# In[24]:


#Debugging
'''
for key in dist.keys():
    print(key,dist[key])
'''


# In[27]:


import random
import math
import matplotlib.pyplot as plt
#The KMEANS ALGORITHM 
candidate = [i for i in range(len(seq))]
K_LIST=[k for k in range(1,201)] # Possible K values,to compare for different number of clusters
print(K_LIST)
WSS_LIST=[]
for K in K_LIST:
    candidate = [i for i in range(len(seq))] 
    centroid_points=[]
    print(K)
    # Generate random cluster centers
    for k in range(K):
        idx = random.randint(0,len(candidate)-1)
        centroid_points.append(candidate[idx])
        candidate.remove(candidate[idx])
    
    print("INITIAL CENTROIDS :",centroid_points)
    
    while(True):
        old_centroid_points = []
        #This will hold the older points, to check for convergence
        for k in centroid_points:
            old_centroid_points.append(k)
        ############################################
        clusters={}
        for k in centroid_points:
            clusters[k]=[k]
        #The above initializes clusters
        
        #Check which cluster center the point is closest to, and put it there
        for p in range(len(seq)):
            if(p in centroid_points):
                continue
            min_dist = math.inf
            min_clust = -1
            for k in centroid_points:
                if(dist[(p,k)]<min_dist):
                    min_dist = dist[(p,k)]
                    min_clust=k
            clusters[min_clust].append(p)
        
        #print("INTERMEDIATE CLUSTERS", clusters)
        ############################################
 
        #Find new cluster center using K-MEDIODS algorithm
        new_centroid_points=[]
        for key,val in clusters.items():
            score_incluster=[]
            for i in val:
                score=0
                for j in val:
                    score+=(dist[(i,j)])
                score_incluster.append([score,i])

            score_incluster.sort()
            new_centroid_points.append(min(score_incluster)[1])
        ############################################
        
        #Check if cluster points don't change
        centroid_points = new_centroid_points
        count=0
        for i in range(len(old_centroid_points)):
            if(old_centroid_points[i]==new_centroid_points[i]):
                count+=1
            else:
                break

        if(count==len(old_centroid_points)):
            break

    print("FINAL CENTROIDS :",centroid_points)
    WSS=0
    for key,val in clusters.items():
        WSS_Cluster=0
        for i in val:
            #print(i,key)
            WSS_Cluster+=(dist[(i,key)])
        WSS+=WSS_Cluster
    #print(WSS)
    WSS_LIST.append(WSS)
    #print("FINAL CLUSTERS :", clusters)


# In[28]:


plt.plot(K_LIST, WSS_LIST)
plt.show()

