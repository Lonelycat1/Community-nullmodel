# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:42:23 2017
revised on Oct 15 2017
@author: Aipan1
"""

import networkx as nx
import random
import copy
'''
###################################################
#函数名称：config_model
#功能：配置模型的1阶零模型
#输入参数：G0(原始网路)
#输出参数：G(设置好的网络)
###################################################
'''
def config_model(G0):
    degree_seq = list(G0.degree().values()) 
    G = nx.configuration_model(degree_seq) 
    return G

 '''
###################################################
#函数名称：edge_in_community
#功能: 判断某条边是否为社团内部连边
#输入参数：
#    参数1：node_comunity_list(网络中节点的社团归属信息)
#    参数2：edge(网络中的一条连边)
#输出参数：
#    1：是社团内部连边
#            or
#    0：是社团外部连边
###################################################
''' 
def edge_in_community(node_community_list, edge):        
    return_value = 0
    for community_i in node_community_list:        
        if edge[0] in community_i and edge[1] in community_i: #拿出边的两个节点
            return_value=return_value+1
            return 1
    if return_value==0:
        return 0
    
'''
###################################################
#函数名称：dict_degree_nodes
#功能：将节点的度的列表转化为以节点度为键名，节点为键值的字典
       例：[(1,9),(2,9)] ——> {9:[1,2]}
       
#输入参数：degree_node_list(关于所有节点度的列表)
            例：[(节点1,节点1的度),(节点2,节点2的度),...]
            
#输出参数：D(关于以节点度为关键字的字典)
            例：{度：[节点1，节点2，..]}，其中节点1和节点2有相同的度
###################################################
'''
def dict_degree_nodes(degree_node_list):

    D = {}      
    for degree_node_i in degree_node_list:
        if degree_node_i[0] not in D:
            D[degree_node_i[0]] = [degree_node_i[1]]
        else:
            D[degree_node_i[0]].append(degree_node_i[1])
    return D
 
 '''
###################################################
#函数名称：inner_random_0k
#功能：基于随机断边重连的0阶零模型，
      (保证0阶特性不变的前提下，对社区内部的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''  
def inner_random_0k(G0,node_community_list,nswap=1, max_tries=100,connected=1):  
#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("It is only allowed for undirected networks")
    if nswap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")  
        
    G = copy.deepcopy(G0)      

    n = 0
    swapcount = 0
    edges = list(G.edges())
    nodes = list(G.nodes())
    while swapcount < nswap:
        n=n+1
        u,v = random.choice(edges)      #随机选网络中的一条要断开的边
        x,y = random.sample(nodes,2)    #随机找两个不相连的节点
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团内部连边
            #保证新生成的边还是社团内连边			
                if (x,y) not in edges and (y,x) not in edges:
                    G.remove_edge(u,v)              #断旧边
                    G.add_edge(x,y)                 #连新边
                    edges.remove((u,v))
                    edges.append((x,y))
            
                if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                    if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                        G.remove_edge(x,y)              #断新边
                        G.add_edge(u,v)                 #连旧边
                        edges.remove((x,y))
                        edges.append((u,v))
                        continue 
                    swapcount=swapcount+1             
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +'before desired swaps achieved (%s).'%nswap)
            print(e)
            break
    return G

'''
###################################################
#函数名称：inner_random_1k
#功能：基于随机断边重连的1阶零模型
       (保证1阶特性不变的前提下，对社区内部的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inner_random_1k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团内部连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边还是社团内连边			

                    if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                         
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
    
    
                    if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                        if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                            G.add_edge(u,v)
                            G.add_edge(x,y)
                            G.remove_edge(u,y)
                            G.remove_edge(x,v)
                            continue 
                    swapcount=swapcount+1              
    return G       
'''
###################################################
#函数名称：inner_random_2k
#功能：基于随机断边重连的2阶零模型
       (保证2阶特性不变的前提下，对社区内部的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inner_random_2k(G0,node_community_list,nswap=1, max_tries=100,connected=1):
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团内部连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边还是社团内连边			
    
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                        
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
    
                            if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                                if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    G.add_edge(u,v)
                                    G.add_edge(x,y)
                                    G.remove_edge(u,y)
                                    G.remove_edge(x,v)
                                    continue 
                            swapcount=swapcount+1              
    return G       
 
'''
###################################################
#函数名称：inner_random_25k
#功能：基于随机断边重连的2阶零模型
       (保证2.5阶特性不变的前提下，对社区内部的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inner_random_25k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团内部连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边还是社团内连边			
    
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                        
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
    
                           
                            degree_node_list = [(t[1],t[0]) for t in list(G0.degree([u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y])))]  
                        		#先找到四个节点以及他们邻居节点的集合，然后取出这些节点所有的度值对应的节点，格式为（度，节点）形式的列表
                        		
                            D = dict_degree_nodes(degree_node_list) # 找到每个度对应的所有节点，具体形式为
                            for i in range(len(D)):
                                avcG0 = nx.average_clustering(G0, nodes=list(D.values())[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(G, nodes=list(D.values())[i], weight=None, count_zeros=True)
                                i += 1
                                if avcG0 != avcG:   #若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                                    G.add_edge(u,v)
                                    G.add_edge(x,y)
                                    G.remove_edge(u,y)
                                    G.remove_edge(x,v)
                                    break
                                if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                                    if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                        G.add_edge(u,v)
                                        G.add_edge(x,y)
                                        G.remove_edge(u,y)
                                        G.remove_edge(x,v)
                                        continue 
                                swapcount=swapcount+1 
                
    return G       
'''
###################################################
#函数名称：inner_random_3k
#功能：基于随机断边重连的3阶零模型
       (保证3阶特性不变的前提下，对社区内部的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inner_random_3k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边还是社团内连边			
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
            				
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                    
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
                    		
                            node_list=[u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y]) #找到四个节点以及他们邻居节点的集合
                            avcG0 = nx.clustering(G0, nodes=node_list) #计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)   #计算新网络中4个节点以及他们邻居节点的聚类系数
                            
                            if avcG0 != avcG:                           #保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u,v)
                                G.add_edge(x,y)
                                G.remove_edge(u,y)
                                G.remove_edge(x,v)
                                continue
                            if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                                if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    G.add_edge(u,v)
                                    G.add_edge(x,y)
                                    G.remove_edge(u,y)
                                    G.remove_edge(x,v)
                                    continue 
                            swapcount=swapcount+1              
    return G       
'''
###################################################
#函数名称：inter_random_0k
#功能：基于随机断边重连的0阶零模型
      (保证0阶特性不变的前提下，对社区间的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inter_random_0k(G0,node_community_list,nswap=1, max_tries=100,connected=1):  

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("It is only allowed for undirected networks")
    if nswap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")  
        
    G = copy.deepcopy(G0)      

    tn = 0
    swapcount = 0
    edges = []
    nodes = []
    edges = list(G.edges())
    nodes = list(G.nodes())
    while swapcount < nswap:
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        random_edge = random.choice(edges)      #随机选网络中的一条要断开的边
        u = random_edge[0]
        v = random_edge[1]
        x,y = random.sample(nodes,2)    #随机找两个不相连的节点
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团间连边
            #保证新生成的边还是社团间连边			
                if (x,y) not in edges and (y,x) not in edges:
                    G.remove_edge(u,v)              #断旧边
                    G.add_edge(x,y)                 #连新边
                    edges.remove((u,v))
                    edges.append((x,y))
            
                if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                    if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                        G.remove_edge(x,y)              #断新边
                        G.add_edge(u,v)                 #连旧边
                        edges.remove((x,y))
                        edges.append((u,v))
                        continue 
                    swapcount=swapcount+1             
    return G
'''
###################################################
#函数名称：inter_random_1k
#功能：基于随机断边重连的1阶零模型
      (保证1阶特性不变的前提下，对社区间的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inter_random_1k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 
#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边还是社团间连边			
    
                    if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                         
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
    
    
                    if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                        if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                            G.add_edge(u,v)
                            G.add_edge(x,y)
                            G.remove_edge(u,y)
                            G.remove_edge(x,v)
                            continue 
                    swapcount=swapcount+1              
    return G   

'''
###################################################
#函数名称：inter_random_2k
#功能：基于随机断边重连的2阶零模型
      (保证2阶特性不变的前提下，对社区间的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inter_random_2k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 
# 保证2k特性不变和网络联通的情况下，交换社团外部的连边
# G0：待改变结构的网络
# node_community_list：是网络中节点的社团归属信息
# nswap：是改变成功的系数，默认值为1
# max_tries：是尝试改变的次数，默认值为100
# connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团内部连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边还是社团内连边			


                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                        
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
    
                            if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                                if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    G.add_edge(u,v)
                                    G.add_edge(x,y)
                                    G.remove_edge(u,y)
                                    G.remove_edge(x,v)
                                    continue 
                            swapcount=swapcount+1              
    return G       

'''
###################################################
#函数名称：inter_random_25k
#功能：基于随机断边重连的2.5阶零模型
      (保证2.5阶特性不变的前提下，对社区间的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inter_random_25k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团内部连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边还是社团内连边			
    
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                        
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
    
                           
                            degree_node_list = [(t[1],t[0]) for t in list(G0.degree([u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y])).items())]  
                        		#先找到四个节点以及他们邻居节点的集合，然后取出这些节点所有的度值对应的节点，格式为（度，节点）形式的列表
                        		
                            D = dict_degree_nodes(degree_node_list) # 找到每个度对应的所有节点，具体形式为
                            for i in range(len(D)):
                                avcG0 = nx.average_clustering(G0, nodes=list(D.values())[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(G, nodes=list(D.values())[i], weight=None, count_zeros=True)
                                i += 1
                                if avcG0 != avcG:   #若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                                    G.add_edge(u,v)
                                    G.add_edge(x,y)
                                    G.remove_edge(u,y)
                                    G.remove_edge(x,v)
                                    break
                                if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                                    if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                        G.add_edge(u,v)
                                        G.add_edge(x,y)
                                        G.remove_edge(u,y)
                                        G.remove_edge(x,v)
                                        continue 
                                swapcount=swapcount+1 
            
    return G       


'''
###################################################
#函数名称：inter_random_3k
#功能：基于随机断边重连的3阶零模型
      (保证3阶特性不变的前提下，对社区间的边进行置乱)
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2：node_community_list(网络中节点的社团归属信息)
       参数3：nswap(改变成功的系数，默认值为1)
       参数4：max_tries(尝试改变的次数，默认值为100)
       参数5：connected(是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inter_random_3k(G0,node_community_list,nswap=1, max_tries=100,connected=1): 
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边还是社团内连边			
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
            				
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                    
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
                    		
                            node_list=[u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y]) #找到四个节点以及他们邻居节点的集合
                            avcG0 = nx.clustering(G0, nodes=node_list) #计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)   #计算新网络中4个节点以及他们邻居节点的聚类系数
                            
                            if avcG0 != avcG:                           #保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u,v)
                                G.add_edge(x,y)
                                G.remove_edge(u,y)
                                G.remove_edge(x,v)
                                continue
                            if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                                if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    G.add_edge(u,v)
                                    G.add_edge(x,y)
                                    G.remove_edge(u,y)
                                    G.remove_edge(x,v)
                                    continue 
                            swapcount=swapcount+1              
    return G       

'''
###################################################
#函数名称：inner_community_swap
#功能：保证度分布不变的情况下，交换社团内的连边
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2: node_community_list(网络中节点的社团归属信息)
       参数2：nswap(改变成功的系数，默认值为1)
       参数3：max_tries(尝试改变的次数，默认值为100)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inner_community_swap(G0,node_community_list,nswap=1, max_tries=100): 

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团内连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边还是社团内连边			
                    if (y not in G[u]) and (v not in G[x]): #保证新生成的连边是原网络中不存在的边
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
                
                        swapcount+=1							  #改变成功次数加1               
    return G
'''
###################################################
#函数名称：inter_community_swap
#功能：保证度分布不变的情况下，交换社团间的连边
#输入参数：
       参数1：G0(待改变结构的网络)
       参数2: node_community_list(网络中节点的社团归属信息)
       参数2：nswap(改变成功的系数，默认值为1)
       参数3：max_tries(尝试改变的次数，默认值为100)
#输出参数：G(改变结构后的网络)
###################################################
'''
def inter_community_swap(G0,node_community_list,nswap=1, max_tries=100): 

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证为四个独立节点
            if edge_in_community(node_community_list,(u,v)) == 0 and edge_in_community(node_community_list,(x,y)) == 0: #保证所取的连边是社团间部连边
                if edge_in_community(node_community_list,(u,y)) == 0 and edge_in_community(node_community_list,(v,x)) == 0: #保证新生成的边是社团间的连边
                    if (y not in G[u]) and (v not in G[x]): #保证新生成的连边是原网络中不存在的边
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
                
                        swapcount = swapcount + 1			   #改变成功次数加1
                
    return G     	
    
'''
###################################################
#函数名称：Q_increase_1k
#功能：保证1阶特性不变的前提下，增加社区间的连边，减少社区内部的连边，
       以达到减弱社区结构的作用。
#输入参数：
    参数1：G0(待改变结构的网络)
    参数2：node_community_list（网络中节点的社团归属信息）
    参数3：nswap（改变成功的系数，默认值为1）
    参数4：max_tries（尝试改变的次数，默认值为100）
#输出参数：G(改变后的网络)
###################################################
'''      
def Q_increase_1k(G0,node_community_list,nswap=1, max_tries=100): 
    
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边是内部连边	
                    if (y not in G[u]) and (v not in G[x]): #保证新生成的连边是原网络中不存在的边
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
                
                        swapcount+=1							  #改变成功次数加1
                
    return G     
'''
###################################################
#函数名称：Q_decrease_1k
#功能：保证1阶特性不变的前提下，增加社区间的连边，减少社区内部的连边，
       以达到减弱社区结构的作用。
#输入参数：
    参数1：G0(待改变结构的网络)
    参数2：node_community_list（网络中节点的社团归属信息）
    参数3：nswap（改变成功的系数，默认值为1）
    参数4：max_tries（尝试改变的次数，默认值为100）
#输出参数：G(改变后的网络)
###################################################
'''    
def Q_decrease_1k(G0,node_community_list,nswap=1, max_tries=100): 
#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) #keys表示节点，degrees为每个节点对应的度值
    cdf = nx.utils.cumulative_distribution(degrees) #度的累积分布
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf) #离散序列
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        
        if len(set([u,v,x,y])) == 4: #保证为四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边是社团内部连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边是社团间的连边
                    if (y not in G[u]) and (v not in G[x]): #保证新生成的连边是原网络中不存在的边
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
                
                        swapcount+=1							  #改变成功次数加1
                
    return G     
'''
###################################################
#函数名称：Q_decrease_2k
#功能：保持2阶特性不变的前提下，增加社区间的连边，减少社区内部的连边，
       以达到减弱社区结构的作用
#输入参数：
    参数1：G0(待改变结构的网络)
    参数2：node_community_list（网络中节点的社团归属信息）
    参数3：nswap（改变成功的系数，默认值为1）
    参数4：max_tries（尝试改变的次数，默认值为100）
#输出参数：G(改变后的网络)
###################################################
'''     
def Q_decrease_2k(G0,node_community_list,nswap=1, max_tries=100): 
# connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持
#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团内部连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边是社团间的连边			
    
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                        
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
     
                            swapcount=swapcount+1              
    return G           
'''
###################################################
#函数名称：Q_increase_2k
#功能：保持2阶特性不变的前提下，社区减少间的连边，增加社区内部的连边，
       以达到增强社区结构的作用
#输入参数：
    参数1：G0(待改变结构的网络)
    参数2：node_community_list（网络中节点的社团归属信息）
    参数3：nswap（改变成功的系数，默认值为1）
    参数4：max_tries（尝试改变的次数，默认值为100）
#输出参数：G(改变后的网络)
###################################################
'''   
def Q_increase_2k(G0,node_community_list,nswap=1, max_tries=100): 
#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边是社团内部连边			
    
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                        
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
     
                            swapcount=swapcount+1              
    return G              
 
'''
###################################################
#函数名称：Q_decrease_3k
#功能：保证3阶特性不变的前提下，增加社区间的连边，减少社区内部的连边，
       以达到减弱社区结构的作用。
#输入参数：
    参数1：G0(待改变结构的网络)
    参数2：node_community_list（网络中节点的社团归属信息）
    参数3：nswap（改变成功的系数，默认值为1）
    参数4：max_tries（尝试改变的次数，默认值为100）
#输出参数：G(改变后的网络)
###################################################
'''     
def Q_decrease_3k(G0,node_community_list,nswap=1, max_tries=100): 
#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==1 and edge_in_community(node_community_list,(x,y))==1: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==0 and edge_in_community(node_community_list,(v,x))==0: #保证新生成的边是社团间连边			
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
            				
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                    
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
                    		
                            node_list=[u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y]) #找到四个节点以及他们邻居节点的集合
                            avcG0 = nx.clustering(G0, nodes=node_list) #计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)   #计算新网络中4个节点以及他们邻居节点的聚类系数
                            
                            if avcG0 != avcG:                           #保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u,v)
                                G.add_edge(x,y)
                                G.remove_edge(u,y)
                                G.remove_edge(x,v)
                                continue 
                            swapcount=swapcount+1              
    return G           
'''
###################################################
#函数名称：Q_increase_3k
#功能：保持3阶特性不变的前提下，社区减少间的连边，增加社区内部的连边，
       以达到增强社区结构的作用
#输入参数：
    参数1：G0(待改变结构的网络)
    参数2：node_community_list（网络中节点的社团归属信息）
    参数3：nswap（改变成功的系数，默认值为1）
    参数4：max_tries（尝试改变的次数，默认值为100）
#输出参数：G(改变后的网络)
###################################################
'''     
def Q_increase_3k(G0,node_community_list,nswap=1, max_tries=100): 

#    if not nx.is_connected(G0):
#        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
         
    tn = 0   #尝试次数
    swapcount = 0   #有效交换次数
    
    G = copy.deepcopy(G0)
    keys,degrees = list(zip(*list(G.degree().items()))) 
    cdf = nx.utils.cumulative_distribution(degrees) 
   
    while swapcount < nswap:       #有效交换次数小于规定交换次数      
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print (e)
            break     
        tn += 1 

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        if len(set([u,v,x,y])) == 4: #保证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0: #保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1: #保证新生成的边是社团内部连边			
                    if G.degree(v)==G.degree(y):#保证节点的度匹配特性不变
            				
                        if (y not in G[u]) and (v not in G[x]):       #保证新生成的连边是原网络中不存在的边
                            G.add_edge(u,y)                           #增加两条新连边
                            G.add_edge(v,x)
                    
                            G.remove_edge(u,v)                        #删除两条旧连边
                            G.remove_edge(x,y)
                    		
                            node_list=[u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y]) #找到四个节点以及他们邻居节点的集合
                            avcG0 = nx.clustering(G0, nodes=node_list) #计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)   #计算新网络中4个节点以及他们邻居节点的聚类系数
                            
                            if avcG0 != avcG:                           #保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u,v)
                                G.add_edge(x,y)
                                G.remove_edge(u,y)
                                G.remove_edge(x,v)
                                continue 
                            swapcount=swapcount+1              
    return G               
    
    
