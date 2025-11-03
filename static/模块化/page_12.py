# 12: 地灾评估单元
import streamlit as st
from __init__ import lineinput
def page_12():
    st.subheader("12: 地灾评估单元")
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        地质勘查管理处

        ### 二、审查标准  
        1. 单独选址项目不位于地质灾害易发区的，建设单位不需要对项目进行地质灾害危险性评估。
        2. 单独选址项目位于地质灾害易发区的，建设单位已按规定完成地质灾害危险性评估。
        """)
    
    # 添加判断按钮，让用户选择是否位于地质灾害易发区（横向排列）
    st.subheader("地质灾害危险性评估")
    in_hazard_area = st.radio(
        "是否位于地质灾害易发区：",
        ('是', '否'),
        index=0,  # 默认选择"是"
        horizontal=True  # 横向排列按钮
    )
    
    # 设置默认变量缓存
    defaults = {
        '位于易发区': in_hazard_area,
        '评估资质等级': '甲',
        '评估单位名称': 'XX地质灾害评估公司',
        '评估级别': '一',
        '组织审查单位': 'XX自然资源局',
        '评估结论': '适宜',
        '提出防治工程': '是',
        '已出具承诺书': '是',
        '项目名称': 'XX建设项目'
    }
    
    # 根据用户选择生成相应的模板内容
    if in_hazard_area == '是':
        # 位于易发区的模板
        fixed_template = '''〔地质灾害危险性评估〕该项目建设区位于地质灾害易发区。已由建设项目用地单位书面委托具备地质灾害危险性评估{{ 评估资质等级 }}级资质的{{ 评估单位名称 }}按规定进行了地质灾害危险性评估，评估级别为{{ 评估级别 }}级。评估报告已经{{ 组织审查单位 }}组织有关专家审查通过，评估结论（建设场地适应性评价结论）为{{ 评估结论 }}。评估报告{{ 提出防治工程 === "是" ? '已' : '未' }}提出应配套建设地质灾害防治工程。建设项目用地单位{{ 已出具承诺书 === "是" ? '已' : '未' }}按照地质灾害危险性评估报告中提出的防治措施，作出了具有法律效力的《关于落实{{ 项目名称 }}地质灾害防治措施的承诺书》。'''
    else:
        # 不位于易发区的模板
        fixed_template = '''〔地质灾害危险性评估〕该项目建设区不位于地质灾害易发区。'''

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
        key="page_12_" + in_hazard_area
    )
    return component_result