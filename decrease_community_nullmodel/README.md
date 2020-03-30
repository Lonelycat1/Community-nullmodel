# **减弱社区结构测试程序**  
## 测试程序描述：  
目的：减弱社区结构  
程序流程： 
>> 1、Read the data of original network;  
>> 2、use CNM algorithm 算法对原始网络进行社区划分； 
>> 3、获取原始网络信息；
>> 4、根据原始网络信息调整零模型输入参数；  
>> 5、根据用户需求选择相应的功能和相应阶数的零模型(测试程序以1阶减弱社区结构零模型Q_decrease_1k为例);   
>> 6、生成新的网络，利用CNM算法对新网络进行社区划分；   
>> 7、保存新网络数据和节点归属信息；  
## 相关依赖文件： 
>**community_nullmodel:**
>>社区内部随机置乱函数：  
>>>inner_random_0k  
>>>inner_random_1k  
>>>inner_random_2k  
>>>inner_random_25k  
>>>inner_random_3k  

>>社区外部随机置乱函数：  
>>>inter_random_0k  
>>>inter_random_1k  
>>>inter_random_2k  
>>>inter_random_25k  
>>>inter_random_3k  

>>增强社区结构函数：  
>>>Q_increase_1k  
>>>Q_increase_2k  
>>>Q_increase_3k  

>>减弱社区结构函数：  
>>>Q_decrease_1k  
>>>Q_decrease_2k  
>>>Q_decrease_3k  

>>连边判断函数：  
>>>edge_in_community   

>>交换连边函数：  
>>>inner_community_swap    
>>>inter_community_swap  

>>节点度字典转换函数：  
>>>dict_degree_nodes  

**相关解释说明：**  
0-3k代表所保持0-3阶特性  
0k:保证节点平均度分布特性不变  
1k:保证网络中节点度分布特性不变  
2k:保证网络联合度分布特不变    
25K:保证网络联合度分布特不变和断边前后度相关的聚类系数不变  
3k:保证网络联合边度分布特性不变  
changed_community:新网络节点归属信息保存文件  
changed_network:新网络数据保存文件  
