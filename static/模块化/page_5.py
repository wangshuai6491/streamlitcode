# 5: 权属地类单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group

def page_5():
    st.subheader("5: 权属地类单元")
    
    # 使用侧边栏中设置的用地类型
    land_type = st.session_state.land_type
    
    # 设置默认变量缓存
    defaults = {
        # 基础信息
        "涉及县列表": "",
        "乡镇数": "",
        "村数": "",
        "国有单位数": "",
        "宗地总数": "",
        "已发证宗地数": "",
        "未发证宗地数": "",
        "未发证原因及权利人意见": "",
        "权属数据库一致": "是",
        "不一致图斑数": "",
        "不一致面积": "0.0000",
        "图斑权属单位": "",
        "图斑权属性质": "",
        "不一致原因": "",
        "实际权属单位": "",
        "实际权属性质": "",
        "永久基本农田面积": "0.0000",
        "变更调查年度": "",
        "调查总面积": "0.0000",
        "调查农用地": "0.0000",
        "调查耕地": "0.0000",
        "调查水田": "0.0000",
        "调查建设用地": "0.0000",
        "调查未利用地": "0.0000",
        "调查与实际一致": "是",
        "无合法来源建设用地面积": "0.0000",
        "违法涉及农用地": "0.0000",
        "违法涉及耕地": "0.0000",
        "违法发生在2020年前": "否",
        "违法涉及可调整地类": "0.0000",
        "违法涉及未利用地": "0.0000",
        "已依法批准建设用地面积": "0.0000",
        "批准涉及农用地": "0.0000",
        "批准涉及耕地": "0.0000",
        "批准涉及未利用地": "0.0000",
        "其他不一致情况": "否",
        "其他不一致原因": "",
        "涉及53号文情形": "否",
        "现状耕地面积53号文": "0.0000",
        "调查林地总面积": "0.0000",
        "无需林地审批面积": "0.0000",
        "实际申请总面积": "0.0000",
        "实际农用地": "0.0000",
        "实际耕地": "0.0000",
        "实际永久基本农田": "0.0000",
        "实际可调整地类": "0.0000",
        "实际建设用地": "0.0000",
        "实际未利用地": "0.0000",
        "项目类型": "普通",
        # 批次用地特有字段
        "批次名称": "",
        "批次涉及乡镇数": "",
        "批次涉及村数": "",
        "批次宗地总数": "",
        "批次已发证宗地数": "",
        "批次未发证宗地数": "",
        "批次未发证原因": "",
        "批次权属数据库一致": "是",
        "批次永久基本农田面积": "0.0000",
        "批次调查总面积": "0.0000",
        "批次调查农用地": "0.0000",
        "批次调查耕地": "0.0000",
        "批次调查水田": "0.0000",
        "批次调查建设用地": "0.0000",
        "批次调查未利用地": "0.0000",
        "批次实际申请总面积": "0.0000",
        "批次实际农用地": "0.0000",
        "批次实际耕地": "0.0000",
        "批次实际永久基本农田": "0.0000",
        "批次实际建设用地": "0.0000",
        "批次实际未利用地": "0.0000"
    }

    # 头部信息（默认折叠）
    with st.expander("文件原文（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室
        自然资源确权登记局、自然资源调查监测处

        ### 二、审查标准
        1. 勘测定界符合《土地勘测定界规程》(TD/T1008-2007)、《土地利用现状分类》(GB/T21010-2017)等规定。
        2. 集体土地和国有土地宗地数正确，登记发证情况符合要求，权属清楚，无争议。
        3. 现状地类以"三调"地类为基础、组卷时最新年度变更调查数据为准，总面积、农用地、耕地、建设用地、未利用地面积差异均在合理误差范围内(总面积差异在1%以内或各地类面积差异在1%以内)或无差异。
        4. 已按照自然资源部办公厅《关于以"三调"成果为基础做好建设用地审查报批地类认定的通知》(自然资办发(2022)411号)、《关于以第三次全国国土调查成果为基础明确林地管理边界规范林地管理的通知》(自然资发(2023)53号)等规定完成报批地类认定。
        """)
    # 初始化返回结果
    component_result = {}
    
    # 存储每个区块的结果
    all_results = {}
    
    # 根据用地类型分别处理不同区块
    if land_type == '单独选址':
        # 区块1: 权属基本情况
        st.markdown("### 〔权属基本情况〕")
        # 判断区域 - 未发证宗地数是否有值
        未发证宗地数 = button_group(
            label="",
            options=[{"label": "有未发证宗地", "value": "有"}, {"label": "无", "value": "无"}],
            default_value="无",
            key="未发证宗地数存在"
        )
        # 更新会话状态
        st.session_state.default_values['未发证宗地数存在'] = 未发证宗地数
        
        # 构建模板
        if 未发证宗地数 == "有":
            block1_template = '''项目用地涉及{{涉及县列表}}县（市、区）的{{乡镇数}}个乡镇、{{村数}}个村和{{国有单位数}}个国有单位，共{{宗地总数}}宗地（集体土地所有权与国有土地使用权合计），其中：{{已发证宗地数}}宗地已登记发证，{{未发证宗地数}}宗地未登记发证，原因：{{未发证原因及权利人意见}}，土地产权明晰，界址清楚，没有争议。'''  
        else:
            block1_template = '''项目用地涉及{{涉及县列表}}县（市、区）的{{乡镇数}}个乡镇、{{村数}}个村和{{国有单位数}}个国有单位，共{{宗地总数}}宗地（集体土地所有权与国有土地使用权合计），其中：{{已发证宗地数}}宗地已登记发证，土地产权明晰，界址清楚，没有争议。'''  
        
        all_results['block1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_block1"
        )
        
        # 区块2: 权属数据库一致性
        st.markdown("### 〔权属数据库一致性〕")
        权属数据库一致 = button_group(
            label="",
            options=[{"label": "权属数据库一致", "value": "是"}, {"label": "不一致", "value": "否"}],
            default_value="是",
            key="权属数据库一致"
        )
        st.session_state.default_values['权属数据库一致'] = 权属数据库一致
        
        if 权属数据库一致 == "否":
            不一致图斑数 = button_group(
                label="",
                options=[{"label": "不一致图斑数不超过5个", "value": ""}, {"label": "不一致图斑数超过5个", "value": "超过5"}],
                default_value="",
                key="不一致图斑数超过5"
            )
            st.session_state.default_values['不一致图斑数超过5'] = 不一致图斑数
            
            if 不一致图斑数 == "超过5":
                block2_template = '''权属数据库是否一致：{{权属数据库一致}}\n权属数据库和实际情况不一致：图斑共{{不一致图斑数}}个，面积{{不一致面积}}公顷，地类权属单位{{图斑权属单位}}，权属性质{{图斑权属性质}}。经实地调查（原因：{{不一致原因}}），实际为{{实际权属单位}}，权属性质{{实际权属性质}}。（不一致图斑列表另附）'''  
            else:
                block2_template = '''权属数据库是否一致：{{权属数据库一致}}\n权属数据库和实际情况不一致：图斑共{{不一致图斑数}}个，面积{{不一致面积}}公顷，地类权属单位{{图斑权属单位}}，权属性质{{图斑权属性质}}。经实地调查（原因：{{不一致原因}}），实际为{{实际权属单位}}，权属性质{{实际权属性质}}。'''  
        else:
            block2_template = '''权属数据库是否一致：{{权属数据库一致}}'''  
        
        all_results['block2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_block2"
        )
        
        # 区块3: 永久基本农田情况
        st.markdown("### 〔永久基本农田情况〕")
        block3_template = '''项目申请用地范围涉及永久基本农田{{永久基本农田面积}}公顷。'''  
        all_results['block3'] = lineinput(
            block3_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_block3"
        )
        
        # 区块4: 变更调查套合情况
        st.markdown("### 〔变更调查套合情况〕")
        block4_template = '''经与{{变更调查年度}}年度国土变更调查成果套合，项目申请用地范围内{{变更调查年度}}年度国土变更调查成果现状情况为：总面积{{调查总面积}}公顷，其中，农用地{{调查农用地}}公顷（耕地{{调查耕地}}公顷，含水田{{调查水田}}公顷），建设用地{{调查建设用地}}公顷，未利用地{{调查未利用地}}公顷。'''  
        all_results['block4'] = lineinput(
            block4_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_block4"
        )
        
        # 区块5: 调查与实际一致性
        st.markdown("### 〔调查与实际一致性〕")
        调查与实际一致 = button_group(
            label="",
            options=[{"label": "调查与实际一致", "value": "是"}, {"label": "不一致", "value": "否"}],
            default_value="是",
            key="调查与实际一致"
        )
        st.session_state.default_values['调查与实际一致'] = 调查与实际一致
        
        if 调查与实际一致 == "否":
            # 构建不一致情况模板
            存在无合法来源建设用地 = button_group(
                label="",
                options=[{"label": "存在无合法来源建设用地", "value": "存在"}, {"label": "不存在", "value": "不存在"}],
                default_value="",
                key="存在无合法来源建设用地"
            )
            st.session_state.default_values['存在无合法来源建设用地'] = 存在无合法来源建设用地
            
            存在已依法批准建设用地 = button_group(
                label="",
                options=[{"label": "存在已依法批准建设用地", "value": "存在"}, {"label": "不存在", "value": "不存在"}],
                default_value="",
                key="存在已依法批准建设用地"
            )
            st.session_state.default_values['存在已依法批准建设用地'] = 存在已依法批准建设用地
            
            其他不一致情况 = button_group(
                label="",
                options=[{"label": "有其他不一致情况", "value": "是"}, {"label": "没有", "value": "否"}],
                default_value="否",
                key="其他不一致情况"
            )
            st.session_state.default_values['其他不一致情况'] = 其他不一致情况
            
            block5_template = '''调查与实际是否一致：{{调查与实际一致}}\n'''  
            
            if 存在无合法来源建设用地 == "存在":
                违法发生在2020年前 = button_group(
                    label="",
                    options=[{"label": "违法发生在2020年前", "value": "是"}, {"label": "违法发生在2020年后", "value": "否"}],
                    default_value="否",
                    key="违法发生在2020年前"
                )
                st.session_state.default_values['违法发生在2020年前'] = 违法发生在2020年前
                
                if 违法发生在2020年前 == "是":
                    block5_template += '''一是{{变更调查年度}}年度国土变更调查现状成果中存在无合法来源建设用地。{{变更调查年度}}年度国土变更调查现状成果中建设用地{{无合法来源建设用地面积}}公顷因无合法来源，相关建设用地按照违法用地发生前一年的国土（土地）利用现状地类报批，涉及农用地{{违法涉及农用地}}公顷（其中耕地{{违法涉及耕地}}公顷；可调整地类{{违法涉及可调整地类}}公顷）、未利用地{{违法涉及未利用地}}公顷。（具体情况列表附后）\n'''  
                else:
                    block5_template += '''一是{{变更调查年度}}年度国土变更调查现状成果中存在无合法来源建设用地。{{变更调查年度}}年度国土变更调查现状成果中建设用地{{无合法来源建设用地面积}}公顷因无合法来源，相关建设用地按照违法用地发生前一年的国土（土地）利用现状地类报批，涉及农用地{{违法涉及农用地}}公顷（其中耕地{{违法涉及耕地}}公顷）、未利用地{{违法涉及未利用地}}公顷。（具体情况列表附后）\n'''  
            
            if 存在已依法批准建设用地 == "存在":
                block5_template += '''二是{{变更调查年度}}年度国土变更调查现状成果中存在已依法批准建设用地。{{变更调查年度}}年度国土变更调查现状成果中农用地{{批准涉及农用地}}公顷（耕地{{批准涉及耕地}}公顷）、未利用地{{批准涉及未利用地}}公顷，已经依法批准为建设用地（具体情况列表附后）。\n'''  
            
            if 其他不一致情况 == "是":
                block5_template += '''三是其他。除上述情况外，项目申请用地范围内{{变更调查年度}}年度国土变更调查现状成果中还存在其它需要说明的情况，具体原因：{{其他不一致原因}}。\n'''  
        else:
            block5_template = '''调查与实际是否一致：{{调查与实际一致}}'''  
        
        all_results['block5'] = lineinput(
            block5_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_block5"
        )
        
        # 区块6: 53号文特殊处理
        st.markdown("### 〔53号文特殊处理〕")
        涉及53号文情形 = button_group(
            label="",
            options=[{"label": "涉及53号文情形", "value": "是"}, {"label": "不涉及", "value": "否"}],
            default_value="否",
            key="涉及53号文情形"
        )
        st.session_state.default_values['涉及53号文情形'] = 涉及53号文情形
        
        if 涉及53号文情形 == "是":
            block6_template = '''根据《关于以第三次全国国土调查成果为基础明确林地管理边界规范林地管理的通知》（自然资发〔2023〕53号）要求，项目用地范围内有{{现状耕地面积53号文}}公顷现状耕地，属于《国务院关于保护森林制止毁林开垦和乱占林地的通知》（国发明电〔1998〕8号）印发以后，在国有林区、国有林场的国有林权证范围内的林地（湿地、草地）上开垦形成且未划入保护红线的，已按林地办理审批手续，按规定不需要落实耕地占补平衡。项目用地范围内{{变更调查年度}}年度国土变更调查现状成果中林地{{调查林地总面积}}公顷，其中有{{无需林地审批面积}}公顷按要求无需办理林地审批手续。'''  
            all_results['block6'] = lineinput(
                block6_template,
                default_values=st.session_state.default_values.copy(),
                key="page_5_block6"
            )
        
        # 区块7: 实际申请用地情况汇总
        st.markdown("### 〔实际申请用地情况汇总〕")
        违法发生在2020年前最终 = st.session_state.default_values.get('违法发生在2020年前', '否')
        
        if 违法发生在2020年前最终 == "是":
            block7_template = '''综上，该项目实际申请用地情况为：总面积{{实际申请总面积}}公顷，其中，农用地{{实际农用地}}公顷（其中耕地{{实际耕地}}公顷，含永久基本农田{{实际永久基本农田}}公顷；可调整地类{{实际可调整地类}}公顷）、建设用地{{实际建设用地}}公顷、未利用地{{实际未利用地}}公顷。\n\n项目类型：{{项目类型}}'''  
        else:
            block7_template = '''综上，该项目实际申请用地情况为：总面积{{实际申请总面积}}公顷，其中，农用地{{实际农用地}}公顷（其中耕地{{实际耕地}}公顷，含永久基本农田{{实际永久基本农田}}公顷）、建设用地{{实际建设用地}}公顷、未利用地{{实际未利用地}}公顷。\n\n项目类型：{{项目类型}}'''  
        
        all_results['block7'] = lineinput(
            block7_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_block7"
        )
        
    else:
        # 批次用地模板 - 区块1: 基本情况
        st.markdown("### 〔基本情况〕")
        # 判断区域 - 未发证宗地数是否有值
        批次未发证宗地数 = button_group(
            label="",
            options=[{"label": "无未发证宗地", "value": "无"}, {"label": "有未发证宗地", "value": "有"}],
            default_value="",
            key="批次未发证宗地数存在"
        )
        # 更新会话状态
        st.session_state.default_values['批次未发证宗地数存在'] = 批次未发证宗地数
        
        # 构建模板
        if 批次未发证宗地数 == "有":
            block1_template = '''{{批次名称}}涉及{{批次涉及乡镇数}}个乡镇、{{批次涉及村数}}个村，共{{批次宗地总数}}宗地，其中：{{批次已发证宗地数}}宗地已登记发证，{{批次未发证宗地数}}宗地未登记发证，原因：{{批次未发证原因}}，土地产权明晰，界址清楚，没有争议。'''  
        else:
            block1_template = '''{{批次名称}}涉及{{批次涉及乡镇数}}个乡镇、{{批次涉及村数}}个村，共{{批次宗地总数}}宗地，其中：{{批次已发证宗地数}}宗地已登记发证，土地产权明晰，界址清楚，没有争议。'''  
        
        all_results['batch_block1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_batch_block1"
        )
        
        # 批次用地模板 - 区块2: 权属数据库一致性
        st.markdown("### 〔权属数据库一致性〕")
        block2_template = '''权属数据库是否一致：{{批次权属数据库一致}}'''  
        all_results['batch_block2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_batch_block2"
        )
        
        # 批次用地模板 - 区块3: 永久基本农田情况
        st.markdown("### 〔永久基本农田情况〕")
        block3_template = '''项目申请用地范围涉及永久基本农田{{批次永久基本农田面积}}公顷。'''  
        all_results['batch_block3'] = lineinput(
            block3_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_batch_block3"
        )
        
        # 批次用地模板 - 区块4: 变更调查套合情况
        st.markdown("### 〔变更调查套合情况〕")
        block4_template = '''经与{{变更调查年度}}年度国土变更调查成果套合，批次用地范围内现状情况为：总面积{{批次调查总面积}}公顷，其中，农用地{{批次调查农用地}}公顷（耕地{{批次调查耕地}}公顷，含水田{{批次调查水田}}公顷），建设用地{{批次调查建设用地}}公顷，未利用地{{批次调查未利用地}}公顷。'''  
        all_results['batch_block4'] = lineinput(
            block4_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_batch_block4"
        )
        
        # 批次用地模板 - 区块5: 实际申请用地情况汇总
        st.markdown("### 〔实际申请用地情况汇总〕")
        block5_template = '''综上，该批次实际申请用地情况为：总面积{{批次实际申请总面积}}公顷，其中，农用地{{批次实际农用地}}公顷（其中耕地{{批次实际耕地}}公顷，含永久基本农田{{批次实际永久基本农田}}公顷）、建设用地{{批次实际建设用地}}公顷、未利用地{{批次实际未利用地}}公顷。'''  
        all_results['batch_block5'] = lineinput(
            block5_template,
            default_values=st.session_state.default_values.copy(),
            key="page_5_batch_block5"
        )
    
    # 更新默认值缓存
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 合并所有区块的结果
    for block_result in all_results.values():
        if isinstance(block_result, dict):
            component_result.update(block_result)
    
    return component_result