# **Community Nullmodel**  
## Project Description：
此项目是一个基于零模型的社区检测基准网络构造的测试程序，旨在根据用户生需求进行网络重构生成适合的人工网络。  
项目共有两个部分组成，分别为:  
*** 
1、保持中尺度网络特性测试程序  
**construct_benchmark_network_nullmodel**  
* communitynullmodel_new.py     
* ` benchmark-test.py`     
* karate.txt  

**function description：**  
基于随机断边重连原理，在保持各种网络特性不变的情况下，对原始网络(karate网络)进行重构，生成新网络并保存。  
高亮部分为主程序文件，communitynullmodel_new.py和karate.txt分别为主程序所依赖的库文件与网络数据文件。  
所涉及到的网络微观特性：  
1、Q  
2、MU(模糊系数)  
3、社区数  
4、平均路径长度  
5、betweeness介数  
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
运行环境：*Anconda3.7*  
网络数据：karate.txt  








