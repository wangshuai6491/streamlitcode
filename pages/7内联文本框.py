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

# 13: 信访处理模板
def page_13():
    st.subheader("标签13: 信访处理模板")
    
    # 添加判断按钮，让用户选择是否发生信访（横向排列）
    st.subheader("信访状态选择")
    has_letter = st.radio(
        "是否发生信访?",
        ('是', '否'),
        index=1,  # 默认选择"否"
        horizontal=True  # 横向排列按钮
    )
    
    # 设置默认变量缓存
    defaults = {
        '是否发生信访': has_letter,
        '信访年份': '2024',
        '信访月份': '6',
        '信访县': 'XX',
        '信访乡': 'XX',
        '信访村': 'XX',
        '信访人姓名': '张三',
        '信访反映具体内容': '相关问题',
        '受理自然资源主管部门': 'XX自然资源局',
        '处理具体措施': '已采取相应措施'
    }
    
    # 根据用户选择生成相应的模板内容
    if has_letter == '是':
        # 发生信访的模板
        fixed_template = "〔信访处理〕 {{ 信访年份 }}年{{ 信访月份 }}月，{{ 信访县 }}县{{ 信访乡 }}乡{{ 信访村 }}村村民{{ 信访人姓名 }}来信（访）反映该批次拟占地块{{ 信访反映具体内容 }}。{{ 受理自然资源主管部门 }}进行了认真调查处理，{{ 处理具体措施 }}。目前，信访群众反映的问题已得到妥善解决，信访人表示不再上访。"
    else:
        # 未发生信访的模板
        fixed_template = "〔信访处理〕 该批次用地截至目前未收到相关信访事项。"

    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)

    # 调用组件，传递模板和默认值字典（确保使用最新的会话状态值）
    component_result = lineinput(
        fixed_template, 
        default_values=st.session_state.default_values.copy(),  # 创建副本以确保使用最新值
        key="page_13_" + has_letter  # 使用不同的key以确保在切换选项时重新渲染组件
    )
    return component_result

# 主应用逻辑
if __name__ == "__main__":
    # 初始化会话状态
    init_session_state()
    
    # 增加侧边栏导航
    st.sidebar.title("模块单元")
    page = st.sidebar.selectbox(
        "选择模块",
        ["标签13: 信访处理模板", "测试1"],
        index=0  # 默认选中标签13
    )

    if page == "标签13: 信访处理模板":
        component_result = page_13()
        st.write(component_result['content'])
        # 调用函数更新变量缓存
        update_variable_cache(component_result)
    
    # 把缓存显示放到最后就能确保刷新
    with st.sidebar.expander("当前缓存", expanded=False):
        st.write(st.session_state.default_values)