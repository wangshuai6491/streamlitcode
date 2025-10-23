import streamlit as st
import sys
import os

# 添加父目录到Python路径，这样可以直接导入__init__.py中的函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from __init__ import my_component


st.subheader("测试1")

# 内联式文本输入框组件，将模板中的{{变量}}替换为输入框。
# my_component
# 我们使用特殊的 "key" 参数为此组件实例分配固定身份。默认情况下，当组件参数更改时，
# 它被视为新实例，将在前端重新挂载并丢失当前状态。在此情况下，我们希望在不让其重新创建的前提下改变组件的 "name" 参数。
zfc = "地址是{{*省自治区}}，我的名字是{{姓名}}，今年{{**}}岁，面积{{0.0000}}公顷。"
name_input = st.text_input("name参数", value = zfc)

res = my_component(name_input, key="foo")

if res != "等待用户输入...":
    st.code(res)
