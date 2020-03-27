# **Community Nullmodel**  
## Project Description：
此项目是一个基于零模型的社区检测基准网络构造demo，旨在依据用户生成适合的人工网络。  
项目共有两个部分组成，分别为:  
1、保持中尺度网络特性测试程序(位于construct_benchmark_network_nullmodel文件夹）  
2、减弱社区结构测试程序(位于decrease_community_nullmodel文件夹)

运行环境：anconda3.7;  
demo主要使用了karate网络作为测试网络;  
community_nullmodel.py为自定义零模型库;  
community_detection_algorithm为自定义社区测试算法库，demo主要使用了其中DECD算法；  
存储关于社区零模型构造的文件，一共2个部分：  
Construct_benchmark_network_nullmodel文件是基于随机短边重连原理构造中尺度网络;  
decrease_community_nullmodel文件是关于减弱社区结构零模型网络;  





