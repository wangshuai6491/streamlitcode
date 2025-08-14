# 项目介绍
本项目是一个基于streamlit的python项目，已经与最开始的项目“PDFSizeAnalyzer-MCP”大相径庭，刚开始只是简单的给main.py的MCP服务加了个前端界面，后面'发现streamlit打包的特性',又延申了更多的功能，紧接着发现'streamlit cloud'云端免费部署的优劣，又对程序进行了改造，故此，本程序的功能定位越来越混乱，但功能也越来越复杂。


## streamlit打包的特性
由于项目基于streamlit并打包，打包后的exe文件只发挥python解释器的功能，而代码仍然以.py的python文件存在，在程序运行时才读取.py代码并运行，这就允许用户在pages中不断增加新的.py文件，增加新的功能。

## streamlit cloud 云端免费部署的优劣
streamlit cloud 是streamlit官方提供的免费部署服务，用户可以在streamlit cloud上免费部署自己的streamlit项目，但是有一些限制，比如：
1. 必须要有一个github账号。
2. 受云端限制和安全限制，云端的任何程序都是不能操作用户本地电脑的文件（夹）的，这保护了用户的数据安全，但也造成了一些不便。

关于本地文件的操作：程序中有很多对本地文件的操作，如果程序只在本地运行，可以不受影响，但如果运行在云端，则需要考虑下载问题。

我的处理思路是io.BytesIO() 内存缓冲区 + zipfile.ZipFile 生成压缩包 + 把内存缓冲区交给 st.download_button，全程不落盘，直接提供下载结果。

# 项目结构

```
打包后的项目结构/
├── PDF分析和图片处理工具.exe # 启动程序
├── PDF.py # 第一个页面
├── main.py # PDF页面的后端程序，此文件以mcp服务的形式运行，可同时支持AI以MCP方式运行
├── pages/ # 子页面文件夹，每个子页面都是一个.py文件
│   ├── 图片批量旋转与尺寸调整工具.py
│   ├── 开源地址.py
│   ├── 后续新增的其他功能.py
```
## 已打包的模块

hiddenimports=['streamlit', 'streamlit.web.cli', 'streamlit-sortables', 'pandas', 'PIL', 'PyMuPDF', 'fitz', 'fastmcp', 'PyPDF2', 'tkinter', 'tkinter.filedialog', 'tkinter.simpledialog', 'tkinter.messagebox', 'tkinter.commondialog', 'tkinter.colorchooser', 'tkinter.font', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.dnd', 'tkinter.constants', 'tkinter.tix'],


# 本地浏览器使用说明

1. 用streamlit运行PDF.py

```bash
.\venv\Scripts\activate
streamlit run PDF.py --server.port 8501
```

2. 根据运行窗口生成的网址，或自动打开的网址，在浏览器中打开。
3. 上传pdf文件，根据需求点击按钮，结果展示在网页展示，并自动打开结果文件夹。

# pyinsaller打包教程

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

## 图片批量旋转与尺寸调整工具

这是整合了`谢基海`的代码

### 功能

- 批量旋转图片：支持批量旋转图片，用户可以选择旋转角度。
- 批量调整尺寸：支持批量调整图片尺寸，用户可以选择调整宽度和高度。
