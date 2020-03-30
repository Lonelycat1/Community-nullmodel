# **Maintain the mesoscale network characteristics test program**  
## program process:  
**Objective**: to randomly scramble the network on the premise of keeping the original network characteristics unchanged.   
Process Description： 
>> 1、Read the data of original network;  
>> 2、use infomap Infomap algorithm to divide the original network into communities；    
>> 3、Get the information original network; 
>> 4、Adjust the input parameters of the null model according to the original network information;
>> 5、According to the user's demand, the null model of different order is selected and a new network is constructed (the test program takes the null model of order 1 as an example).  
>> 6、Adjust the fuzzy coefficient mu to  controll the ratio of the inner and outer edges of the community i;
>> 7、Obtain a new network GAS. Then, use ifomap algorithm to to divide GAS into communities. And save the node ownership information of GAS.   
## Dependent documents: 
>**community_nullmodel:**
>>Random scrambling function in the community:  
>>>inner_random_0k  
>>>inner_random_1k  
>>>inner_random_2k  
>>>inner_random_25k  
>>>inner_random_3k  

>>Random scrambling function outside the community:  
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

>>swap connection function:  
>>>inner_community_swap    
>>>inter_community_swap  

>>Node degree dictionary conversion function:  
>>>dict_degree_nodes  

**Relevant Explanation:**  
0-3k represents the property of order 0-3  
0k:The distribution characteristics of average degree of nodes remains unchanged  
1k:The distribution characteristics of node degree unchanged in the network  
2k:The distribution of network association degree remains unchanged    
25K:The clustering coefficient related to the degree before and after breaking edge remains unchanged  
3k:the distribution characteristics of network joint edges remains unchanged  
changed_community:file of new network node ownership information  
changed_network:file of new network data  
