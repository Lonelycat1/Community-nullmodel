# **Community Nullmodel**  
## Project Description：
>> This project is a test program for community detection benchmark network construction based on null model, which aims to reconstruct the network according to the user's requirements to generate a suitable artificial network.  The project has two parts, as follow:    
*** 
### ***Part 1:* Maintain the mesoscale network feature test program**  
**mesoscale_benchmark_test**  
* communitynullmodel_new.py     
* ` mesoscale_benchmark_test.py`     
* karate.txt  

**function description：**  
>> Based on the principle of random reconnection of broken edges, the original network (karate network) was reconstructed and a new network was generated and saved under the condition of keeping various network characteristics unchanged.    

>> The highlighted part is the main program file. Communitynullmodel_new.py is a library file on which  main program depends. And karate.txt is a file of network data.  

>> involved network characteristics:  
1、modularity  
2、fuzzy coefficient  
3、number of communities  
4、average path length  
5、betweeness  
6、matching coefficient  
7、clustering coefficient  
8、average clustering coefficient  
9、average degree  
*** 
### ***Part 2:* Weaken the community structure test program** 
**weaken_benchmark_test**  
* community_detection_algorithm.py  
* ` decrease_community_structure.py`  
* communitynullmodel_new.py  
* karate.txt  

**function description：**   
>> Based on the principle of random broken edge reconnection, the connection inside the community is randomly disconnected to generate the connection outside the community, and the original network (karate network) is reconstructed to generate a new network and saved.  

>> The highlighted part is the main program file. Communitynullmodel_new.py is a library file on which  main program depends. And karate.txt is a file of network data.     
## Depend on the environment：
Runtime Environment：[*Anaconda3.7*](https://www.anaconda.com/)  
Network Data：[karate.zip](http://www-personal.umich.edu/~mejn/netdata/karate.zip) 

:stuck_out_tongue_winking_eye:If you think it is helpful or interesting for you, please follow me.








