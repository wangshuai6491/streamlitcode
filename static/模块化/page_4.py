# 4: 土地预审单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group

def page_4():
    st.subheader("4: 土地预审单元")
    
    # 使用侧边栏中设置的用地类型
    land_type = st.session_state.land_type
    
    # 设置默认变量缓存
    defaults = {
        "审批权是否下放": "否",
        "下放依据文件": "",
        "审批权下放部门": "",
        "预审通过年月": "*年*月",
        "预审自然资源主管部门": "*省自然资源厅",
        "预审文号": "XX预审〔202X〕XX号",
        "占用永久基本农田且由省级自然资源主管部门预审": "否",
        "立项与预审层级一致": "是",
        "申报用地与预审控制用地规模": "一致",
        "贫困地区类型": "",
        "预审层级": "",
        "不一致原因": "",
        "预审总面积": "0.0000",
        "预审农用地": "0.0000",
        "预审耕地": "0.0000",
        "预审永农": "0.0000",
        "超出原因": "",
        "超出面积": "0.0000",
        "超出农用地": "0.0000",
        "超出耕地": "0.0000",
        "超出永农": "0.0000",
        "超出比例": "0",
        "范围重合度": "100"
    }

    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        行政审批管理处、国土空间用途管制处  

        ### 二、审查标准  
        1. 已按规定通过用地预审，预审层级应符合要求，应在预审批准后且有效期内批复可研报告或核准项目。  
        2. 重新预审的符合有关规定。  
        3. 用地规模和用地预审控制规模比对情况应符合有关要求。  

        ### 三、审查内容模板  
        *土地预审单元不区分单选和批次，用的是同一套模板*
        """)
    
    # 初始化返回结果
    component_result = {}
    
    # 存储每个区块的结果
    all_results = {}
    
    # 土地预审单元不区分用地类型，使用统一处理逻辑
    # 区块1: 用地预审情况
    st.markdown("### 〔用地预审情况〕")
    # 判断区域
    审批权是否下放 = button_group(
        label="",
        options=[{"label": "审批权下放", "value": "是"}, {"label": "否", "value": "否"}],
        default_value="否",
        key="审批权是否下放"
    )
    # 更新会话状态
    st.session_state.default_values['审批权是否下放'] = 审批权是否下放
    
    # 根据判断结果生成不同的模板
    if 审批权是否下放 == "是":
        block1_template = '''该项目符合基本建设投资管理规定。按照{{下放依据文件}}规定，{{审批权下放部门}}办理，{{预审通过年月}}，该项目通过{{预审自然资源主管部门}}用地预审({{预审文号}})。'''  
    else:
        block1_template = '''该项目符合基本建设投资管理规定。{{预审通过年月}}，{{预审自然资源主管部门}}通过用地预审（文号：{{预审文号}}）。'''  
    
    all_results['block1'] = lineinput(
        block1_template,
        default_values=st.session_state.default_values.copy(),
        key="page_4_block1"
    )
    
    # 区块2: 落实预审意见
    st.markdown("### 〔落实预审意见〕")
    
    # 判断条件

    占用永久基本农田且由省级自然资源主管部门预审 = button_group(
        label="",
        options=[{"label": "占用永久基本农田且由省级自然资源主管部门预审", "value": "是"}, {"label": "否", "value": "否"}],
        default_value="否",
        key="占用永久基本农田且由省级自然资源主管部门预审"
    )

    立项与预审层级一致 = button_group(
        label="",
        options=[{"label": "立项与预审层级一致", "value": "是"}, {"label": "否", "value": "否"}],
        default_value="是",
        key="立项与预审层级一致"
    )

    申报用地与预审控制用地规模 = button_group(
        label="申报用地与预审控制用地规模",
        options=[{"label": "一致", "value": "一致"}, {"label": "基本一致", "value": "基本一致"}, {"label": "超出规模", "value": "超出规模"}],
        default_value="一致",
        key="申报用地与预审控制用地规模"
    )
    st.session_state.default_values['申报用地与预审控制用地规模'] = 申报用地与预审控制用地规模
    
    # 根据判断结果生成不同的模板
    # 第一部分：预审层级信息
    if 占用永久基本农田且由省级自然资源主管部门预审 == "是":
        block2_part1 = '''该项目属于{{贫困地区类型}}，符合占用永久基本农田条件，由省级自然资源主管部门通过预审。'''  
    else:
        block2_part1 = '''该项目由{{预审层级}}自然资源主管部门通过预审，'''  
    
    # 第二部分：立项与预审层级一致性
    if 立项与预审层级一致 == "是":
        block2_part2 = '''与批准项目立项政府部门层级一致，用地预审层级符合有关规定。'''  
    else:
        block2_part2 = '''立项与预审层级不一致，具体原因：{{不一致原因}}'''  
    
    # 第三部分：预审控制规模信息
    block2_part3 = '''项目用地预审控制规模{{预审总面积}}公顷，其中农用地{{预审农用地}}公顷（耕地{{预审耕地}}公顷、永久基本农田{{预审永农}}公顷），'''  
    
    # 第四部分：申报用地与预审控制用地规模比较
    if 申报用地与预审控制用地规模 == "一致":
        block2_part4 = '''申报用地与预审控制用地规模一致。'''  
    elif 申报用地与预审控制用地规模 == "基本一致":
        block2_part4 = '''申报用地与预审控制用地规模基本一致。'''  
    else:  # 超出规模
        block2_part4 = '''因{{超出原因}}，申报用地超出预审控制规模{{超出面积}}公顷，其中农用地{{超出农用地}}公顷（含耕地{{超出耕地}}公顷、永久基本农田{{超出永农}}公顷）。超出比例：{{超出比例}}%，范围重合度：{{范围重合度}}%'''  
        
        # 尝试获取超出比例和范围重合度，添加特殊说明
        try:
            超出比例 = float(st.session_state.default_values.get('超出比例', '0'))
            范围重合度 = float(st.session_state.default_values.get('范围重合度', '100'))
            if 超出比例 >= 10 or 范围重合度 < 80:
                block2_part4 += '''（建设项目申请总面积超出用地预审总面积达到10%且范围重合度低于80%，需对用地变化情况的必要性、合理性作出说明。）'''  
        except:
            pass
    
    # 合并所有部分
    block2_template = block2_part1 + "\n" + block2_part2 + "\n" + block2_part3 + "\n" + block2_part4
    
    all_results['block2'] = lineinput(
        block2_template,
        default_values=st.session_state.default_values.copy(),
        key="page_4_block2"
    )
    
    # 更新默认值缓存
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 合并所有区块的结果
    for block_result in all_results.values():
        if isinstance(block_result, dict):
            component_result.update(block_result)
    
    return component_result