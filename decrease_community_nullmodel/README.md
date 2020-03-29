# **减弱社区结构测试程序**  
## 测试程序描述：  
目的：减弱社区结构  
程序流程： 
>> 1、读取原始网络；  
>> 2、划分原始网络社区；  
>> 3、保存原始网络数据和社区信息；  
>> 4、保证社区结构不变的前提下,随机选取社区内部的边进行断开，生成新边；   
>> 5、保证新生成的边为社区外部的边，否则撤销操作；  
>> 6、循环步骤3与步骤4，直至无法进行断边重连操作；  
>> 7、生成新的网络；   
>> 8、保存新网络数据和社区信息；  
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

相关解释说明：  
0-3k代表所保持0-3阶特性  
0k:保证节点平均度分布特性不变  
1k:保证网络中节点度分布特性不变  
2k:保证网络联合度分布特不变    
25K:保证网络联合度分布特不变和断边前后度祥光的聚类系数不变  
3k:保证网络联合边度分布特性不变  
