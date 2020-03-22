# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 18:47:20 2020

@author: LX
"""
############################基于社区局部变化零模型的网络构造#########################

import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import random  
from numpy import random
import networkx as nx
import copy
import pandas as pd
import math
from igraph import*
from communitynullmodel_new import *
'''
###################################################
#函数名称：Edges
#功能：取得列表中所有元素的索引值
#输入参数：
        参数1:communitydivision_list(社区划分列表)
        参数2:edges_dic(连边字典)
#输出参数：edgesinside(内部连边列表)
###################################################
'''
def Edges(communitydivision_list,edges_dic):
    edgesinside = []  
    edge_outside = []
    for node in communitydivision_list:               #通过循环得到所有节点的社团内部连边
        try:
            for edges in edges_dic[node]:
                if edges in communitydivision_list:     #判断边是否在社团内部
                    edgesinside.append((node,edges))
                else:
                    edge_outside.append((node,edges))                   
        except:
            pass
        
    return edgesinside #返回内部连边数和外部连边
'''
###################################################
#函数名称：find_all_index
#功能：取得列表中所有元素的索引值
#输入参数：
        参数1:arr(待寻找列表)
        参数2:item(待需要寻找的元素)
#输出参数：index_list(arr中所有元素值等于为item的索引)
###################################################
'''
def find_all_index(arr,item):
    index_list = [i for i,a in enumerate(arr) if a == item]
    return  index_list
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
        pair_node = line[i].split(' ')     #用空格分裂得到节点对    
        node_1 = int(pair_node[0])      #得到第一个节点
        node_2 = int(pair_node[1])      #得到第二个节点
        G.add_edge(node_1,node_2)       #添加边至空网络
    
    return G
'''
###################################################
#函数名称：cleanup
#功能：
    对种群中每个个体中节点的社区标号进行纠错，随机选择个体中的若干个节点，
选几个和选哪几个均为随机。根据其CV值及其邻域节点所属社区更新节点i的社区
#输入参数：
        参数1：x(待纠错种群)
        参数2：n(个体长度)
        参数3：NP(种群大小)
        参数4：Gi(生成的网络)
        参数5：threshold_value()
#输出参数：X(返回纠错后的新种群)
###################################################
'''  
def cleanup(X,n,NP,Gi,threshold_value):
    for i in range(NP):
        # 所有节点标号
        all_node_index = list(range(n))
        # 确定选择节点标号的数目
        get_num=random.randint(1,n)
        # 在1-n号节点中随机选择get_num个不一样的节点标号
        use_node_index=[]        
        # 在个体i中随机选择get_num个不同的节点，保存在use_node_index
        for cu_i in range(get_num):
            # 在1-n节点中随机选取一个节点序号
            cur_rand_index=random.randint(0,len(all_node_index)-1)
            # 添加至use_node_index
            use_node_index.append(all_node_index[cur_rand_index])
            # 将all_node_index中对应的元素删除
            all_node_index.remove(all_node_index[cur_rand_index])
    
        # 对use_node_index中的节点进行纠错
        for rand_i in range(get_num):           
           # 针对use_node_index中的每一个节点进行社区标号纠错
            node=use_node_index[rand_i]
            # 确定节点node的所有邻域个体，包括其自身，如node=16，那么all_adj_node=【16,33,34】
            neigh_node=Gi.neighbors(node)
            
            # 构建节点node自身及邻域集合列表
            # 例如：[2, 0, 1, 3, 7, 8, 9, 13, 27, 28, 32] 
            all_adj_node=[]
            all_adj_node.append(node)
            for k in range(len(neigh_node)):
                all_adj_node.append(neigh_node[k])
                  
            # node及其邻域节点所属的社区编号
            node_comm=X[i][node]
            # node邻域节点所属的社区编号
            node_neigh_comm=[]
            for k in range(len(neigh_node)):
                node_neigh_comm.append(X[i][neigh_node[k]])
            # 计算CV
            # 节点node与邻域个体属于不同社区的数目
            different_comm_number=0
            for k in range(len(node_neigh_comm)):
                if node_comm!=node_neigh_comm[k]:
                   different_comm_number+=1
            # 节点node的度
            degree_node=len(node_neigh_comm)
            # 节点node的CV值
            CV_node=float(different_comm_number)/degree_node
            # 判断CV是否大于阈值
            # 若是，则说明节点node与邻域节点不在同一社区的概率较大
            # 节点社区标号错误,选择邻域节点中出现次数最多的社区标号
            if CV_node > threshold_value:
               # 邻域节点所属社区标号               
               temp_comm=node_neigh_comm
               # 邻域节点所归属最多的社区数目
               max_num = 0
               # 邻域节点所归属最多的社区标号
               max_comm_id = 0
               # 找到node_neigh_comm中邻域节点归属最多的社区
               while len(temp_comm)>0:
                   # 选取第一个邻域节点所属社区cur_comm
                   cur_comm=temp_comm[0]
                   # 归属cur_comm的所有邻域节点的序号集合
                   all_node=[]
                   for k in range(len(temp_comm)):
                       if temp_comm[k]==cur_comm:
                          all_node.append(k)
                   # 归属cur_comm的所有邻域节点数目
                   cur_num=len(all_node)
                   # 比较cur_num与max_num，更新max_num和max_comm_id
                   if cur_num>max_num:
                      # 属于当前社区cur_comm的邻居节点>已知属于同一社区的最多邻居节点数目max_num
                      max_num=cur_num
                      max_comm_id=cur_comm
                   elif cur_num==max_num:
                       # 以50%的概率决定是否更改max_num和max_comm_id
                       if np.random.rand(1,1)>0.5:
                          max_num=cur_num
                          max_comm_id=cur_comm
                   # 删除temp_comm中归属于cur_comm的邻域节点\
                   del_comm=[]       
                   for k in range(len(all_node)):
                       del_comm.append(temp_comm[all_node[k]])
                   for k in del_comm:
                       temp_comm.remove(k) 
                      
               # 将pop中node的社区标号更新为max_comm_id       
               X[i][node]=max_comm_id     
    #返回纠错后的新种群
    return X
'''
###################################################
#函数名称：draw_G
#功能：可视化网络
#输入参数：G(待可视化网络)
#输出参数：无
###################################################
'''
def draw_G(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize = (20,16))
    nx.draw(G,pos,with_labels=True,node_size =500,node_color='w',node_shape = '.')
    for i in range(len(membership_list)):
        if i == 0:
            nx.draw_networkx_nodes(G,pos,nodelist=membership_list[i], node_size=300, node_color='r',node_shape = 's',with_labels=True)
        elif i == 1:
            nx.draw_networkx_nodes(G,pos,nodelist=membership_list[i], node_size=300, node_color='y',node_shape = 'o',with_labels=True)
        elif i == 2:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='g',node_shape = 'H', with_labels=True)
        elif i == 3:
            nx.draw_networkx_nodes(G,pos,nodelist=membership_list[i], node_size=300, node_color='b', node_shape = 'D',with_labels=True)
        elif i == 4:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='c', node_shape = 'h', with_labels=True) 
        elif i == 5:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='lime', node_shape = '*', with_labels=True)
        elif i == 6:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='gold',node_shape = 'd',  with_labels=True)
        elif i == 7:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='tan', node_shape = '>', with_labels=True)
        elif i == 8:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='darkorange', node_shape = '<', with_labels=True)
        elif i == 9:
            nx.draw_networkx_nodes(G, pos,nodelist=membership_list[i], node_size=300, node_color='m', node_shape = '^', with_labels=True)
        plt.show()
'''
###################################################
#函数名称：DECD(差分进化算法)
#功能：利用差分进化得到最优种群并计算其Q值
#输入参数：
#        参数1：NP(种群大小)
#        参数2：Fit(社区适应度)
#        参数2：domain(变量维度)
#        参数3：D(个体长度)
#        参数4：Gen(进化代数)
#        参数5：threshold_value(社区修正阈值)
#        参数6：exetime(执行次数)
#        参数7：F(变异因子)
#        参数8：CR(控制参数，确定每个个体从变异个体中继承的百分比)
#输出参数：无
###################################################
'''  
def DECD(NP,Fit,domain,D,Gen,threshold_value,exetime,F,CR):
    best_in_history=[]
    bestx_in_history=[]
    while exetime < Gen:
    # 输出当前进化代数exetime
        print('exetime=',exetime)
    # 变异操作
        mutation_pop=[]
        for i in range(NP):
            a=random.randint(0,NP-1)  # a in [0,NP-1]
            b=random.randint(0,NP-1)
            c=random.randint(0,NP-1)
            if a==i:
                a=random.randint(0,NP-1)
            if b==i or b==a:
                b=random.randint(0,NP-1)
            if c==i or c==b or c==a:
                c=random.randint(0,NP-1)
         # 构造第i个个体对应的变异个体V
            V=[]
            for j in range(D):
                vec = int(pop[a][j] + F*(pop[b][j]-pop[c][j]))
             # 限制每一维分量的取值范围
                if vec<domain[j][0]:
                     vec=random.randint(domain[j][0],domain[j][1]+1)
                elif vec>domain[j][1]:
                    vec=random.randint(domain[j][0],domain[j][1]+1)
                V.append(vec)
         # 将第i个个体对应的变异个体V存入变异种群mutation_pop
            mutation_pop.append(V)
   
        mutation_pop = cleanup(mutation_pop,n,NP,Gi,threshold_value)
    
    # 交叉操作
        crossover_pop=copy.deepcopy(pop)
#    for i in range(NP):
#        crossover_pop.append(pop[i])
    # 根据DE算法的交叉操作，以概率CR，保留变异种群mutation_pop中的社区性状
        for i in range(NP):
        # 在[0，n-1]范围内，随机选择一维分量
            rand_j=random.randint(0,D)  # rand_j in [0,D-1]
            for j in range(D):
                np.random.randn
                if np.random.rand(1,1)<=CR or j==rand_j:
               # 变异个体i中第j维分量对应的社区标号
                   comm_id_j = mutation_pop[i][j]
               # 变异个体i中属于第comm_id_j个社区的节点集合
                   all_nodes_j=[]
                   all_nodes_j.append(j)
                   for k in range(D):
                       if k!=j and mutation_pop[i][k]==comm_id_j:
                           all_nodes_j.append(k)
               # 交叉个体i中上述节点集合的社区标号全部改为comm_id_j  
                   for k in range(D):
                       if k in all_nodes_j:
                           crossover_pop[i][k]=comm_id_j
    # 交叉种群clean-up operation                 
        crossover_pop=cleanup(crossover_pop,n,NP,Gi,threshold_value)            
    
    # 选择操作
    # 将crossover_pop中的优秀个体保留至下一代种群pop
        for i in range(NP):
            score=ig.GraphBase.modularity(Gi,crossover_pop[i])
            if score > Fit[i]:
                pop[i][:]=crossover_pop[i][:]
                Fit[i]=score
        
    # 记录每一代最优解，绘制收敛曲线        
        best_in_history.append(max(Fit))
        bestx_in_history.append(pop[Fit.index(max(Fit))])
        exetime+=1  
#        ig.GraphBase.modularity(Gi,pop[Fit.index(max(Fit))]) 
    print('The max Q is=',best_in_history[len(best_in_history)-1]) 
    print('The best membership is=',bestx_in_history[len(bestx_in_history)-1])
    print(len(set(bestx_in_history[len(bestx_in_history)-1])))

'''
###################################################
#函数名称：text_save
#功能：文本文件保存
#输入参数：
#        参数1：content(待保存内容)
#        参数2：filename(待生成文件名称)
#        参数3：mode(文件打开模式，默认'a'追加)
#输出参数：X(返回纠错后的新种群)
###################################################
'''       
def text_save(content,filename,mode='a'):
   file = open(filename,mode)
   for edge in content:
        node_1 = str(edge[0])
        node_2 = str(edge[1])        
        file.write(node_1+' '+node_2+'\n')
   file.close()

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

##############################karate网络计算结果#################################
membership_list = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21], 
                   [4, 5, 6, 10, 16], 
                   [8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33], 
                   [23, 24, 25, 27, 28, 31]]
#各个社区内部的节点(nodelist1-4)
nodelist1 = [0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21]
nodelist2 = [4, 5, 6, 10, 16]
nodelist3 = [8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33]
nodelist4 = [23, 24, 25, 27, 28, 31]

#各个社区内部的边(nodelist1_edges-nodelist4_edges)
nodelist1_edges = [(0, 1), (0, 2), (0, 3), (0, 7), (0, 11),(0, 12), (0, 13), (0, 17), (0, 19), (0, 21), 
                   (1, 2), (1, 3), (1, 7), (1, 13), (1, 17), (1, 19), (1, 21), (2, 3), (2, 7), (2, 13), 
                   (3, 7), (3, 12), (3, 13)]

nodelist2_edges = [(4, 10), (4, 6), (5, 16), (5, 10), (5, 6), (6, 16)]

nodelist3_edges = [(8, 32), (8, 30), (8, 33), (9, 33), (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), (18, 33), 
                   (20, 32), (20, 33), (22, 32), (22, 33), (26, 33), (26, 29), (29, 32), (29, 33), (30, 33), (30, 32), 
                   (32, 33)]

nodelist4_edges = [(23, 25), (23, 27), (24, 25), (24, 27), (24, 31), (25, 31), (28, 31)]

#各个社区间的连边
nodelist12_edges = [(0, 1), (0, 2), (0, 3), (0, 7), (0, 11),(0, 12), (0, 13), (0, 17), (0, 19), (0, 21),
                    (4, 10), (4, 6), (5, 16), (5, 10), (5, 6),(6, 16), (1, 2), (1, 3), (1, 7), (1, 13), 
                    (1, 17), (1, 19), (1, 21), (2, 3), (2, 7), (2, 13), (3, 7), (3, 12), (3, 13),(0, 4),
                    (0, 5),(0, 6),(0, 10)]

nodelist13_edges = [(0, 1), (8, 32), (8, 30), (8, 33), (9, 33), (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), 
                    (18, 33), (20, 32), (20, 33), (22, 32), (22, 33), (26, 33), (26, 29), (29, 32),(29, 33), (30, 33),
                    (30, 32), (32, 33),(0, 2), (0, 3), (0, 7), (0, 11), (0, 12), (0, 13), (0, 17), (0, 19), 
                    (0, 21), (1, 2), (1, 3), (1, 7), (1, 13), (1, 17), (1, 19), (1, 21), (2, 3), (2, 7), 
                    (2, 13), (3, 7), (3, 12), (3, 13),(0, 8),(1, 30),(2, 32),(2, 8),(2, 9), (13, 33),(19, 33)]

nodelist14_edges = [(0, 1), (23, 25), (23, 27), (24, 25), (24, 27), (24, 31), (25, 31), (28, 31),(0, 2), (0, 3), 
                    (0, 7), (0, 11), (0, 12), (0, 13), (0, 17), (0, 19), (0, 21), (1, 2), (1, 3), (1, 7), 
                    (1, 13), (1, 17), (1, 19), (1, 21), (2, 3), (2, 7), (2, 13), (3, 7), (3, 12), (3, 13),
                    (0, 31),(2, 27),(2, 28)]

nodelist23_edges = [(4, 10), (4, 6), (5, 16), (5, 10), (5, 6), (6, 16),(8, 32), (8, 30), (8, 33), (9, 33), 
                    (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), (18, 33), (20, 32), (20, 33), (22, 32), (22, 33),
                    (26, 33), (26, 29), (29, 32), (29, 33), (30, 33), (30, 32), (32, 33)]

nodelist24_edges = [(4, 10), (4, 6), (5, 16), (5, 10), (5, 6), (6, 16),(23, 25), (23, 27), (24, 25), (24, 27), 
                    (24, 31), (25, 31), (28, 31)]

nodelist34_edges = [(8, 32), (23, 25), (23, 27), (24, 25), (24, 27), (24, 31), (25, 31), (28, 31),(8, 30), (8, 33),
                    (9, 33), (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), (18, 33), (20, 32), (20, 33), (22, 32),
                    (22, 33), (26, 33), (26, 29), (29, 32), (29, 33), (30, 33), (30, 32), (32, 33),(29, 23),(32, 23), 
                    (32, 31),(33, 23), (33, 27), (33, 28), (33, 31)]

nodelist12 = [0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21,4, 5, 6, 10, 16]

nodelist13 = [0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21,8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33]

nodelist14 = [0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21,23, 24, 25, 27, 28, 31]

nodelist23 = [4, 5, 6, 10, 16,8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33]

nodelist24 = [4, 5, 6, 10, 16,23, 24, 25, 27, 28, 31]

nodelist34 = [8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33,23, 24, 25, 27, 28, 31]


membership_list12 = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21], 
                     [4, 5, 6, 10, 16]]

membership_list13 = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21],
                     [8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33]]

membership_list14 = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21],
                     [23, 24, 25, 27, 28, 31]]

membership_list23 = [[4, 5, 6, 10, 16], 
                     [8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33]]

membership_list24 = [[4, 5, 6, 10, 16],
                     [23, 24, 25, 27, 28, 31]]

membership_list34 = [[8, 9, 14, 15, 18, 20, 22, 26, 29, 30, 32, 33], 
                     [23, 24, 25, 27, 28, 31]]

edges_12 = nodelist12_edges

#读取原始网络
G = nx.Graph() 
G = load_Graph('karate.txt')
all_edges = G.edges()
all_nodes = G.nodes() 
M = G.number_of_edges()
edges_dic = nx.to_dict_of_lists(G)

##第1步：生成局部网络
G1 = nx.Graph()
G1.add_nodes_from(nodelist12)           #加点集合
G1.add_edges_from(edges_12)             #加边集合
origin_edges = nx.to_edgelist(G1)

##第2步：生成零模型
M1 = G1.number_of_edges()  
nswap = 2*M1     
maxtry = 10*nswap
#调用1阶零模型
GAS = inner_random_1k(G1,membership_list12,nswap=nswap, max_tries=maxtry)
#保存新的网络信息 
nx.write_edgelist(GAS,'all_inter'+'.txt',data=False)

##第3步：获取零模型生成的新的连边信息
G11 = nx.Graph()
G11 = load_Graph('all_inter.txt')       #生成局部网络图
edges12_new = G11.edges()               #改变后的局部网络的所有边列表

#第4步：将原始网络中存在的连边信息替换为新生成的连边信息
all_edges_new = G.edges()               #获取原始网络的所有边   
old_edges = []                      
for i in edges_12: 
    old_edges.append(i)                 #记录移除的旧边             
    list(all_edges_new).remove(i)       #移除旧边
    
print('The old edges that are going to be replaced are：',old_edges)

renew_edges = []
for (m,k) in edges12_new:
    #保证新生成的边为社区内部的连边   
    if ((m in nodelist12) and (k in nodelist12)):       
        list(all_edges_new).append((m,k))      #更新新边
        renew_edges.append((m,k))              #记录更新的边
print('These latest edges are：',renew_edges)
#保存更新完毕后的所有边
text_save(all_edges_new,'network12.txt')
#将连边列表转化为int型
all_edges_new_s = list(all_edges_new)
#
#第5步：合成新网络
G1_end = nx.Graph()
G1_end.add_nodes_from(all_nodes)            #加点集合all_nodes
G1_end.add_edges_from(all_edges_new)        #加边集合all_edges_new  
      
Gi = ig.Graph.Read_Edgelist('network12.txt') 
origin_edges_new = nx.to_edgelist(G1_end)
new_list_new = []
for edge_i in range(0,len(origin_edges_new)):
    node_dict = list(origin_edges_new)[edge_i]
    new_list_new.append([node_dict[0],node_dict[1]])          

Gi = Graph(new_list_new)                     #用变向量列表创建图形
h1 = Gi.community_fastgreedy (weights=None)  # fastgreedy算法社团检测
c1 = list(h1.as_clustering())                #对系统树图进行切割，按照Q值最大的标准
print(h1)
print(c1)

membership=[]
for i in range(0,len(G)):
   membership.append(0) 
#根据社团划分对membership赋值
for i in range(0,len(membership_list)):
    nodes = membership_list[i]
    for j in nodes:
        membership[j]=i
print(membership)
#根据membership计算模块度
Q = GraphBase.modularity(Gi,membership)      #计算Q值
print(Q)

#第6步：计算合成后的网络的模块度值使用DECD计算
n = G1_end.number_of_nodes()    #获取最后合成的新网络的节点列表
NP = 100
Gen = 100                       #进化迭代100次数
threshold_value = 0.7
exetime = 1
F = 0.9
CR = 0.3

xmin = 1
xmax = n  
D = n 
#每一维分量的取值范围[1,n]
domain = []  
for i in range(0,n):                                                        #128
    domain.append((xmin,xmax)) 
pop = []
for i in range(NP):                                                         #100
    vec = [random.randint(domain[j][0],domain[j][1]+1) 
         for j in range(D)]                                                 #100*128     
    pop.append(vec)    

Fit = []      #自适应值
for i in range(NP):
    fit = GraphBase.modularity(Gi,pop[i])
    Fit.append(fit)

DECD(NP,Fit,domain,D,Gen,threshold_value,exetime,F,CR)




#社团划分之后每一部分所得模块度值
##LFR-100
#nodelist1_random_Q_1kc=[0.726325416141,0.725726701183,0.725726701183,0.726034570147,0.725882737293,0.726034570147,0.725882737293,0.726325416141,0.726464322745,0.726034570147]
#nodelist2_random_Q_1kc=[0.729983276528,0.730893121302,0.732752071264,0.730597599504,0.73146129681,0.73146129681,0.731180993291,0.730597599504,0.731734112288,0.731734112288]
#nodelist3_random_Q_1kc=[0.728862286738,0.728604899393,0.728862286738,0.728862286738,0.729354743368,0.728862286738,0.728862286738,0.728067398071,0.7291122078,0.729354743368]
#nodelist4_random_Q_1kc=[0.729757681013,0.728975398247,0.730697949237,0.728975398247,0.729757681013,0.730473657259,0.730697949237,0.730003601115,0.730242233728,0.730697949237]
#nodelist5_random_Q_1kc=[0.729482065887,0.728666349906,0.728818517911,0.728666349906,0.728507526591,0.728507526591,0.728964103935,0.728818517911,0.728507526591,0.728169616497]
#nodelist6_random_Q_1kc=[0.728658686021,0.72985473823,0.729085372013,0.729483852525,0.729288099462,0.728658686021,0.728875593414,0.729288099462,0.730030020111,0.729085372013]
#all_random_Q_1kc=[0.729288099462,0.729288099462,0.725882737293,0.729288099462,0.726464322745,0.732752071264,0.73146129681,0.73146129681,0.730893121302,0.730893121302,0.730893121302]
#nodelist1_random_Q_1kc=[0.523046875,0.533912513336,0.528413255661,0.525078125,0.533912513336,0.530805138691,0.526561475252,0.528515625,0.524296875,0.533455265966]
#nodelist2_random_Q_1kc=[0.532754849582,0.532593495643,0.533682294037,0.532152707214,0.531404958678,0.532152707214,0.534369549605,0.531496786042,0.53481079932,0.53303925737]
#nodelist3_random_Q_1kc=[]
#nodelist4_random_Q_1kc=[0.52740234375,0.529107673315,0.529319856487,0.529570618417,0.5271875,0.52765625,0.528664017592,0.52765625,0.524168347771,0.529319856487]
#nodelist5_random_Q_1kc=[0.527842518556,0.527739094433,0.529742909391,0.527566574839,0.529742909391,0.529539846132,0.528290723941,0.528165226433,0.529742909391,0.528903049613]
#all_random_Q_1kc=[0.544012345679,0.56475,0.531702484377,0.56475,0.529765625,0.525789900081,0.56475,0.56475,0.56475,0.56475]
##计算平均值及标准差
#n = len(all_random_Q_1kc)
#n = list(range(0,n+10,10))
#a = 0
#ave = []
#std = []
#for i in n[1:]:
#    ave.append(float(sum(all_random_Q_1kc[a:i]))/10)#平均值
#    std.append(np.std(all_random_Q_1kc[a:i]))#标准差
#    a=i
#print(ave)
#print(std)
##画网络图
#draw_G(G)





