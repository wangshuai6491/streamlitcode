# 9: 古树名木和历史文化保护单元
import streamlit as st
from __init__ import lineinput
def page_9():
    st.subheader("9: 古树名木和历史文化保护单元")
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        自然保护地管理处、历史文化保护处

        ### 二、审查标准  
        1. 项目用地应避让古树名木、历史文化名镇名村、传统村落、文物保护单位等。
        2. 确实无法避让的，应按规定取得相关主管部门同意意见。
        """)
    
    # 添加判断按钮，让用户选择是否涉及古树名木和历史文化保护（横向排列）
    st.subheader("古树名木和历史文化保护")
    has_protection = st.radio(
        "是否涉及古树名木和历史文化保护：",
        ('否', '是'),
        index=0,  # 默认选择"否"
        horizontal=True  # 横向排列按钮
    )
    
    # 如果选择涉及，再询问具体类型
    protection_type = None
    if has_protection == '是':
        protection_type = st.radio(
            "涉及类型：",
            ('古树名木', '历史文化名镇名村', '传统村落', '文物保护单位', '其他'),
            index=0,  # 默认选择"古树名木"
            horizontal=True  # 横向排列按钮
        )
    
    # 设置默认变量缓存
    defaults = {
        '是否涉及': has_protection,
        '涉及类型': protection_type,
        '古树名木数量': '0',
        '古树名木等级': '三级',
        '保护方案批准部门': 'XX林业局',
        '历史文化名称': 'XX历史文化名镇',
        '文物保护单位级别': '省级',
        '文物保护单位名称': 'XX文物保护单位',
        '审批部门': 'XX文物局',
        '批复文号': 'XX文物[2025]XX号'
    }
    
    # 根据用户选择生成相应的模板内容
    if has_protection == '否':
        # 不涉及的模板
        fixed_template = '''〔古树名木和历史文化保护〕该项目不涉及古树名木和历史文化保护问题。经核查，项目用地范围内无古树名木、历史文化名镇名村、传统村落、文物保护单位等。'''  
    else:
        # 涉及的模板
        if protection_type == '古树名木':
            fixed_template = '''〔古树名木和历史文化保护〕该项目涉及{{ 古树名木数量 }}株{{ 古树名木等级 }}古树名木，已取得{{ 保护方案批准部门 }}同意的保护方案。建设单位将严格按照保护方案进行施工，确保古树名木安全。'''  
        elif protection_type == '历史文化名镇名村':
            fixed_template = '''〔古树名木和历史文化保护〕该项目涉及{{ 历史文化名称 }}，已取得相关主管部门同意意见，项目建设符合历史文化名镇名村保护规划要求。'''  
        elif protection_type == '传统村落':
            fixed_template = '''〔古树名木和历史文化保护〕该项目涉及{{ 历史文化名称 }}（传统村落），已取得相关主管部门同意意见，项目建设符合传统村落保护要求。'''  
        elif protection_type == '文物保护单位':
            fixed_template = '''〔古树名木和历史文化保护〕该项目涉及{{ 文物保护单位级别 }}文物保护单位{{ 文物保护单位名称 }}，已取得{{ 审批部门 }}出具的同意意见（文号：{{ 批复文号 }}）。'''  
        else:
            fixed_template = '''〔古树名木和历史文化保护〕该项目涉及其他历史文化保护对象，已取得相关主管部门同意意见，项目建设符合保护要求。'''  

    # 确保session_state中存在default_values字典
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {}
    
    # 更新默认值到session_state
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)

    # 生成唯一的key
    key_suffix = has_protection
    if protection_type:
        key_suffix += "_" + protection_type

    # 调用组件，传递模板和默认值字典
    component_result = lineinput(
        fixed_template, 
        default_values=st.session_state.default_values.copy(),
        key="page_9_" + key_suffix
    )
    return component_result