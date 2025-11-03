# 11: 压矿情况单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group
def page_11():
    st.subheader("11: 压矿情况单元")
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        矿产资源保护监督处、行政审批管理处

        ### 二、审查标准  
        1. 单独选址项目应核实是否压覆重要矿产资源。
        2. 单独选址项目压覆重要矿产资源的，应取得同意压覆的意见。
        3. 单独选址项目压覆重要矿产资源的，按规定组织安全论证，且结论为项目建设不影响矿产资源合理开采利用的，不做压覆处理。
        """)
    
    # 添加判断按钮，让用户选择压覆情形（横向排列）
    st.subheader("压矿情况单元不区分单选和批次，用的是同一套模板")
    mineral_case = button_group(
        "",
        options=[{"label": "不压覆", "value": "不压覆"}, 
                 {"label": "影响但不作压覆处理", "value": "影响但不作压覆处理"}, 
                 {"label": "已办审批", "value": "已办审批"}],
        default_value="不压覆",
        key="mineral_case_select"
    )
    
    # 设置默认变量缓存
    defaults = {
        '压覆情形': mineral_case,
        '压覆矿种': '煤、铁等',
        '压覆矿业权名称': 'XX矿业权',
        '审批自然资源主管部门': 'XX自然资源厅'
    }
    
    # 根据用户选择生成相应的模板内容
    if mineral_case == '不压覆':
        # 不压覆的模板
        fixed_template = '''〔压覆重要矿产资源审批情况〕①该项目不压覆重要矿产资源。'''
    elif mineral_case == '影响但不作压覆处理':
        # 影响但不作压覆处理的模板
        fixed_template = '''〔压覆重要矿产资源审批情况〕②该项目涉及压覆{{ 压覆矿种 }}等重要矿产资源，经项目所在市、县（市、区）人民政府牵头组织安全论证，结论为项目建设不影响矿产资源合理开采利用，不作压覆处理（项目压覆{{ 压覆矿业权名称 }}矿业权，已签订互不影响协议）。'''
    else:
        # 已办审批的模板
        fixed_template = '''〔压覆重要矿产资源审批情况〕③该项目涉及压覆{{ 压覆矿种 }}等重要矿产资源，建设单位已按规定办理压覆矿产资源审批手续，{{ 审批自然资源主管部门 }}同意压覆上述重要矿产资源。'''

    # 确保session_state中存在default_values字典
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {}
    
    # 更新默认值到session_state
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)

    # 调用组件，传递模板和默认值字典
    component_result = lineinput(
        fixed_template, 
        default_values=st.session_state.default_values.copy(),
        key="page_11_" + mineral_case
    )
    return component_result