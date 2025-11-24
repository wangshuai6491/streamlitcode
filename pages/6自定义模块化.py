import re
from typing import List, Dict, Any, Union
import streamlit as st
import os
import sys
import json,time
# 添加父目录到Python路径，确保可以导入__init__.py中的函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 直接导入__init__.py中的lineinput函数
from __init__ import parse_and_render, setup_sidebar


if __name__ == "__main__":
    # 配置侧边栏
    setup_sidebar()
    # 自定义语法内容
    # template = st.sidebar.text_area("请输入自定义模板语法：", height=300)
    template = """
 {% radio 批次类型 %}
普通批次|增减挂钩批次
{% endradio %}
{% toggle 分次报批 %}
{% endtoggle %}

{% if 批次类型 = "普通批次" %} 
该批次申请将农用地{{转用农用地|default:0.0000}}公顷（耕地{{转用耕地|default:0.0000}}公顷）、未利用地{{转用未利用地|default:0.0000}}公顷转为建设用地，其中：农民集体所有农用地{{集体转用农用地|default:0.0000}}公顷（耕地{{集体转用耕地|default:0.0000}}公顷）、未利用地{{集体转用未利用地|default:0.0000}}公顷；国有农用地{{国有转用农用地|default:0.0000}}公顷（耕地{{国有转用耕地|default:0.0000}}公顷）、未利用地{{国有转用未利用地|default:0.0000}}公顷。 
{% else %} 
该批次使用{{指标来源|default:*县自产}}{{挂钩指标面积|default:0.0000}}公顷，其中水田{{挂钩水田|default:0.0000}}公顷，标准粮食产能{{挂钩产能|default:0}}公斤； 
{% endif %} 

{% if 分次报批 %} 
建新区拟使用土地{{新区拟用面积|default:0.0000}}公顷，其中水田{{新区水田|default:0.0000}}公顷，标准粮食产能{{新区产能|default:0}}公斤。建新区土地已全部转为建设用地。 
{% else %} 
建新区已使用{{已用面积|default:0.0000}}公顷，其中水田{{已用水田|default:0.0000}}公顷，标准粮食产能{{已用产能|default:0}}公斤；本次报批{{本次报批面积|default:0.0000}}公顷，其中水田{{本次水田|default:0.0000}}公顷，标准粮食产能{{本次产能|default:0}}公斤；剩余{{剩余面积|default:0.0000}}公顷，其中水田{{剩余水田|default:0.0000}}公顷，标准粮食产能{{剩余产能|default:0}}公斤。建新区土地已全部转为建设用地。 
{% endif %}
"""

    # 只有template不为空时才解析
    if template.strip():
        # 解析并渲染自定义模板，返回结果存入session_state
        parse_and_render(template)

    # 可选：在页面上展示解析后的结果（调试用）
    st.write(st.session_state)