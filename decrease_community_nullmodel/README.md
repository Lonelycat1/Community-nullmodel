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
 
## Dependent documents: 
>**community_nullmodel:**
>>Edge random scrambling function inside the community:  
>>>inner_random_0k  
>>>inner_random_1k  
>>>inner_random_2k  
>>>inner_random_25k  
>>>inner_random_3k  

>>Edge random scrambling function outside the communityn:  
>>>inter_random_0k  
>>>inter_random_1k  
>>>inter_random_2k  
>>>inter_random_25k  
>>>inter_random_3k  

>>Enhanced community structure function:  
>>>Q_increase_1k  
>>>Q_increase_2k  
>>>Q_increase_3k  

>>Weaken the community structure function:  
>>>Q_decrease_1k  
>>>Q_decrease_2k  
>>>Q_decrease_3k  

>>Edge judgment function:  
>>>edge_in_community   

>>swap edge function:  
>>>inner_community_swap    
>>>inter_community_swap  

>>Node degree dictionary conversion function:  
>>>dict_degree_nodes  

**Relevant Explanation:**  
0-3k represents the property of order 0-3  
0k: The  characteristics of average degree of nodes distribution remains unchanged.  
1k: The characteristics of node degree distribution remains unchanged.   
2k: The Joint degree distribution of network remains unchanged.    
25K: The clustering coefficient related to the degree before and after disconnect for rewriting remain unchanged.  
3k: The distribution characteristics of network joint edges remains unchanged  
changed_community: file of new network node ownership information  
changed_network: file of new network data  
