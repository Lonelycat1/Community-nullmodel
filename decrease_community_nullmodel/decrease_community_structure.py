# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 18:48:12 2020

@author: LX
"""

######################################基于社区强弱变化零模型的网络构造########################################

from communitynullmodel_new import*
import networkx as nx
import igraph as ig
import pandas as pd
from community_detection_algorithm  import DECD
def load_Graph(filename):
    #读入网络数据
    network = open(filename)            #
    network = network.read()
    
    #生成空的无向图
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
g = ig.Graph(new_list)  
h = g.community_infomap()
community_list = list(h)
membership = network_community(community_list,G)
Q = ig.GraphBase.modularity(g, membership)    #计算原始网络Q值

#将networkx中的节点编号转换成字符才能和igraph里面的节点对应上
community_list_s  = community_list     
for i in range(0,len(community_list)):                 
    community_list_s[i] = list(map(str, community_list[i]))

##改变原始网络结构
steps=1
nswap =2*M  #交换次数2l,l=M    
maxtry = 10*nswap

for i in range(0,10):
    GAS = Q_decrease_1k(Gn,community_list_s,nswap=nswap, max_tries=maxtry)
    nx.write_edgelist(GAS,'changed_network'+str(i)+'.txt',data=False)
    edges_dic = nx.to_dict_of_lists(GAS)
    changed_edges = nx.to_edgelist(GAS)

    new_list_changed = []
    for edge_i in range(0,len(changed_edges)):
        node_dict = list(changed_edges)[edge_i]
        new_list.append([node_dict[0],node_dict[1]])
    
    
    #用变向量列表创建图形           
    g_changed = ig.Graph(new_list_changed)  
    h = g_changed.community_infomap()
    community_list_changed = list(h)
    membership_changed = network_community(community_list_changed,GAS)
    Q_changed = ig.GraphBase.modularity(g, membership_changed)    #计算原始网络Q值
    save_community_file(membership,'changed_community'+str(i),'.txt')
    
    DECD('changed_network'+str(i)+'.txt','changed_community'+str(i)+'.txt')
    
    
    
    
    
    
