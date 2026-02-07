## 1.后端项目搭建
### 1.UV的安装
安装参考：https://uv.doczh.com/getting-started/installation/
### 2.工作目录的创建
进入到工作目录，比如 D:\workspace\research_agent  
初始化工程：
- 使用命令：uv init backend，创建后端工程
- 进入到工程中，使用vscode/pycharm打开
### 3.安装依赖包
- uv add fastapi
- uv add uvicorn  
写一个简单的hello fastapi程序，测试是否可以运行：  
启动命令：uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
- uv add sqlmodel
- uv add langchain langchain-community
- uv add arxiv langchain-arxiv
