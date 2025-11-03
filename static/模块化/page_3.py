# 3: 计划指标单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group

def page_3():
    st.subheader("3: 计划指标单元")
    
    # 使用侧边栏中设置的用地类型
    land_type = st.session_state.land_type
    
    # 设置默认变量缓存
    defaults = {
        # 用地类型
        '用地类型': st.session_state.land_type,
        '转用总面积': '0.0000',
        '农用地面积': '0.0000',
        '未利用地面积': '0.0000',
        '列入重大项目清单': '否',
        '涉及违法用地': '否',
        '重大项目层级': '',
        '违法总面积': '0.0000',
        '违法农用地': '0.0000',
        '违法未利用地': '0.0000',
        '违法指标来源': '',
        '剩余总面积': '0.0000',
        '剩余农用地': '0.0000',
        '剩余未利用地': '0.0000',
        '县名称': '*县',
        '指标类型': '',
        '使用专项计划': '否',
        '专项指标类型': ''
    }

    # 头部信息（默认折叠）
    with st.expander("文件原文（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处  

        ### 二、审查标准  
        1. 土地利用计划指标安排应符合自然资源部和省自然资源厅年度土地利用计划管理规定。
        
        ### 三、审查内容模板  
        """)
    # 初始化返回结果
    component_result = {}
    
    # 存储每个区块的结果
    all_results = {}
    
    # 根据用地类型分别处理不同区块
    if land_type == '单独选址':
        # 区块1: 土地利用计划
        st.markdown("### 〔土地利用计划〕")
        # 基本信息
        template = '''项目用地符合土地利用计划管理规定。该项目用地中{{转用总面积}}公顷（农用地{{农用地面积}}公顷、未利用地{{未利用地面积}}公顷）需转为建设用地。'''
        
        # 判断是否列入重大项目清单
        列入重大项目清单 = button_group(
            label="",
            options=[{"label": "已列入重大项目清单", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="列入重大项目清单"
        )
        # 更新会话状态
        st.session_state.default_values['列入重大项目清单'] = 列入重大项目清单
        
        # 根据判断结果添加模板内容
        if 列入重大项目清单 == "是":
            # 判断是否涉及违法用地
            涉及违法用地 = button_group(
                label="",
                options=[{"label": "涉及违法用地", "value": "是"}, {"label": "否", "value": "否"}],
                default_value="否",
                key="涉及违法用地"
            )
            st.session_state.default_values['涉及违法用地'] = 涉及违法用地
            
            if 涉及违法用地 == "是":
                template += '''已列入{{重大项目层级}}人民政府重大项目用地清单，因涉及违法用地{{违法总面积}}公顷（农用地{{违法农用地}}公顷、未利用地{{违法未利用地}}公顷），按照年度计划管理文件要求，涉及违法用地的{{违法总面积}}公顷使用{{违法指标来源}}；剩余部分{{剩余总面积}}公顷（农用地{{剩余农用地}}公顷、未利用地{{剩余未利用地}}公顷），申请由国家配置计划。'''
            else:
                template += '''已列入{{重大项目层级}}人民政府重大项目用地清单，申请由国家配置计划。'''
        else:
            template += '''未列入国家重大项目清单和省级人民政府重大项目用地清单，按规定使用{{县名称}}本年度存量土地处置规模为基础核定的{{指标类型}}。'''
        
        all_results['block1'] = lineinput(
            template,
            default_values=st.session_state.default_values.copy(),
            key="page_3_block1"
        )
        
    else:
        # 批次用地模板 - 区块1: 土地利用计划
        st.markdown("### 〔土地利用计划〕")
        # 基本信息
        template = '''该批次用地符合土地利用计划管理规定。批次用地中{{转用总面积}}公顷（农用地{{农用地面积}}公顷、未利用地{{未利用地面积}}公顷）需转为建设用地，'''
        
        # 判断是否使用专项计划
        使用专项计划 = button_group(
            label="",
            options=[{"label": "使用专项计划", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="使用专项计划"
        )
        st.session_state.default_values['使用专项计划'] = 使用专项计划
        
        # 根据判断结果添加模板内容
        if 使用专项计划 == "是":
            template += '''使用{{专项指标类型}}。'''
        else:
            template += '''按规定使用{{县名称}}以本年度存量土地处置规模为基础核定的计划指标。'''
        
        all_results['block1'] = lineinput(
            template,
            default_values=st.session_state.default_values.copy(),
            key="page_3_batch_block1"
        )
        
    # 更新默认值缓存
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 合并所有区块的结果
    for block_result in all_results.values():
        if isinstance(block_result, dict):
            component_result.update(block_result)
    
    return component_result