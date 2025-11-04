# 2: 审核许可单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group

def page_2():
    st.subheader("2: 审核许可单元")
    
    # 使用侧边栏中设置的用地类型
    land_type = st.session_state.land_type
    
    # 设置默认变量缓存
    defaults = {
        # 单独选址默认值
        "涉及占用林地": "否",
        "占用林地面积": "0.0000",
        "林地手续文号": "XX林地审核同意书〔202X〕XX号",
        "采矿许可年月": "*年*月",
        "核发部门": "*省自然资源厅",
        "矿种": "**矿",
        "采矿许可证证号": "",
        "涉及保护地": "否",
        "保护地名称": "*保护地",
        "保护地面积": "0.0000",
        "保护地主管部门": "*省林业局",
        "保护地同意文号": "XX保护地同意书〔202X〕XX号",
        # 批次用地默认值
        "涉及林地": "否",
        "林地面积": "0.0000",
        "林地审核状态": "已获批",
        "林草部门": "*省林业局"
    }

    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处  

        ### 二、审查标准  
        1. 涉及占用林地的，应当取得使用林地审核同意书，且应当在有效期内。涉及占用各类保护地的，需取得相关主管部门同意的意见。  
        2. 采矿用地需取得采矿许可证。  

        ### 三、审查内容模板  
        """)
    # 初始化返回结果
    component_result = {}
    
    # 存储每个区块的结果
    all_results = {}
    
    # 根据用地类型分别处理不同区块
    if land_type == '单独选址':
        # 区块1: 有关审核许可手续
        st.markdown("### 〔有关审核许可手续〕")
        # 判断区域
        涉及占用林地 = button_group(
            label="",
            options=[{"label": "涉及占用林地", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="涉及占用林地"
        )
        # 更新会话状态
        st.session_state.default_values['涉及占用林地'] = 涉及占用林地
        # 根据判断结果生成不同的模板
        if 涉及占用林地 == "是":
            block1_template = '''项目涉及占用林草部门管理范围内林地{{ 占用林地面积 }}公顷，已按要求办理林地相关手续（文号：{{ 林地手续文号 }}）。'''  
        else:
            block1_template = '''项目不涉及占用林草部门管理范围内林地。'''  
        all_results['block1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_2_block1"
        )
        
        # 区块2: 采矿许可证信息
        st.markdown("### 〔采矿许可证信息〕")
        block2_template = '''建设单位已于{{ 采矿许可年月 }}取得{{ 核发部门 }}核发的{{ 矿种 }}采矿许可证（证号：{{ 采矿许可证证号 }}）。'''  
        all_results['block2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_2_block2"
        )
        
        # 区块3: 保护地情况
        st.markdown("### 〔保护地情况〕")
        涉及保护地 = button_group(
            label="",
            options=[{"label": "涉及保护地", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="涉及保护地"
        )
        st.session_state.default_values['涉及保护地'] = 涉及保护地
        if 涉及保护地 == "是":
            block3_template = '''项目用地涉及{{ 保护地名称 }}，面积{{ 保护地面积 }}公顷，已取得{{ 保护地主管部门 }}同意的意见（文号：{{ 保护地同意文号 }}）。'''  
        else:
            block3_template = '''项目用地不涉及各类保护地。'''  
        all_results['block3'] = lineinput(
            block3_template,
            default_values=st.session_state.default_values.copy(),
            key="page_2_block3"
        )
        
    else:
        # 批次用地模板 - 区块1: 林地审核情况
        st.markdown("### 〔林地审核情况〕")
        # 判断区域
        涉及林地 = button_group(
            label="",
            options=[{"label": "涉及林地", "value": "是"}, {"label": "不涉及", "value": "否"}],
            default_value="否",
            key="涉及林地"
        )
        # 更新会话状态
        st.session_state.default_values['涉及林地'] = 涉及林地
        # 根据判断结果生成不同的模板
        if 涉及林地 == "是":
            林地审核状态 = button_group(
                label="",
                options=[{"label": "已获批", "value": "已获批"}, {"label": "正在办理", "value": "正在办理"}],
                default_value="已获批",
                key="林地审核状态"
            )
            st.session_state.default_values['林地审核状态'] = 林地审核状态
            if 林地审核状态 == "已获批":
                block1_template = '''该批次用地涉及林地{{ 林地面积 }}公顷，已取得{{ 林草部门 }}《林地审核同意书》。'''  
            else:
                block1_template = '''该批次用地涉及林地{{ 林地面积 }}公顷，相关材料已报{{ 林草部门 }}待批，我局承诺在用地上报省政府前补充《林地审核同意书》。'''  
        else:
            block1_template = '''该批次不涉及占用林草部门管理范围内林地。'''  
        all_results['block1_1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_2_batch_block1"
        )
        
        # 区块2: 保护地情况
        st.markdown("### 〔保护地情况〕")
        批次涉及保护地 = button_group(
            label="",
            options=[{"label": "涉及保护地", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="批次涉及保护地"
        )
        st.session_state.default_values['批次涉及保护地'] = 批次涉及保护地
        if 批次涉及保护地 == "是":
            block2_template = '''项目用地涉及{{ 保护地名称 }}，面积{{ 保护地面积 }}公顷，已取得{{ 保护地主管部门 }}同意的意见（文号：{{ 保护地同意文号 }}）。'''  
        else:
            block2_template = '''项目用地不涉及各类保护地。'''  
        all_results['block1_2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_2_batch_block2"
        )
        
    # 更新默认值缓存
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 合并所有区块的结果
    for block_result in all_results.values():
        if isinstance(block_result, dict):
            component_result.update(block_result)
    
    return component_result