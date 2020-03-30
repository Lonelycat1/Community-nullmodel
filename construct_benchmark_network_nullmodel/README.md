# **保持中尺度特性的零模型构造测试**  
## 测试程序描述：  
目的：保持原始网络微观特性不变的前提下，随机置乱网络， 
程序流程： 
>> 1、读取原始网络；  
>> 2、利用infomap算法对原始网络进行社区划分；    
>> 3、计算原始网络的节点数N和边数M； 
>> 4、根据N和M调整零模型输入参数nswap(2M)和maxtry(10nswap)；
>> 5、调用1阶零模型，构造新的网络；  
>> 6、通过模糊程度系数mu的大小控制内外部连边的比例；
>> 7、得到新网络GAS，再次利用infomap进行社区划分并保存社区信息； 
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
25K:保证网络联合度分布特不变和断边前后度祥光的聚类系数不变  
3k:保证网络联合边度分布特性不变  
changed_community:新网络划分社区信息保存文件  
changed_network:新网络数据保存文件  
