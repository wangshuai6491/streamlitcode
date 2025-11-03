# 13: 信访情况单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group
def page_13():
    st.subheader("13: 信访情况单元")
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        办公室

        ### 二、审查标准  
        存在的信访问题已妥善解决。
        """)
    
    # 添加判断按钮，让用户选择是否发生信访（横向排列）
    custom_options = [
        {"label": "有信访", "value": "是"},
        {"label": "无信访", "value": "否"}
    ]
    has_letter = button_group("",custom_options,"否",key="has_letter_selection")
    
    # 设置默认变量缓存
    defaults = {
        '是否发生信访': has_letter,
        '信访年月': '2025年6月',
        '信访县乡村': 'XX县XX乡XX村',
        '信访人姓名': '张三',
        '信访反映具体内容': '信访反映具体内容',
        '受理自然资源主管部门': 'XX自然资源局',
        '处理具体措施': '处理具体措施'
    }
    
    # 根据用户选择生成相应的模板内容
    if has_letter == '是':
        # 发生信访的模板
        fixed_template = '''〔信访处理〕 {{ 信访年月 }}，{{ 信访县乡村 }}村民{{ 信访人姓名 }}来信（访）反映该批次拟占地块{{ 信访反映具体内容 }}。{{ 受理自然资源主管部门 }}进行了认真调查处理，{{ 处理具体措施 }}。目前，信访群众反映的问题已得到妥善解决，信访人表示不再上访。'''
    else:
        # 未发生信访的模板
        fixed_template = '''〔信访处理〕 该批次用地截至目前未收到相关信访事项。'''

    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)

    # 调用组件，传递模板和默认值字典（确保使用最新的会话状态值）
    component_result = lineinput(
        fixed_template, 
        default_values=st.session_state.default_values.copy(),  # 创建副本以确保使用最新值
        key="page_13_" + has_letter  # 使用不同的key以确保在切换选项时重新渲染组件
    )
    return component_result
