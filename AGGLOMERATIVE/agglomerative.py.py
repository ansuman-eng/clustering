#!/usr/bin/env python
# coding: utf-8

# In[42]:


import pickle
with open('dataset.pkl','rb') as f:
    dist = pickle.load(f)


# In[43]:


for key in dist.keys():
    print(key,dist[key])


# In[106]:


metric = input("Please enter 'min', 'max' or 'av'")


# In[107]:


import math


# In[108]:


clusters = []
for i in range(311):
    clusters.append([i])
print(clusters)


# In[109]:


def dist_cluster(cluster1, cluster2, metric):
    min_dist = math.inf
    max_dist = -math.inf
    av_dist = 0
    count=0
    for i in cluster1:
        for j in cluster2:
            count+=1
            if(dist[(i,j)] > max_dist):
                max_dist = dist[(i,j)]
            if(dist[(i,j)] < min_dist):
                min_dist = dist[(i,j)]
            av_dist+=dist[(i,j)]
    if(metric=='min'):
        return min_dist
    elif(metric=='max'):
        return max_dist
    elif(metric=='av'):
        return av_dist
    


# In[110]:


def WSS(cluster):
    minss = 10e9
    #print(cluster)
    for point in cluster:
        squaredsum = 0
        for ppoint in cluster:
            #print(point,ppoint)
            squaredsum += dist[(point,ppoint)]
        if squaredsum < minss:
            minss = squaredsum
    return minss


# In[111]:


count_iter=0
WSS_list = []
clust_list = []

while(len(clusters)>1):
    #print(len(clusters))
    clust_list.append(len(clusters))
    #print(len(clust_list))
    WSS_temp=0
    for cluster in clusters:
        WSS_temp+=WSS(cluster)
    WSS_list.append(WSS_temp)
    '''
    print(clusters)
    print(WSS(clusters))
    print("###################")
    '''
    
    #NUMBER OF CLUSTERS WILL REDUCE BY 1 ON EACH ITERATION

    min_dist = math.inf
    clust1_idx = 0
    clust2_idx = 0
    
    #FIND THE TWO CLUSTERS WHICH ARE CLOSEST
    for i in range(len(clusters)):
        for j in range(i+1,len(clusters)):
            cache = dist_cluster(clusters[i], clusters[j], metric)
            if(cache < min_dist):
                min_dist = cache
                clust1_idx = i
                clust2_idx = j
    
    clust1 = clusters.pop(clust1_idx)
    clust2 = clusters.pop(clust2_idx -1)
    
    clust1 = clust1+clust2
    clusters.append(clust1)
    
   



# In[112]:


clust_list.append(len(clusters))
WSS_list.append(WSS(clusters[0]))


# In[113]:


print(len(clust_list))
print(len(WSS_list))


# In[114]:


import matplotlib.pyplot as plt
plt.plot(clust_list, WSS_list)
plt.show()


# In[ ]:




