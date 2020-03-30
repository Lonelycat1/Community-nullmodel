# **Weaken the community structure test program**  
## program process:    
**Objectiv:** Weaken the community structure  
Process Description:    
>> 1、Read the data of original network;  
>> 2、use infomap CNM algorithm to divide the original network into communities;      
>> 3、Get the information original network;   
>> 4、Adjust the input parameters of the null model according to the original network information;
>> 5、According to the user's requirement, the null model of different order is selected and a new network is constructed (the test program &ensp; takes Q_decrease_1k as an example);    
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

## **Relevant Explanation:**  
**0-3k represents the property of order 0-3**  
&ensp;***0k:*** The  characteristics of average degree of nodes distribution remains unchanged.  
&ensp;***1k:*** The characteristics of node degree distribution remains unchanged.   
&ensp;***2k:*** The Joint degree distribution of network remains unchanged.    
&ensp;***25K:*** The clustering coefficient related to the degree before and after disconnect for rewriting remain unchanged.  
&ensp;***3k:*** The distribution characteristics of network joint edges remains unchanged  
***changed_community:*** file of new network node ownership information  
***changed_network:*** file of new network data  
