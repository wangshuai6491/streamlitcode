# 1: 基本情况单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group

def page_1():
    st.subheader("1: 基本情况单元")
    
    # 使用侧边栏中设置的用地类型
    land_type = st.session_state.land_type
    
    # 设置默认变量缓存
    defaults = {
        # 用地类型
        '用地类型': st.session_state.land_type,
        '预审通过年月': '*年*月',
        '预审自然资源主管部门': '*省自然资源厅',
        '预审文号': 'XX预审〔202X〕XX号',
        '用地面积': '0.0000'
    }

    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处  

        ### 二、审查标准  
        1. 符合基本建设投资管理规定。  
        2. 建设单位已取得建设项目批准（核准或备案）文件、初步设计批准或审核文件，且应当在有效期内。  
        3. 用地涉及的新增建设用地应按规定缴纳新增建设用地土地有偿使用费，缴纳等级、标准应准确。  
        4. 1999 年 1 月 1 日之后经依法批准的集体建设用地，在批准农用地转用时未缴纳新增建设用地有偿使用费的，申请土地征收时按照现行标准补缴。  

        ### 三、审查内容模板  
        """)
    # 初始化返回结果
    component_result = {}
    
    # 存储每个区块的结果
    all_results = {}
    
    # 根据用地类型分别处理不同区块
    if land_type == '单独选址':
        # 区块1: 用地预审情况
        st.markdown("### 〔用地预审情况〕")
        # 判断区域
        审批权下放 = button_group(
            label="",
            options=[{"label": "是", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="审批权下放"
        )
        # 根据判断结果生成不同的模板
        if 审批权下放 == "是":
            block1_template = '''该项目符合基本建设投资管理规定。按照{{ 下放依据 }}规定，{{ 审批权下放部门 }}，{{ 预审通过年月 }}，该项目通过{{ 预审自然资源主管部门 }}用地预审（文号：{{ 预审文号 }}）。'''
        else:
            block1_template = '''该项目符合基本建设投资管理规定。{{ 预审通过年月 }}通过{{ 预审自然资源主管部门 }}用地预审（文号：{{ 预审文号 }}）。'''
        all_results['block1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block1"
        )
        
        # 区块2: 可研批复情况
        st.markdown("### 〔可研批复情况〕")
        # 判断条件
        col1, col2, col3 = st.columns(3)

        with col1:
            _2024以后通过预审 = button_group(
                label="",
                options=[{"label": "否", "value": "否"}, {"label": "是", "value": "是"}],
                default_value="否",
                key="_2024以后通过预审"
            )
            st.session_state.default_values['2024以后通过预审'] = _2024以后通过预审

        with col2:
            用地预审在可研之后 = button_group(
                label="",
                options=[{"label": "否", "value": "否"}, {"label": "是", "value": "是"}],
                default_value="否",
                key="用地预审在可研之后"
            )
            st.session_state.default_values['用地预审在可研之后'] = 用地预审在可研之后

        with col3:
            可研变更 = button_group(
                label="",
                options=[{"label": "否", "value": "否"}, {"label": "是", "value": "是"}],
                default_value="否",
                key="可研变更"
            )
            st.session_state.default_values['可研变更'] = 可研变更
        核准超期 = button_group(
            label="",
            options=[
                {"label": "未超期", "value": "未超期"},
                {"label": "项目核准文件超出有效期但项目单位在核准有效期内提出用地申请", "value": "项目核准文件超出有效期但项目单位在核准有效期内提出用地申请"},
                {"label": "项目超出核准有效期但已获得原批准机关核准延期批复", "value": "项目超出核准有效期但已获得原批准机关核准延期批复"},
                {"label": "项目超出核准有效期但已获得原批准机关核准延期说明", "value": "项目超出核准有效期但已获得原批准机关核准延期说明"}
            ],
            default_value="未超期",
            key="核准超期"
        )
        st.session_state.default_values['核准超期'] = 核准超期

        
        # 根据判断结果生成不同的模板
        block2_template = '''{{ 可研批复年月 }}，{{ 可研批复部门 }}（文号：{{ 可研批复文号 }}）。'''
        
        # 添加附加内容
        if _2024以后通过预审 == "是":
            block2_template += '''可行性研究报告（或项目申请报告）已包含用地预审审查后的节约集约用地专章相关内容。'''
        if 用地预审在可研之后 == "是":
            block2_template += '''{{ 投资主管部门 }}已出具书面说明并检讨。'''
        if 核准超期 == "项目核准文件超出有效期但项目单位在核准有效期内提出用地申请":
            block2_template += '''项目核准文件超出有效期，但项目单位在核准有效期内提出用地申请。'''
        elif 核准超期 == "项目超出核准有效期但已获得原批准机关核准延期批复":
            block2_template += '''项目超出核准有效期，但已获得原批准机关核准延期批复。'''
        elif 核准超期 == "项目超出核准有效期但已获得原批准机关核准延期说明":
            block2_template += '''项目超出核准有效期，但已获得原批准机关核准延期说明。'''
        if 可研变更 == "是":
            block2_template += '''{{ 可研变更批复年月 }}，{{ 可研变更批复部门 }}（文号：{{ 可研变更文号 }}）。'''
        
        all_results['block2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block2"
        )
        
    else:
        # 批次用地模板 - 区块1: 基本情况
        st.markdown("### 〔基本情况〕")
        # 判断区域
        有无可调整地类 = button_group(
            label="",
            options=[{"label": "有可调整地类", "value": "是"}, {"label": "无可调整地类", "value": "否"}],
            default_value="是",
            key="有无可调整地类"
        )

        # 根据判断结果生成不同的模板
        if 有无可调整地类 == "是":
            block1_template = '''该批次实际申请用地情况为：总面积{{总面积}}公顷，其中：农用地{{农用地面积}}公顷（耕地{{耕地面积}}公顷）、建设用地{{建设用地面积}}公顷、未利用地{{未利用地面积}}公顷。'''
        else:
            block1_template = '''该批次实际申请用地情况为：总面积{{总面积}}公顷，其中：农用地{{农用地面积}}公顷（耕地{{耕地面积}}公顷；可调整地类{{可调整地类面积}}公顷）、建设用地{{建设用地面积}}公顷、未利用地{{未利用地面积}}公顷。'''
        all_results['block1_1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_batch_block1"
        )
        block1_template2 = '''按权属和地类分：农民集体所有土地{{集体土地总面积}}公顷，其中：农用地{{集体农用地}}公顷（耕地{{集体耕地}}公顷）、建设用地{{集体建设用地}}公顷、未利用地{{集体未利用地}}公顷；国有土地{{国有土地总面积}}公顷，其中：农用地{{国有农用地}}公顷（耕地{{国有耕地}}公顷）、建设用地{{国有建设用地}}公顷、未利用地{{国有未利用地}}公顷，地类和面积准确。'''
        all_results['block1_2'] = lineinput(
            block1_template2,
            default_values=st.session_state.default_values.copy(),
            key="page_1_batch_block1_2"
        )
        
    # 更新默认值缓存
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 合并所有区块的结果
    for block_result in all_results.values():
        if isinstance(block_result, dict):
            component_result.update(block_result)
    
    return component_result
