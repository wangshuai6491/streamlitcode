import re
from typing import List, Dict, Any, Union
import streamlit as st
import os
import sys
import json,time
# 添加父目录到Python路径，确保可以导入__init__.py中的函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 直接导入__init__.py中的lineinput函数
from __init__ import main

if __name__ == "__main__":
    # 页面标题
    st.title('数据渲染组件')
    # 自定义语法内容
    template = st.text_area("请输入自定义模板语法：", height=300)

    # 只有template不为空时才解析
    if template.strip():
        main(template)