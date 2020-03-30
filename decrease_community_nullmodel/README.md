# **Weaken the community structure test program**  
## 测试程序描述：  
目的：减弱社区结构  
程序流程： 
>> 1、Read the data of original network;  
>> 2、use infomap CNM algorithm to divide the original network into communities;      
>> 3、Get the information original network;   
>> 4、Adjust the input parameters of the null model according to the original network information;
>> 5、According to the user's demand, the null model of different order is selected and a new network is constructed (the test program takes );    
>> 6、Obtain a new network. And use use infomap CNM algorithm to divide the original network into communities;  
>> 7、 Save data and the node ownership information of the new network.   
 
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
