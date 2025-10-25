import streamlit as st
import re
import os
import sys

# 添加父目录到Python路径，确保可以导入__init__.py中的函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入__init__.py中的lineinput函数
from __init__ import lineinput

# 初始化会话状态
def init_session_state():
    # 初始化默认值缓存为空字典，只保留lineinput组件返回的variables
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {}

# 更新会话状态中的变量缓存
def update_variable_cache(component_result):
    # 当组件返回结果且包含更新的变量值时，更新会话状态中的缓存
    if component_result and isinstance(component_result, dict):
        # 检查是否有 'variables' 字段，这应该包含用户在组件中修改的变量值
        if 'variables' in component_result and isinstance(component_result['variables'], dict):
            # 更新会话状态中的默认值缓存
            for var_name, var_value in component_result['variables'].items():
                st.session_state.default_values[var_name] = var_value
            # st.success("已更新会话状态中的变量值缓存")
            return True
    return False


if __name__ == "__main__":
    # 初始化会话状态
    init_session_state()
    
    st.subheader("测试1")

    # 输入模板
    fixed_template = "地址是{{地址}}，{{姓名}}我的名字是{{姓名}}，今年{{年龄}}岁，面积{{面积}}公顷。"
    # 设置默认变量缓存
    defaults = {'地址': '**省', '姓名': '王帅', '年龄': 18, '面积': 100}
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 显示当前使用的模板
    st.write("当前使用的模板:")
    st.code(fixed_template)

    # 调用组件，传递模板和默认值字典（确保使用最新的会话状态值）
    component_result = lineinput(
        fixed_template, 
        default_values=st.session_state.default_values.copy(),  # 创建副本以确保使用最新值
        key="foo"
    )
    # 调用函数更新变量缓存
    update_variable_cache(component_result)
    
    # 显示组件返回的结果
    st.subheader("组件返回结果")
    if component_result and component_result.get('content') != "等待用户输入...":
        st.write("### 拼接后文本")
        st.code(component_result['content'])
        
        st.write("### 变量值字典")
        st.json(component_result['variables'])
    else:
        st.write("等待用户输入...")

    # 可选：添加会话状态信息显示，方便调试
    if st.checkbox("显示会话状态信息"):
        st.write("### 会话状态详情")
        st.write("当前缓存:", st.session_state.default_values)