# 项目介绍
本项目是一个基于streamlit的python项目，主要部署在云端，用户可以在浏览器中直接使用。
注意：
1. 本项目主要部署在streamlit cloud上，用户可以在浏览器中直接使用https://wangshuai.streamlit.app/。
2. 本项目的代码是开源的，用户可以在github上查看和修改代码。
3. github限制单个文件大小为100MB。

## streamlit打包的特性
由于项目基于streamlit并打包，打包后的exe文件只发挥python解释器的功能，而代码仍然以.py的python文件存在，在程序运行时才读取.py代码并运行，这就允许用户在pages中不断增加新的.py文件，增加新的功能。

## streamlit cloud 云端免费部署的优劣
streamlit cloud 是streamlit官方提供的免费部署服务，用户可以在streamlit cloud上免费部署自己的streamlit项目，但是有一些限制，比如：
1. 必须要有一个github账号。
2. 受云端限制和安全限制，云端的任何程序都是不能操作用户本地电脑的文件（夹）的，这保护了用户的数据安全，但也造成了一些不便。

关于本地文件的操作：程序中有很多对本地文件的操作，如果程序只在本地运行，可以不受影响，但如果运行在云端，则需要考虑下载问题。

我的处理思路是io.BytesIO() 内存缓冲区 + zipfile.ZipFile 生成压缩包 + 把内存缓冲区交给 st.download_button，全程不落盘，直接提供下载结果。


# 本地浏览器使用说明

1. 用streamlit运行PDF.py

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
streamlit run PDF.py
```

2. 根据运行窗口生成的网址，或自动打开的网址，在浏览器中打开。
3. 上传pdf文件，根据需求点击按钮，结果展示在网页展示，并自动打开结果文件夹。

# pyinsaller打包教程

按操作执行：'如果需要打包，就把此文件夹中的内容放到项目根目录'文件夹下的内容移到根目录

1. 激活虚拟环境

```bash
.\venv\Scripts\activate
```

2. 用spec打包，注意打包streamlit有点不同：

需要额外的run_app.py文件，需要特定的文件夹hooks，这个文件夹内还需要特定的hook-streamlit.py。
当然这些文件的内容都是固定的，不需要自己修改。

有了上面的基础，就可以打包了。注意修改run_app.spec中datas的文件夹路径

```bash
pyinstaller run_app.spec
```

3. 打包完成后，在 dist 目录下会生成一个可执行文件,但这个执行文件无法运行，还需要把依赖的py文件复制到dist目录下。
   本项目中是：
   PDF.py # 前端主程序
   main.py # 后端主程序
   pages/子页面的py文件 # 子页面的py文件

## 注意事项

- 确保使用的是虚拟环境中的 Python 解释器，涉及到依赖问题。
- 先用纯英文目录测试，成功后再测试中文目录。

# 主页面PDF.py

主要是'PDFSizeAnalyzer-MCP'的前端页面。

关于MCP服务的说明，请看[mcp服务只用这个文件夹内容即可]文件夹下的说明.md文件。

在云端环境下，也就是本项目根目录的PDF.py文件中，只保留用前端js无法实现的章节信息提取功能。

在本地环境下，也就是本项目打包后的项目exe文件夹下的PDF.py文件中，保留了所有的功能。


# pages中的子页面

## 网易云音乐功能

- 单曲下载
- 歌单下载

## 酷匠网小说功能

- 小说下载

## 高德地图

- 坐标转换

## 网站导航

- 导航






