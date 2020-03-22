# -*- coding: utf-8 -*-
"""
Created on Mon May 28 15:22:46 2018

@author: lenovo
"""

#所有算法计算模块度Q和归一化互信息NMI值
#(1) nx.k_clique_communities(G, 3) [Newman 2005] 
#
#(2) fastgreedy.community [Clauset et al., 2004] (modularity optimization method)
#
#(3) edge.betweenness.community [Newman and Girvan, 2004]
#
#(4) DECD[2017]
#
#(5) label.propagation.community [Raghavan et al., 2007]
#
#(6) multilevel.community [Blondel et al., 2008] (the Louvain method)
#
#(7) walktrap.community [Pons and Latapy, 2005]

#(8) leading.eigenvector.community [Newman, 2006]
#
#(9) infomap.community [Rosvall and Bergstrom, 2008] 
#
#(10) spinglass.community [Reichardt and Bornholdt, 2006]no
#
#(11) optimal.community [Brandes et al., 2008]no
#
#(12) GSA [Karaboga, 2009]no
#



#K派系算法
#计算dolphins网络在用k派系算法划分社区时的模块度
#import networkx as nx
#from igraph import*
#import matplotlib.pyplot as plt 
#import igraph as ig
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#dolphins=open('C:\\Users\\Lenovo\\Desktop\\network_bq\\ys\\after\\bqcb_network_afterunweight.txt') 
#dolphins=dolphins.read()
##第2步：根据网络边列表生成图
#G = nx.Graph()
#liebiao=dolphins.split("\n") # 用回车符分裂字符串
#for i in range(0,len(liebiao)-1):
#    liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#    node1=int(liebiao1[0])   #节点转化为整数
#    node2=int(liebiao1[1])
#    G.add_edge(node1,node2)
#c=list(nx.k_clique_communities(G, 3)) # k=3 
#membership=[]
#for i in range(0,len(G)):
#   membership.append(0) 
#for i in range(0,len(c)):
#    nodes=c[i]
#    for j in nodes:
#        membership[j]=i
#origin_edges=nx.to_edgelist(G) #三元组形式
#new_list=[]
#for edge_i in range(0,len(origin_edges)):
#    node_dict=origin_edges[edge_i]
#    new_list.append([node_dict[0],node_dict[1]])
#g1=Graph(new_list)   #生成一个图
#Q=GraphBase.modularity(g1, membership)
#print Q
#comm1=membership
#    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
#           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
#           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community7.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI     
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)

###########################################################################
##fastgreedy算法CNM算法
#import networkx as nx
#from igraph import*
#import matplotlib.pyplot as plt
##all_Q=[]
##all_NMI=[]
##steps=0
##while steps<10:
#karate=open('C:\\Users\\Lenovo\\Desktop\\bqgx_network_250unweight.txt')
#karate=karate.read()
#G = nx.Graph()
#liebiao=karate.split("\n")  #用回车符分裂字符串
#for i in range(0,len(liebiao)-1):
#    liebiao1=liebiao[i].split()     #用空格符分裂0和1
#    node1=int(liebiao1[0])          #节点转化为整数
#    node2=int(liebiao1[1])
#    G.add_edge(node1,node2)
#origin_edges=nx.to_edgelist(G)
#new_list=[]
#for edge_i in range(0,len(origin_edges)):
#    node_dict=origin_edges[edge_i]
#    new_list.append([node_dict[0],node_dict[1]])          
#g1=Graph(new_list)  #  用变向量列表创建图形
#h1=g1.community_fastgreedy(weights=None)
#c=list(h1.as_clustering())
#community_list_gx=[[2, 6, 19, 37, 54, 58, 69, 75, 87, 89, 90, 93, 94, 113, 118, 119, 122, 128, 131, 143, 158, 199, 204, 205, 216, 229, 235, 247, 260, 262, 276, 277, 310, 312, 348, 363, 377, 392, 393, 397, 406, 408, 410, 411, 417, 432, 436, 456, 461, 468, 473, 487, 505, 507, 516, 525, 551, 560, 565, 574, 580, 592, 599, 615, 621, 623, 629, 639, 644, 651, 655, 662, 680, 689, 704, 708, 711, 718, 733, 736, 740, 745, 759, 785, 788, 792, 796, 800, 806, 838, 848, 856, 858, 859, 883, 892, 900, 905, 909, 915, 934, 936, 939, 940, 963, 970, 971, 978],[12, 24, 28, 35, 127, 160, 169, 174, 233, 267, 294, 391, 440, 466, 472, 547, 594, 654, 671, 685, 698, 720, 723, 734, 770, 779, 781, 810, 831, 931, 967],[13, 67, 80, 98, 133, 157, 180, 217, 220, 237, 292, 340, 355, 442, 444, 452, 478, 489, 566, 582, 669, 675, 714, 722, 798, 823, 871, 930],[16, 29, 31, 36, 40, 45, 48, 55, 71, 73, 76, 78, 81, 96, 101, 104, 108, 109, 124, 142, 144, 151, 161, 162, 165, 206, 228, 232, 250, 257, 265, 269, 271, 273, 274, 279, 290, 291, 295, 296, 303, 311, 321, 326, 332, 342, 345, 356, 360, 366, 372, 384, 387, 388, 390, 401, 412, 415, 420, 424, 427, 445, 446, 470, 476, 484, 485, 495, 497, 508, 514, 518, 535, 563, 567, 570, 572, 575, 579, 581, 588, 596, 598, 600, 603, 614, 632, 687, 694, 717, 719, 739, 748, 750, 755, 777, 780, 802, 816, 820, 841, 861, 867, 873, 874, 875, 886, 890, 891, 895, 899, 901, 917, 926, 948, 951, 952, 958, 960, 961, 980],[17, 20, 22, 25, 26, 33, 62, 64, 72, 86, 95, 110, 112, 116, 123, 126, 136, 154, 156, 164, 168, 170, 172, 173, 176, 186, 187, 193, 195, 196, 200, 201, 203, 208, 215, 219, 238, 242, 251, 256, 259, 284, 287, 316, 319, 322, 325, 365, 379, 386, 395, 422, 426, 428, 433, 437, 443, 450, 460, 463, 467, 479, 480, 490, 491, 499, 506, 509, 510, 511, 513, 522, 523, 532, 559, 561, 578, 585, 587, 601, 626, 628, 631, 635, 636, 637, 642, 643, 647, 649, 653, 661, 663, 676, 691, 692, 693, 695, 696, 738, 743, 744, 754, 758, 763, 764, 772, 790, 795, 804, 807, 821, 842, 843, 849, 880, 884, 911, 913, 914, 916, 919, 923, 957, 959, 975],[27, 313],[34, 100, 448, 504, 515, 541, 791, 811],[38, 57, 145, 197, 236, 275, 457, 481, 498, 555, 558, 606, 741, 945],[74, 141, 167, 413, 438, 613],[117, 221, 314, 333, 488, 533, 568, 709, 812, 955]]
#community_list_cb=[[2, 6, 19, 22, 25, 26, 31, 38, 54, 55, 69, 75, 89, 90, 93, 94, 104, 112, 113, 122, 126, 128, 131, 142, 143, 158, 161, 164, 170, 172, 193, 196, 199, 200, 201, 203, 205, 208, 216, 228, 235, 242, 250, 259, 262, 271, 277, 284, 287, 310, 311, 325, 326, 348, 363, 366, 372, 377, 379, 386, 388, 397, 406, 408, 422, 426, 428, 436, 437, 443, 445, 457, 461, 467, 476, 478, 506, 507, 509, 511, 513, 522, 523, 525, 559, 565, 572, 575, 585, 588, 601, 621, 628, 629, 639, 642, 649, 651, 653, 663, 689, 691, 692, 693, 695, 696, 704, 711, 718, 719, 736, 738, 743, 744, 748, 750],[12, 24, 28, 127, 160, 169, 176, 233, 391, 395, 480, 547, 654, 671, 685, 734],[13, 36, 45, 48, 62, 67, 71, 73, 80, 81, 86, 96, 101, 108, 109, 118, 124, 154, 157, 162, 165, 173, 180, 197, 217, 232, 247, 265, 269, 274, 279, 290, 303, 319, 322, 332, 342, 345, 355, 360, 365, 384, 390, 392, 411, 412, 424, 432, 442, 444, 452, 479, 481, 484, 489, 495, 497, 498, 499, 505, 514, 518, 535, 555, 558, 563, 570, 579, 598, 603, 606, 623, 632, 662, 669, 675, 687, 708, 714, 717, 722, 741],[16, 74, 141, 151, 167, 296, 413, 427, 438, 490, 551, 567, 613, 698],[17, 20, 27, 33, 40, 57, 58, 72, 87, 98, 110, 116, 119, 145, 156, 186, 187, 215, 219, 220, 236, 237, 238, 251, 260, 273, 291, 295, 313, 356, 387, 415, 420, 433, 446, 456, 460, 463, 472, 485, 487, 508, 557, 561, 566, 578, 580, 587, 599, 615, 631, 643, 644, 676, 723, 739, 745],[29, 35, 37, 64, 123, 136, 168, 174, 229, 256, 267, 275, 276, 292, 294, 312, 316, 340, 393, 401, 410, 417, 440, 473, 516, 560, 574, 581, 582, 592, 594, 626, 636, 637, 655, 680, 694, 720],[34, 100, 448, 504, 515, 541],[117, 221, 314, 333, 488, 533, 568, 709]]
##    membership=[]
##    for i in range(0,len(G)):
##        membership.append(0)
##    #根据社团划分对membership赋值
##    for i in range(0,len(c)):
##        nodes=c[i]
##        for j in nodes:
##            membership[j]=i
##    #根据membership计算模块度
##    Q=GraphBase.modularity(g1,membership)
##    print Q    
##    comm1=membership
###    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
###           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
###           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
###           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
##    filename=('D:\\python\\networks\\LFR\\community9.txt')
##    file = open(filename,'r')
##    content = file.readlines()
##    mem=[]
##    for i in range(len(content)):
##        a,b=content[i].split('\t')
##        mem.append((int(b)))
##    comm0=mem
##    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
##    print NMI     
##    all_Q.append(Q)
##    all_NMI.append(NMI)
##    steps+=1
##print 'The average Q=',sum(all_Q)/len(all_Q)
##print 'The average NMI=',sum(all_NMI)/len(all_NMI)
    
#########################################################################
#GN算法
#import networkx as nx
#from igraph import*
#import igraph as ig
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\LFR\\network9.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    origin_edges=nx.to_edgelist(G)
#    new_list=[]
#    for edge_i in range(0,len(origin_edges)):
#        node_dict=origin_edges[edge_i]
#        new_list.append([node_dict[0],node_dict[1]])          
#    g1=Graph(new_list)  #  用变向量列表创建图形
#    h1=g1.community_edge_betweenness(clusters=None, directed=False, weights=None)
#    c=list(h1.as_clustering())   # 对系统树图进行切割，按照Q值最大的标准
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(c)):
#        nodes=c[i]
#        for j in nodes:
#            membership[j]=i
#    Q=GraphBase.modularity(g1, membership)
#    print Q  #使用GN算法对Dolphins网络进行社区划分并计算模块度    
#    comm1=membership
##    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
##           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
##           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
##           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community9.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI     
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)    
    
##########################################################################
#DECD算法
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import random          # 导入random包
from numpy import random
import networkx as nx
import copy

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
                       if random.rand(1,1)>0.5:
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
    # 返回纠错后的新种群
    return X
def DECD(network_filename,community_filename):
    
    all_Q = []
    all_NMI = []
    steps = 0
    while steps<1:                   
        G = nx.read_edgelist(network_filename)
        G = G.to_undirected()
        n = G.number_of_nodes()
        #基于这些连边使用igraph创建一个新网络
        Gi=ig.Graph.Read_Edgelist(network_filename)  
        Gi=Gi.subgraph(map(int,G.nodes()))          
        Gi=Gi.as_undirected()
        NP = 100
        Gen = 100
        threshold_value = 0.7
        exetime = 1
        F = 0.9
        CR = 0.3
        #构建初始种群，每个个体代表一个社区划分，每个元素对应节点所属社区标号
        #限定种群个体中各维取值范围
        xmin=1
        xmax=n
        D=n
        #每一维分量的取值范围[1,n]
        domain=[]  
        for i in range(0,n):
            domain.append((xmin,xmax))
        #构建初始种群
        #注意：randint函数对于取值范围，包括起始值，但是不包括终值
        pop=[]
        for j in range(NP):          
            vec=[random.randint(domain[j][0],domain[j][1]+1) 
                 for j in range(D)]
            pop.append(vec)
        
        #计算个体适应度值目标函数：模块度函数
        Fit=[]
        for i in range(NP):
            fit=ig.GraphBase.modularity(Gi,pop[i])
            Fit.append(fit)
        #主循环开始
        best_in_history=[]
        bestx_in_history=[]
    
        while exetime < Gen:
        # 输出当前进化代数exetime
            print('exetime=',exetime)
        # 变异操作
            mutation_pop=[]
            for i in range(NP):
                a=random.randint(0,NP)  # a in [0,NP-1]
                b=random.randint(0,NP)
                c=random.randint(0,NP)
                if a==i:
                    a=random.randint(0,NP)
                if b==i or b==a:
                    b=random.randint(0,NP)
                if c==i or c==b or c==a:
                    c=random.randint(0,NP)
                    #构造第i个个体对应的变异个体V
                V=[]
                for j in range(D):
                    vec=int(pop[a][j]+F*(pop[b][j]-pop[c][j]))
                 # 限制每一维分量的取值范围
                    if vec<domain[j][0]:
                        vec=random.randint(domain[j][0],domain[j][1]+1)
                    elif vec>domain[j][1]:
                        vec=random.randint(domain[j][0],domain[j][1]+1)
                    V.append(vec)
             # 将第i个个体对应的变异个体V存入变异种群mutation_pop
                mutation_pop.append(V)
        
        # 变异种群clean-up operation
        # 对种群中每个个体中节点的社区标号进行纠错
        # 随机选择个体中的若干个节点，选几个和选哪几个均为随机。
        # 根据其CV值及其邻域节点所属社区更新节点i的社区    
            mutation_pop=cleanup(mutation_pop,n,NP,Gi,threshold_value)
        
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
                    #变异个体i中属于第comm_id_j个社区的节点集合
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
            exetime += 1   
        
        #ig.GraphBase.modularity(Gi,pop[Fit.index(max(Fit))])
        
        print('The max Q is=',best_in_history[len(best_in_history)-1])
        print('The best membership is=',bestx_in_history[len(bestx_in_history)-1])
        comm1 = bestx_in_history[len(bestx_in_history)-1]
#    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
#           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
#           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
        filename = (community_filename)
        file = open(filename,'r')
        content = file.readlines()
        mem=[]
        for i in range(len(content)):
            a,b=content[i].split(' ')
            mem.append((int(b)))
        comm0 = mem
        NMI = ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
        print(NMI)
        Q = best_in_history[len(best_in_history)-1]
        all_Q.append(Q)
        all_NMI.append(NMI)
        steps += 1
        print('The average Q=',sum(all_Q)/len(all_Q))
        print('The average NMI=',sum(all_NMI)/len(all_NMI))    
    
############################################################################
#标签传播label propagation算法
#import networkx as nx  
#import random                         
#import numpy as np 
#import igraph as ig
#from igraph import*
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\LFR\\network9.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    Gi_d=ig.Graph.Read_Edgelist("D:\\python\\networks\\LFR\\network9.txt")              #基于这些连边使用igraph创建一个新网络
#    Gi=Gi_d.as_undirected()
#    community_list1=Gi.community_label_propagation(weights=None, initial=None, fixed=None)   # 标签传播算法社团检测
#    community_list=[]
#    for item in community_list1:
#        community_list.append(item)        
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(community_list)):
#        nodes=community_list[i]
#        for j in nodes:
#            membership[j]=i
#    Q=community_list1.modularity
#    print Q 
#    comm1=membership
##    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
##           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
##           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
##           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community9.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI         
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#    
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)        
    
#############################################################################
#层次聚类multilevel算法
#import networkx as nx  
#import random                         
#import numpy as np 
#import igraph as ig
#from igraph import*
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\LFR\\network9.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    Gi_d=ig.Graph.Read_Edgelist("D:\\python\\networks\\LFR\\network9.txt")              #基于这些连边使用igraph创建一个新网络
#    Gi=Gi_d.as_undirected()
#    community_list1=Gi.community_multilevel(weights=None, return_levels=False)
#    community_list=[]
#    for item in community_list1:
#        community_list.append(item)        
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(community_list)):
#        nodes=community_list[i]
#        for j in nodes:
#            membership[j]=i
#    Q=community_list1.modularity
#    print Q 
#    comm1=membership
##    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
##           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
##           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
##           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community9.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI         
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#    
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)      
    
##########################################################################
#随机游走walktrap算法
#import networkx as nx
#from igraph import*
#import matplotlib.pyplot as plt
#import igraph as ig
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\LFR\\network9.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    origin_edges=nx.to_edgelist(G)
#    new_list=[]
#    for edge_i in range(0,len(origin_edges)):
#        node_dict=origin_edges[edge_i]
#        new_list.append([node_dict[0],node_dict[1]])          
#    g1=Graph(new_list)  #  用变向量列表创建图形
#    h1=g1.community_walktrap(weights=None, steps=4)
#    c=list(h1.as_clustering())   # 对系统树图进行切割，按照Q值最大的标准
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(c)):
#        nodes=c[i]
#        for j in nodes:
#            membership[j]=i
#    Q=GraphBase.modularity(g1, membership)
#    print Q  #使用GN算法对Dolphins网络进行社区划分并计算模块度    
#    comm1=membership
##    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
##           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
##           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
##           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community9.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI     
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)    
    
#############################################################################
#拉普拉斯矩阵Leading eigenvector算法
#import networkx as nx  
#import random                         
#import numpy as np 
#import igraph as ig
#from igraph import*
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\LFR\\network9.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    Gi_d=ig.Graph.Read_Edgelist("D:\\python\\networks\\LFR\\network9.txt")              #基于这些连边使用igraph创建一个新网络
#    Gi=Gi_d.as_undirected()
#    community_list1=Gi.community_leading_eigenvector(clusters=None)
#    community_list=[]
#    for item in community_list1:
#        community_list.append(item)        
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(community_list)):
#        nodes=community_list[i]
#        for j in nodes:
#            membership[j]=i
#    Q=community_list1.modularity
#    print Q 
#    comm1=membership
##    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
##           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
##           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
##           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community9.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI         
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#    
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)    
    
#############################################################################
#info map算法
#import networkx as nx  
#import random                         
#import numpy as np 
#import igraph as ig
#from igraph import*
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\LFR\\network9.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    Gi_d=ig.Graph.Read_Edgelist("D:\\python\\networks\\LFR\\network9.txt")              #基于这些连边使用igraph创建一个新网络
#    Gi=Gi_d.as_undirected()
#    community_list1=Gi.community_infomap()
#    community_list=[]
#    for item in community_list1:
#        community_list.append(item)        
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(community_list)):
#        nodes=community_list[i]
#        for j in nodes:
#            membership[j]=i
#    Q=community_list1.modularity
#    print Q 
#    comm1=membership
##    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
##           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
##           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
##           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    filename=('D:\\python\\networks\\LFR\\community9.txt')
#    file = open(filename,'r')
#    content = file.readlines()
#    mem=[]
#    for i in range(len(content)):
#        a,b=content[i].split('\t')
#        mem.append((int(b)))
#    comm0=mem
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI         
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#    
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)      
    
#########################################################################
#community_spinglass算法//性能不好
#import networkx as nx  
#import random                         
#import numpy as np 
#import igraph as ig
#from igraph import*
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\karate.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    Gi_d=ig.Graph.Read_Edgelist("D://python//networks//karate.txt")              #基于这些连边使用igraph创建一个新网络
#    Gi=Gi_d.as_undirected()
#    community_list1=Gi.community_spinglass(weights=None,spins=25,parupdate=False,start_temp=1,stop_temp=0.01,cool_fact=0.99,update_rule="config",gamma=1,implementation="orig")
#    community_list=[]
#    for item in community_list1:
#        community_list.append(item)        
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(community_list)):
#        nodes=community_list[i]
#        for j in nodes:
#            membership[j]=i
#    Q=community_list1.modularity
#    print Q 
#    comm1=membership
#    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
#           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
#           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI         
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#    
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)       
    
########################################################################
#community_optimal_modularity算法    
#import networkx as nx  
#import random                         
#import numpy as np 
#import igraph as ig
#from igraph import*
#import matplotlib.pyplot as plt
#all_Q=[]
#all_NMI=[]
#steps=0
#while steps<10:
#    dolphins=open('D:\\python\\networks\\GN\\GN0.txt') 
#    dolphins=dolphins.read()
#    G = nx.Graph()
#    liebiao=dolphins.split("\n") # 用回车符分裂字符串
#    for i in range(0,len(liebiao)-1):
#        liebiao1=liebiao[i].split()  # 用空格符分裂‘0’和‘1’
#        node1=int(liebiao1[0])   #节点转化为整数
#        node2=int(liebiao1[1])
#        G.add_edge(node1,node2)
#    Gi_d=ig.Graph.Read_Edgelist("D://python//networks//GN//GN0.txt")              #基于这些连边使用igraph创建一个新网络
#    Gi=Gi_d.as_undirected()
#    community_list1=Gi.community_optimal_modularity(weights=None)
#    community_list=[]
#    for item in community_list1:
#        community_list.append(item)        
#    membership=[]
#    for i in range(0,len(G)):
#       membership.append(0) 
#    for i in range(0,len(community_list)):
#        nodes=community_list[i]
#        for j in nodes:
#            membership[j]=i
#    Q=community_list1.modularity
#    print Q 
#    comm1=membership
#    comm0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,
#           2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
#           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
#    NMI=ig.compare_communities(comm0, comm1, method='nmi', remove_none=False)
#    print NMI         
#    all_Q.append(Q)
#    all_NMI.append(NMI)
#    steps+=1
#    
#print 'The average Q=',sum(all_Q)/len(all_Q)
#print 'The average NMI=',sum(all_NMI)/len(all_NMI)       
    
######################################################################






    
    