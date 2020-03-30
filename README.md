# **Community Nullmodel**  
## Project Description：
  This project is a test program for community detection benchmark network construction based on null model, which aims to reconstruct the network according to the user's requirements to generate a suitable artificial network.  The project has two parts, as follow:    
*** 
### ***Part 1:* Maintain the mesoscale network feature test program**  
**benchmark_test_for_mesoscale**  
* communitynullmodel_new.py     
* ` benchmark-test.py`     
* karate.txt  

**function description：**  
基于随机断边重连原理，在保持各种网络特性不变的情况下，对原始网络(karate网络)进行重构，生成新网络并保存。  
高亮部分为主程序文件，communitynullmodel_new.py和karate.txt分别为主程序所依赖的库文件与网络数据文件。  
所涉及到的网络特性：  
1、模块度  
2、模糊系数  
3、社区数  
4、平均路径长度  
5、介数  
6、匹配系数  
7、聚类系数  
8、平均聚类系数  
9、平均度  
*** 
2、减弱社区结构测试程序  
**decrease_community_nullmodel**  
* community_detection_algorithm.py  
* ` decrease_community_structure.py`  
* communitynullmodel_new.py  
* karate.txt  

**function description：**   
基于随机断边重连原理，将社区内部的连边随机断开生成社区外的连边，将原始网络(karate网络)重构生成新网络并保存。  
高亮部分为主程序文件，communitynullmodel_new.py、community_detection_algorithm.py和karate.txt分别为主程序所依赖的库文件与网络数据文件。   
## Depend on the environment：
运行环境：[*Anaconda3.7*](https://www.anaconda.com/)  
网络数据：[karate.zip](http://www-personal.umich.edu/~mejn/netdata/karate.zip) 

:stuck_out_tongue_winking_eye:If you think it is helpful or interesting for you, please follow me.








