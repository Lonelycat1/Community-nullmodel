# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 10:01:56 2018

@author: lenovo
"""
#
#########################基于零模型的社区检测基准网络构造及应用#######################

import copy
import math 
import random   
import pandas as pd
import numpy as np                   
import igraph as ig
import networkx as nx                 
import matplotlib.pyplot as plt
from igraph import*
from communitynullmodel_new import *
from numpy import random as nr      
'''
###################################################
#函数名称：degree_hist
#功能：网络所有节点的度分布的直方列表
#输入参数：G
#输出参数：degree_histogram（度分布列表）
###################################################
'''
def degree_hist(G):#节点度分布
    degree_histogram=nx.degree_histogram(G)
    return degree_histogram    

'''
###################################################
#函数名称：Edges
#功能：取得列表中所有元素的索引值
#输入参数：
#        参数1:communitydivision_list(社区划分列表)
#        参数2:edges_dic(连边字典)
#输出参数：edgesinside(内部连边列表)
###################################################
'''   
def Edges(communitydivision_list,edges_dic):
    #初始化定义初值为0
    edgesinside = 0                 
    edgesoutside = 0
    
    #通过循环得到所有节点的社团内部连边
    for node in communitydivision_list:               
        try:
            for edges in edges_dic[node]:
                #判断边是否在社团内部
                if edges in communitydivision_list:     
                    edgesinside += 1
                else:
                    edgesoutside += 1                   
        except:
            pass
    return edgesinside/2.0,edgesoutside     #返回内部连边数和外部连边
'''
###################################################
#函数名称：MU
#功能：计算网络模糊程度的系数mu
#输入参数：
#        参数1:community_list(社区列表)
#        参数2:edges_dic(连边字典)
#输出参数：mu(模糊系数)
###################################################
'''   
def MU(community_list,edges_dic):
    edges_inside=[]
    edges_outside=[]
    
    #通过循环将所有小社团所得结果放在空列表里
    for i in range(len(community_list)):
        #n，m分别为社区内部节点数和边数
        edgesinside,edgesoutside = Edges(community_list[i],edges_dic)
        edges_inside.append(edgesinside)    #获取网络中所有社区内部的连边数
        edges_outside.append(edgesoutside)  #获取网络中所有社区外部连边数
    #all_edgesinside=sum(edges_inside)
    all_edgesoutside=sum(edges_outside)   
    mu=all_edgesoutside*1.0/M
    
    return mu
'''
###################################################
#函数名称：network_community
#功能：将社区划分列表转变成membership，即为原始社区划分
#输入参数：
#        参数1:community_list(社区列表)
#        参数2:G(社区所处的网络)
#输出参数：membership(社区信息归属表)
###################################################
''' 
def network_community(community_list,G):    
    #将节点标号从1开始转化为从0开始
    community_list_new = []
    for i in range(len(community_list)):
        temp = []
        nodes = community_list[i]
        for j in nodes:
            node = int(j-1)
            temp.append(node)
        community_list_new.append(temp)
        
    ##将社区划分列表转变成membership
    membership = []
    for k in range(0,len(G)):
       membership.append(0)
       
    # 根据社团划分对membership赋值
    for l in range(0,len(community_list_new)):
        nodes = community_list_new[l]
        for m in nodes:
            membership[m] = l
    for s in range(len(membership)):
        membership[s] = membership[s]+1
        
    return membership
'''
###################################################
#函数名称：load_Graph
#功能：根据文件生成无向网络
#输入参数：filename(网络数据文件名称)
#输出参数：G(生成好的网络)
###################################################
'''
def load_Graph(filename):
    #读入网络数据
    network = open(filename)            #
    network = network.read()
    #生成无向图
    G = nx.Graph()    
    line = network.split('\n')          #用回车符分裂字符串,得到每一行的数据   
    for i in range(0,len(line)-1):
        pair_node = line[i].split()     #用空格分裂得到节点对    
        node_1 = int(pair_node[0])      #得到第一个节点
        node_2 = int(pair_node[1])      #得到第二个节点
        G.add_edge(node_1,node_2)       #添加边至空网络
    
    return G

'''
###################################################
#函数名称：save_community_file
#功能：保存网络相关的社区信息文件(以空格分隔)
#输入参数：
#        参数1：membership(社区归属信息表)
#        参数2：filename(待生成文件的名称)
#        参数3：filelayout(待生成文件的储存格式)
#输出参数：无
###################################################
'''   
def save_community_file(membership,filename,filelayout):
    
    membership_save = [i+1 for i in range(len(membership))]
    data = pd.DataFrame(membership,index=membership_save)
    save_community_name = filename
    save_file_layout = filelayout
    data.to_csv(save_community_name + save_file_layout,header=None,sep=' ')

'''
###################################################
#函数名称：evaluate_network
#功能：网络微观特性测评，计算并打印网络相关特性
#输入参数：
#        参数1：network_filename(待测评的网络文件)
#        参数2：community_filename(待测评的社区文件)
#输出参数：无
###################################################
''' 
def evaluate_network(network_filename,community_filename):
 
    #加载变化后的网络
    G = nx.Graph()
    G = load_Graph(network_filename)
    n = G.number_of_nodes()
    M = G.number_of_edges()
    #计算相关信息
    K = 2*M*1.0/n                                       #计算平均度
    avg_length = nx.average_shortest_path_length(G)     #计算平均路径长度
    betweeness=nx.betweenness_centrality(G)             #计算betweeness介数
    nx.degree_histogram(G)                              #度分布
    S = nx.clustering(G)                                #聚类系数
    c = nx.average_clustering(G)                        #平均聚类系数
    dac = nx.degree_assortativity_coefficient(G)        #计算匹配系数
    #计算社区数
    filename = community_filename
    file = open(filename,'r')
    content = file.readlines()
    mem = []
    for i in range(len(content)):
        a,b=content[i].split(' ')
        mem.append((int(b)))
    comm0 = mem
    num_comm = len(set(mem))  #计算社区的数目
    #打印信息提示
    print('节点数为',n)
    print('边数为',M)     
    print('平均度为',K)
    print('平均路径长度为',avg_length)
    print('介数为',betweeness)
    print('聚类系数为',S)
    print('平均聚类系数为',c)
    print('匹配系数为',dac)
    print('社区数为',num_comm)

# 读入网络数据        
Gn = nx.read_edgelist('karate.txt')  
Gn = Gn.to_undirected()             #将网络转化为无向
#根据网络边列表生成图
G = nx.Graph()
G = load_Graph('karate.txt')

edges_dic = nx.to_dict_of_lists(G)
M = G.number_of_edges()             #网络中总边数
N = G.number_of_nodes()             #网络中总节点数
origin_edges = nx.to_edgelist(G)

new_list = []
for edge_i in range(0,len(origin_edges)):
    node_dict = list(origin_edges)[edge_i]
    new_list.append([node_dict[0],node_dict[1]])

#用变向量列表创建图形           
g = Graph(new_list)  

#h = g.community_fastgreedy(weights=None)   #fastgreedy算法社团检测
#community_list = list(h.as_clustering())   #按照默认Q值最大的原则，对系统树图进行切割
h = g.community_infomap()
community_list = list(h)
membership = network_community(community_list,G)
Q = GraphBase.modularity(g, membership)    #计算原始网络Q值

#保存原始网络的社团信息
save_community_file(membership,'origin_community','.txt')

#将networkx中的节点编号转换成字符才能和igraph里面的节点对应上
community_list_s  = community_list     
for i in range(0,len(community_list)):                 
    community_list_s[i]=list(map(str, community_list[i]))
origin_mu =  MU(community_list,origin_edges)        #原始网络模糊系数
    
##改变原始网络结构
steps = 1
nswap  = 2*M  #交换次数2l,l=M    
maxtry = 10*nswap

while steps < 100:    
    #调用的零模型改变原始网络结构
    GAS = inter_random_1k(Gn,community_list_s,nswap=nswap, max_tries=maxtry)  
    nx.write_edgelist(GAS,'changed_network'+'.txt',data=False)
    
    #根据网络连边列表生成图
    G1 = nx.Graph()
    G1 = load_Graph('changed_network.txt')
    
    edges_dic_new = nx.to_dict_of_lists(G1)
    origin_edges_new = nx.to_edgelist(G1)
    
    #将节点编号转化为str类型与Graph对应
    list_new = []
    for edge_i in range(0,len(origin_edges_new)):
        node_dict = list(origin_edges_new)[edge_i]
        list_new.append([node_dict[0],node_dict[1]])          
    
    g1 = Graph(list_new)
    h1 = g.community_infomap()
    community_list_new = list(h1)
    list(community_list_new).remove(community_list_new[0])        #去除里面0标号的节点
    #计算改变后网络的Q值
    membership1 = network_community(community_list_new,G1)
    Q1 = GraphBase.modularity(g1, membership1)
    
    #保存改变后网络后的社团信息
    save_community_file(membership1,'changed_community','.txt')
    #计算改变后网络的模糊系数
    mu = MU(community_list_new,edges_dic_new)
    
    print('steps is',steps)
    if mu == 0.02:
        if abs(Q1-Q) <= 0.001:       
           print("GAS is right")
           break
    else:
        print("mu =",mu)
    steps += 1

#网络微观特性测试 
evaluate_network('changed_network.txt','changed_community.txt')
evaluate_network('karate.txt','origin_community.txt')  





