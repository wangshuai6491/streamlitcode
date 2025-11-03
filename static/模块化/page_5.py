import streamlit as st
from datetime import datetime
from common_components import button_group

# 生成唯一的组件key
def generate_key(component_type, index=None):
    """为组件生成唯一的key"""
    timestamp = datetime.now().timestamp()
    if index is not None:
        return f"{component_type}_{index}_{timestamp}"
    return f"{component_type}_{timestamp}"
def page_5():
    # 页面标题
    st.title("权属地类单元")

    # 文件原文折叠面板
    with st.expander("文件原文", expanded=False):
        st.markdown("""### 一、业务指导处室
    自然资源确权登记局、自然资源调查监测处

    ### 二、审查标准
    1. 勘测定界符合《土地勘测定界规程》(TD/T1008-2007)、《土地利用现状分类》(GB/T21010-2017)等规定。
    2. 集体土地和国有土地宗地数正确，登记发证情况符合要求，权属清楚，无争议。
    3. 现状地类以"三调"地类为基础、组卷时最新年度变更调查数据为准，总面积、农用地、耕地、建设用地、未利用地面积差异均在合理误差范围内(总面积差异在1%以内或各地类面积差异在1%以内)或无差异。
    4. 已按照自然资源部办公厅《关于以"三调"成果为基础做好建设用地审查报批地类认定的通知》(自然资办发(2022)411号)、《关于以第三次全国国土调查成果为基础明确林地管理边界规范林地管理的通知》(自然资发(2023)53号)等规定完成报批地类认定。""")

    # 初始化默认值字典
    def get_default_values():
        return {
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
            "不一致面积": "",
            "图斑权属单位": "",
            "图斑权属性质": "",
            "不一致原因": "",
            "实际权属单位": "",
            "实际权属性质": "",
            "永久基本农田面积": "",
            "变更调查年度": "",
            "调查总面积": "",
            "调查农用地": "",
            "调查耕地": "",
            "调查水田": "",
            "调查建设用地": "",
            "调查未利用地": "",
            "调查与实际一致": "是",
            "无合法来源建设用地面积": "",
            "违法涉及农用地": "",
            "违法涉及耕地": "",
            "违法发生在2020年前": "否",
            "违法涉及可调整地类": "",
            "违法涉及未利用地": "",
            "已依法批准建设用地面积": "",
            "批准涉及农用地": "",
            "批准涉及耕地": "",
            "批准涉及未利用地": "",
            "其他不一致情况": "否",
            "其他不一致原因": "",
            "涉及53号文情形": "否",
            "现状耕地面积53号文": "",
            "调查林地总面积": "",
            "无需林地审批面积": "",
            "实际申请总面积": "",
            "实际农用地": "",
            "实际耕地": "",
            "实际永久基本农田": "",
            "实际可调整地类": "",
            "实际建设用地": "",
            "实际未利用地": "",
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
            "批次不一致图斑数": "",
            "批次不一致面积": "",
            "批次图斑权属单位": "",
            "批次图斑权属性质": "",
            "批次不一致原因": "",
            "批次实际权属单位": "",
            "批次实际权属性质": "",
            "批次永久基本农田面积": "",
            "批次调查总面积": "",
            "批次调查农用地": "",
            "批次调查耕地": "",
            "批次调查水田": "",
            "批次调查建设用地": "",
            "批次调查未利用地": "",
            "批次调查与实际一致": "是",
            "批次无合法来源建设用地面积": "",
            "批次违法涉及农用地": "",
            "批次违法涉及耕地": "",
            "批次违法发生在2020年前": "否",
            "批次违法涉及可调整地类": "",
            "批次违法涉及未利用地": "",
            "批次已依法批准建设用地面积": "",
            "批次批准涉及农用地": "",
            "批次批准涉及耕地": "",
            "批次批准涉及未利用地": "",
            "批次其他不一致情况": "否",
            "批次其他不一致原因": "",
            "批次涉及53号文情形": "否",
            "批次现状耕地面积53号文": "",
            "批次调查林地总面积": "",
            "批次无需林地审批面积": "",
            "批次实际申请总面积": "",
            "批次实际农用地": "",
            "批次实际耕地": "",
            "批次实际永久基本农田": "",
            "批次实际可调整地类": "",
            "批次实际建设用地": "",
            "批次实际未利用地": ""
        }

    # 初始化session_state
    if "land_right_form" not in st.session_state:
        st.session_state.land_right_form = get_default_values()

    # 用地类型选择
    land_type = button_group(
        "",
        options=[{"label": "单独选址", "value": "single"}, {"label": "批次用地", "value": "batch"}],
        default_value="single",
        key=generate_key("land_type")
    )

    # 动态更新表单值
    for key, default_value in get_default_values().items():
        if key not in st.session_state.land_right_form:
            st.session_state.land_right_form[key] = default_value

    # 审查内容模板
    st.subheader("三、审查内容模板")

    # 生成模板文本
    def generate_template():
        fixed_template = "[权属、地类和面积]\n\n"
        
        if land_type == "single":
            # 单独选址模板
            fixed_template += f"项目用地涉及{st.session_state.land_right_form['涉及县列表']}县（市、区）的{st.session_state.land_right_form['乡镇数']}个乡镇、{st.session_state.land_right_form['村数']}个村和{st.session_state.land_right_form['国有单位数']}个国有单位，共{st.session_state.land_right_form['宗地总数']}宗地（集体土地所有权与国有土地使用权合计），其中：{st.session_state.land_right_form['已发证宗地数']}宗地已登记发证，{st.session_state.land_right_form['未发证宗地数']}宗地未登记发证"
            
            if st.session_state.land_right_form['未发证宗地数'] and st.session_state.land_right_form['未发证宗地数'] != "":
                fixed_template += f"，原因：{st.session_state.land_right_form['未发证原因及权利人意见']}"
            
            fixed_template += "，土地产权明晰，界址清楚，没有争议。\n\n"
            
            # 权属数据库是否一致
            fixed_template += f"权属数据库是否一致：{st.session_state.land_right_form['权属数据库一致']}\n"
            
            if st.session_state.land_right_form['权属数据库一致'] == "否":
                fixed_template += f"权属数据库和实际情况不一致：图斑共{st.session_state.land_right_form['不一致图斑数']}个，面积{st.session_state.land_right_form['不一致面积']}公顷，地类权属单位{st.session_state.land_right_form['图斑权属单位']}，权属性质{st.session_state.land_right_form['图斑权属性质']}。经实地调查（原因：{st.session_state.land_right_form['不一致原因']}），实际为{st.session_state.land_right_form['实际权属单位']}，权属性质{st.session_state.land_right_form['实际权属性质']}。"
                if st.session_state.land_right_form['不一致图斑数'] and st.session_state.land_right_form['不一致图斑数'] != "" and int(st.session_state.land_right_form['不一致图斑数']) > 5:
                    fixed_template += "（不一致图斑列表另附）"
                fixed_template += "\n\n"
            
            # 永久基本农田面积
            fixed_template += f"项目申请用地范围涉及永久基本农田{st.session_state.land_right_form['永久基本农田面积']}公顷。\n\n"
            
            # 与年度国土变更调查成果套合
            fixed_template += f"经与{st.session_state.land_right_form['变更调查年度']}年度国土变更调查成果套合，项目申请用地范围内{st.session_state.land_right_form['变更调查年度']}年度国土变更调查成果现状情况为：总面积{st.session_state.land_right_form['调查总面积']}公顷，其中，农用地{st.session_state.land_right_form['调查农用地']}公顷（耕地{st.session_state.land_right_form['调查耕地']}公顷，含水田{st.session_state.land_right_form['调查水田']}公顷），建设用地{st.session_state.land_right_form['调查建设用地']}公顷，未利用地{st.session_state.land_right_form['调查未利用地']}公顷。\n\n"
            
            # 调查与实际是否一致
            fixed_template += f"调查与实际是否一致：{st.session_state.land_right_form['调查与实际一致']}\n"
            
            if st.session_state.land_right_form['调查与实际一致'] == "否":
                # 无合法来源建设用地
                if st.session_state.land_right_form['无合法来源建设用地面积'] and st.session_state.land_right_form['无合法来源建设用地面积'] != "":
                    fixed_template += f"一是{st.session_state.land_right_form['变更调查年度']}年度国土变更调查现状成果中存在无合法来源建设用地。{st.session_state.land_right_form['变更调查年度']}年度国土变更调查现状成果中建设用地{st.session_state.land_right_form['无合法来源建设用地面积']}公顷因无合法来源，相关建设用地按照违法用地发生前一年的国土（土地）利用现状地类报批，涉及农用地{st.session_state.land_right_form['违法涉及农用地']}公顷（其中耕地{st.session_state.land_right_form['违法涉及耕地']}公顷"
                    
                    if st.session_state.land_right_form['违法发生在2020年前'] == "是":
                        fixed_template += f"；可调整地类{st.session_state.land_right_form['违法涉及可调整地类']}公顷"
                    
                    fixed_template += f"）、未利用地{st.session_state.land_right_form['违法涉及未利用地']}公顷。（具体情况列表附后）\n"
                
                # 已依法批准建设用地
                if st.session_state.land_right_form['已依法批准建设用地面积'] and st.session_state.land_right_form['已依法批准建设用地面积'] != "":
                    fixed_template += f"二是{st.session_state.land_right_form['变更调查年度']}年度国土变更调查现状成果中存在已依法批准建设用地。{st.session_state.land_right_form['变更调查年度']}年度国土变更调查现状成果中农用地{st.session_state.land_right_form['批准涉及农用地']}公顷（耕地{st.session_state.land_right_form['批准涉及耕地']}公顷）、未利用地{st.session_state.land_right_form['批准涉及未利用地']}公顷，已经依法批准为建设用地（具体情况列表附后）。\n"
                
                # 其他不一致情况
                if st.session_state.land_right_form['其他不一致情况'] == "是":
                    fixed_template += f"三是其他。除上述情况外，项目申请用地范围内{st.session_state.land_right_form['变更调查年度']}年度国土变更调查现状成果中还存在其它需要说明的情况，具体原因：{st.session_state.land_right_form['其他不一致原因']}。\n"
                
                fixed_template += "\n"
            
            # 53号文特殊处理
            if st.session_state.land_right_form['涉及53号文情形'] == "是":
                fixed_template += f"根据《关于以第三次全国国土调查成果为基础明确林地管理边界规范林地管理的通知》（自然资发〔2023〕53号）要求，项目用地范围内有{st.session_state.land_right_form['现状耕地面积53号文']}公顷现状耕地，属于《国务院关于保护森林制止毁林开垦和乱占林地的通知》（国发明电〔1998〕8号）印发以后，在国有林区、国有林场的国有林权证范围内的林地（湿地、草地）上开垦形成且未划入保护红线的，已按林地办理审批手续，按规定不需要落实耕地占补平衡。项目用地范围内{st.session_state.land_right_form['变更调查年度']}年度国土变更调查现状成果中林地{st.session_state.land_right_form['调查林地总面积']}公顷，其中有{st.session_state.land_right_form['无需林地审批面积']}公顷按要求无需办理林地审批手续。\n\n"
            
            # 汇总实际申请用地情况
            fixed_template += f"综上，该项目实际申请用地情况为：总面积{st.session_state.land_right_form['实际申请总面积']}公顷，其中，农用地{st.session_state.land_right_form['实际农用地']}公顷（其中耕地{st.session_state.land_right_form['实际耕地']}公顷，含永久基本农田{st.session_state.land_right_form['实际永久基本农田']}公顷"
            
            if st.session_state.land_right_form['违法发生在2020年前'] == "是":
                fixed_template += f"；可调整地类{st.session_state.land_right_form['实际可调整地类']}公顷"
            
            fixed_template += f"）、建设用地{st.session_state.land_right_form['实际建设用地']}公顷、未利用地{st.session_state.land_right_form['实际未利用地']}公顷。\n\n"
            
            # 项目类型
            fixed_template += f"项目类型：{st.session_state.land_right_form['项目类型']}"
        
        else:
            # 批次用地模板（简化版，根据实际需求可扩展）
            fixed_template += f"{st.session_state.land_right_form['批次名称']}涉及{st.session_state.land_right_form['批次涉及乡镇数']}个乡镇、{st.session_state.land_right_form['批次涉及村数']}个村，共{st.session_state.land_right_form['批次宗地总数']}宗地，其中：{st.session_state.land_right_form['批次已发证宗地数']}宗地已登记发证，{st.session_state.land_right_form['批次未发证宗地数']}宗地未登记发证"
            
            if st.session_state.land_right_form['批次未发证宗地数'] and st.session_state.land_right_form['批次未发证宗地数'] != "":
                fixed_template += f"，原因：{st.session_state.land_right_form['批次未发证原因']}"
            
            fixed_template += "，土地产权明晰，界址清楚，没有争议。\n\n"
            
            # 其他批次用地相关内容
            fixed_template += f"权属数据库是否一致：{st.session_state.land_right_form['批次权属数据库一致']}\n"
            fixed_template += f"项目申请用地范围涉及永久基本农田{st.session_state.land_right_form['批次永久基本农田面积']}公顷。\n\n"
            fixed_template += f"经与{st.session_state.land_right_form['变更调查年度']}年度国土变更调查成果套合，批次用地范围内现状情况为：总面积{st.session_state.land_right_form['批次调查总面积']}公顷，其中，农用地{st.session_state.land_right_form['批次调查农用地']}公顷（耕地{st.session_state.land_right_form['批次调查耕地']}公顷，含水田{st.session_state.land_right_form['批次调查水田']}公顷），建设用地{st.session_state.land_right_form['批次调查建设用地']}公顷，未利用地{st.session_state.land_right_form['批次调查未利用地']}公顷。\n\n"
            fixed_template += f"综上，该批次实际申请用地情况为：总面积{st.session_state.land_right_form['批次实际申请总面积']}公顷，其中，农用地{st.session_state.land_right_form['批次实际农用地']}公顷（其中耕地{st.session_state.land_right_form['批次实际耕地']}公顷，含永久基本农田{st.session_state.land_right_form['批次实际永久基本农田']}公顷）、建设用地{st.session_state.land_right_form['批次实际建设用地']}公顷、未利用地{st.session_state.land_right_form['批次实际未利用地']}公顷。"
        
        return fixed_template

    # 显示表单
    if land_type == "single":
        # 单独选址表单
        with st.form(key=generate_key("single_form")):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.land_right_form['涉及县列表'] = st.text_input("涉及县列表", value=st.session_state.land_right_form['涉及县列表'], key=generate_key("涉及县列表"))
                st.session_state.land_right_form['乡镇数'] = st.text_input("乡镇数", value=st.session_state.land_right_form['乡镇数'], key=generate_key("乡镇数"))
                st.session_state.land_right_form['村数'] = st.text_input("村数", value=st.session_state.land_right_form['村数'], key=generate_key("村数"))
            with col2:
                st.session_state.land_right_form['国有单位数'] = st.text_input("国有单位数", value=st.session_state.land_right_form['国有单位数'], key=generate_key("国有单位数"))
                st.session_state.land_right_form['宗地总数'] = st.text_input("宗地总数", value=st.session_state.land_right_form['宗地总数'], key=generate_key("宗地总数"))
                
            col3, col4 = st.columns(2)
            with col3:
                st.session_state.land_right_form['已发证宗地数'] = st.text_input("已发证宗地数", value=st.session_state.land_right_form['已发证宗地数'], key=generate_key("已发证宗地数"))
            with col4:
                st.session_state.land_right_form['未发证宗地数'] = st.text_input("未发证宗地数", value=st.session_state.land_right_form['未发证宗地数'], key=generate_key("未发证宗地数"))
            
            if st.session_state.land_right_form['未发证宗地数'] and st.session_state.land_right_form['未发证宗地数'] != "":
                st.session_state.land_right_form['未发证原因及权利人意见'] = st.text_input("未发证原因", value=st.session_state.land_right_form['未发证原因及权利人意见'], key=generate_key("未发证原因"))
            
            st.divider()
            
            # 权属数据库是否一致
            st.session_state.land_right_form['权属数据库一致'] = st.radio(
                "权属数据库是否一致",
                options=["是", "否"],
                index=0 if st.session_state.land_right_form['权属数据库一致'] == "是" else 1,
                key=generate_key("权属数据库一致")
            )
            
            if st.session_state.land_right_form['权属数据库一致'] == "否":
                col5, col6 = st.columns(2)
                with col5:
                    st.session_state.land_right_form['不一致图斑数'] = st.text_input("不一致图斑数", value=st.session_state.land_right_form['不一致图斑数'], key=generate_key("不一致图斑数"))
                    st.session_state.land_right_form['不一致面积'] = st.text_input("不一致面积(公顷)", value=st.session_state.land_right_form['不一致面积'], key=generate_key("不一致面积"))
                    st.session_state.land_right_form['图斑权属单位'] = st.text_input("图斑权属单位", value=st.session_state.land_right_form['图斑权属单位'], key=generate_key("图斑权属单位"))
                with col6:
                    st.session_state.land_right_form['图斑权属性质'] = st.text_input("图斑权属性质", value=st.session_state.land_right_form['图斑权属性质'], key=generate_key("图斑权属性质"))
                    st.session_state.land_right_form['不一致原因'] = st.text_input("不一致原因", value=st.session_state.land_right_form['不一致原因'], key=generate_key("不一致原因"))
                    st.session_state.land_right_form['实际权属单位'] = st.text_input("实际权属单位", value=st.session_state.land_right_form['实际权属单位'], key=generate_key("实际权属单位"))
                st.session_state.land_right_form['实际权属性质'] = st.text_input("实际权属性质", value=st.session_state.land_right_form['实际权属性质'], key=generate_key("实际权属性质"))
            
            st.divider()
            
            # 永久基本农田面积
            st.session_state.land_right_form['永久基本农田面积'] = st.text_input("永久基本农田面积(公顷)", value=st.session_state.land_right_form['永久基本农田面积'], key=generate_key("永久基本农田面积"))
            
            st.divider()
            
            # 变更调查信息
            st.subheader("变更调查信息")
            st.session_state.land_right_form['变更调查年度'] = st.text_input("变更调查年度", value=st.session_state.land_right_form['变更调查年度'], key=generate_key("变更调查年度"))
            
            col7 = st.columns(5)
            st.session_state.land_right_form['调查总面积'] = st.text_input("调查总面积(公顷)", value=st.session_state.land_right_form['调查总面积'], key=generate_key("调查总面积"))
            
            col8, col9 = st.columns(2)
            with col8:
                st.session_state.land_right_form['调查农用地'] = st.text_input("调查农用地(公顷)", value=st.session_state.land_right_form['调查农用地'], key=generate_key("调查农用地"))
                st.session_state.land_right_form['调查耕地'] = st.text_input("调查耕地(公顷)", value=st.session_state.land_right_form['调查耕地'], key=generate_key("调查耕地"))
            with col9:
                st.session_state.land_right_form['调查水田'] = st.text_input("调查水田(公顷)", value=st.session_state.land_right_form['调查水田'], key=generate_key("调查水田"))
                st.session_state.land_right_form['调查建设用地'] = st.text_input("调查建设用地(公顷)", value=st.session_state.land_right_form['调查建设用地'], key=generate_key("调查建设用地"))
            
            st.session_state.land_right_form['调查未利用地'] = st.text_input("调查未利用地(公顷)", value=st.session_state.land_right_form['调查未利用地'], key=generate_key("调查未利用地"))
            
            st.divider()
            
            # 调查与实际是否一致
            st.session_state.land_right_form['调查与实际一致'] = st.radio(
                "调查与实际是否一致",
                options=["是", "否"],
                index=0 if st.session_state.land_right_form['调查与实际一致'] == "是" else 1,
                key=generate_key("调查与实际一致")
            )
            
            if st.session_state.land_right_form['调查与实际一致'] == "否":
                # 无合法来源建设用地
                has_illegal_land = st.checkbox("存在无合法来源建设用地", value=bool(st.session_state.land_right_form['无合法来源建设用地面积']), key=generate_key("has_illegal_land"))
                if has_illegal_land:
                    if not st.session_state.land_right_form['无合法来源建设用地面积']:
                        st.session_state.land_right_form['无合法来源建设用地面积'] = "0"
                    
                    col10, col11 = st.columns(2)
                    with col10:
                        st.session_state.land_right_form['无合法来源建设用地面积'] = st.text_input("无合法来源建设用地面积(公顷)", value=st.session_state.land_right_form['无合法来源建设用地面积'], key=generate_key("无合法来源建设用地面积"))
                        st.session_state.land_right_form['违法涉及农用地'] = st.text_input("违法涉及农用地(公顷)", value=st.session_state.land_right_form['违法涉及农用地'], key=generate_key("违法涉及农用地"))
                    with col11:
                        st.session_state.land_right_form['违法涉及耕地'] = st.text_input("违法涉及耕地(公顷)", value=st.session_state.land_right_form['违法涉及耕地'], key=generate_key("违法涉及耕地"))
                        st.session_state.land_right_form['违法涉及未利用地'] = st.text_input("违法涉及未利用地(公顷)", value=st.session_state.land_right_form['违法涉及未利用地'], key=generate_key("违法涉及未利用地"))
                    
                    # 违法发生在2020年前
                    st.session_state.land_right_form['违法发生在2020年前'] = st.radio(
                        "违法发生在2020年前",
                        options=["是", "否"],
                        index=0 if st.session_state.land_right_form['违法发生在2020年前'] == "是" else 1,
                        key=generate_key("违法发生在2020年前")
                    )
                    
                    if st.session_state.land_right_form['违法发生在2020年前'] == "是":
                        st.session_state.land_right_form['违法涉及可调整地类'] = st.text_input("违法涉及可调整地类(公顷)", value=st.session_state.land_right_form['违法涉及可调整地类'], key=generate_key("违法涉及可调整地类"))
                else:
                    st.session_state.land_right_form['无合法来源建设用地面积'] = ""
                
                # 已依法批准建设用地
                has_approved_land = st.checkbox("存在已依法批准建设用地", value=bool(st.session_state.land_right_form['已依法批准建设用地面积']), key=generate_key("has_approved_land"))
                if has_approved_land:
                    if not st.session_state.land_right_form['已依法批准建设用地面积']:
                        st.session_state.land_right_form['已依法批准建设用地面积'] = "0"
                    
                    col12, col13 = st.columns(2)
                    with col12:
                        st.session_state.land_right_form['已依法批准建设用地面积'] = st.text_input("已依法批准建设用地面积(公顷)", value=st.session_state.land_right_form['已依法批准建设用地面积'], key=generate_key("已依法批准建设用地面积"))
                        st.session_state.land_right_form['批准涉及农用地'] = st.text_input("批准涉及农用地(公顷)", value=st.session_state.land_right_form['批准涉及农用地'], key=generate_key("批准涉及农用地"))
                    with col13:
                        st.session_state.land_right_form['批准涉及耕地'] = st.text_input("批准涉及耕地(公顷)", value=st.session_state.land_right_form['批准涉及耕地'], key=generate_key("批准涉及耕地"))
                        st.session_state.land_right_form['批准涉及未利用地'] = st.text_input("批准涉及未利用地(公顷)", value=st.session_state.land_right_form['批准涉及未利用地'], key=generate_key("批准涉及未利用地"))
                else:
                    st.session_state.land_right_form['已依法批准建设用地面积'] = ""
                
                # 其他不一致情况
                st.session_state.land_right_form['其他不一致情况'] = st.radio(
                    "其他不一致情况",
                    options=["是", "否"],
                    index=0 if st.session_state.land_right_form['其他不一致情况'] == "是" else 1,
                    key=generate_key("其他不一致情况")
                )
                
                if st.session_state.land_right_form['其他不一致情况'] == "是":
                    st.session_state.land_right_form['其他不一致原因'] = st.text_input("其他不一致原因", value=st.session_state.land_right_form['其他不一致原因'], key=generate_key("其他不一致原因"))
            
            st.divider()
            
            # 53号文特殊处理
            st.session_state.land_right_form['涉及53号文情形'] = st.radio(
                "涉及53号文情形",
                options=["是", "否"],
                index=0 if st.session_state.land_right_form['涉及53号文情形'] == "是" else 1,
                key=generate_key("涉及53号文情形")
            )
            
            if st.session_state.land_right_form['涉及53号文情形'] == "是":
                col14, col15 = st.columns(2)
                with col14:
                    st.session_state.land_right_form['现状耕地面积53号文'] = st.text_input("现状耕地面积53号文(公顷)", value=st.session_state.land_right_form['现状耕地面积53号文'], key=generate_key("现状耕地面积53号文"))
                    st.session_state.land_right_form['调查林地总面积'] = st.text_input("调查林地总面积(公顷)", value=st.session_state.land_right_form['调查林地总面积'], key=generate_key("调查林地总面积"))
                with col15:
                    st.session_state.land_right_form['无需林地审批面积'] = st.text_input("无需林地审批面积(公顷)", value=st.session_state.land_right_form['无需林地审批面积'], key=generate_key("无需林地审批面积"))
            
            st.divider()
            
            # 实际申请用地情况
            st.subheader("实际申请用地情况")
            st.session_state.land_right_form['实际申请总面积'] = st.text_input("实际申请总面积(公顷)", value=st.session_state.land_right_form['实际申请总面积'], key=generate_key("实际申请总面积"))
            
            col16, col17 = st.columns(2)
            with col16:
                st.session_state.land_right_form['实际农用地'] = st.text_input("实际农用地(公顷)", value=st.session_state.land_right_form['实际农用地'], key=generate_key("实际农用地"))
                st.session_state.land_right_form['实际耕地'] = st.text_input("实际耕地(公顷)", value=st.session_state.land_right_form['实际耕地'], key=generate_key("实际耕地"))
                st.session_state.land_right_form['实际永久基本农田'] = st.text_input("实际永久基本农田(公顷)", value=st.session_state.land_right_form['实际永久基本农田'], key=generate_key("实际永久基本农田"))
            with col17:
                if st.session_state.land_right_form['违法发生在2020年前'] == "是":
                    st.session_state.land_right_form['实际可调整地类'] = st.text_input("实际可调整地类(公顷)", value=st.session_state.land_right_form['实际可调整地类'], key=generate_key("实际可调整地类"))
                st.session_state.land_right_form['实际建设用地'] = st.text_input("实际建设用地(公顷)", value=st.session_state.land_right_form['实际建设用地'], key=generate_key("实际建设用地"))
                st.session_state.land_right_form['实际未利用地'] = st.text_input("实际未利用地(公顷)", value=st.session_state.land_right_form['实际未利用地'], key=generate_key("实际未利用地"))
            
            st.divider()
            
            # 项目类型
            st.session_state.land_right_form['项目类型'] = st.radio(
                "项目类型",
                options=["普通", "水利水电"],
                index=0 if st.session_state.land_right_form['项目类型'] == "普通" else 1,
                key=generate_key("项目类型")
            )
            
            st.form_submit_button("生成模板")
    else:
        # 批次用地表单
        with st.form(key=generate_key("batch_form")):
            st.session_state.land_right_form['批次名称'] = st.text_input("批次名称", value=st.session_state.land_right_form['批次名称'], key=generate_key("批次名称"))
            
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.land_right_form['批次涉及乡镇数'] = st.text_input("涉及乡镇数", value=st.session_state.land_right_form['批次涉及乡镇数'], key=generate_key("批次涉及乡镇数"))
                st.session_state.land_right_form['批次涉及村数'] = st.text_input("涉及村数", value=st.session_state.land_right_form['批次涉及村数'], key=generate_key("批次涉及村数"))
            with col2:
                st.session_state.land_right_form['批次宗地总数'] = st.text_input("宗地总数", value=st.session_state.land_right_form['批次宗地总数'], key=generate_key("批次宗地总数"))
                
            col3, col4 = st.columns(2)
            with col3:
                st.session_state.land_right_form['批次已发证宗地数'] = st.text_input("已发证宗地数", value=st.session_state.land_right_form['批次已发证宗地数'], key=generate_key("批次已发证宗地数"))
            with col4:
                st.session_state.land_right_form['批次未发证宗地数'] = st.text_input("未发证宗地数", value=st.session_state.land_right_form['批次未发证宗地数'], key=generate_key("批次未发证宗地数"))
            
            if st.session_state.land_right_form['批次未发证宗地数'] and st.session_state.land_right_form['批次未发证宗地数'] != "":
                st.session_state.land_right_form['批次未发证原因'] = st.text_input("未发证原因", value=st.session_state.land_right_form['批次未发证原因'], key=generate_key("批次未发证原因"))
            
            st.divider()
            
            # 权属数据库是否一致
            st.session_state.land_right_form['批次权属数据库一致'] = st.radio(
                "权属数据库是否一致",
                options=["是", "否"],
                index=0 if st.session_state.land_right_form['批次权属数据库一致'] == "是" else 1,
                key=generate_key("批次权属数据库一致")
            )
            
            # 永久基本农田面积
            st.session_state.land_right_form['批次永久基本农田面积'] = st.text_input("永久基本农田面积(公顷)", value=st.session_state.land_right_form['批次永久基本农田面积'], key=generate_key("批次永久基本农田面积"))
            
            st.divider()
            
            # 变更调查信息
            st.subheader("变更调查信息")
            st.session_state.land_right_form['变更调查年度'] = st.text_input("变更调查年度", value=st.session_state.land_right_form['变更调查年度'], key=generate_key("变更调查年度"))
            
            st.session_state.land_right_form['批次调查总面积'] = st.text_input("调查总面积(公顷)", value=st.session_state.land_right_form['批次调查总面积'], key=generate_key("批次调查总面积"))
            
            col5, col6 = st.columns(2)
            with col5:
                st.session_state.land_right_form['批次调查农用地'] = st.text_input("调查农用地(公顷)", value=st.session_state.land_right_form['批次调查农用地'], key=generate_key("批次调查农用地"))
                st.session_state.land_right_form['批次调查耕地'] = st.text_input("调查耕地(公顷)", value=st.session_state.land_right_form['批次调查耕地'], key=generate_key("批次调查耕地"))
            with col6:
                st.session_state.land_right_form['批次调查水田'] = st.text_input("调查水田(公顷)", value=st.session_state.land_right_form['批次调查水田'], key=generate_key("批次调查水田"))
                st.session_state.land_right_form['批次调查建设用地'] = st.text_input("调查建设用地(公顷)", value=st.session_state.land_right_form['批次调查建设用地'], key=generate_key("批次调查建设用地"))
            
            st.session_state.land_right_form['批次调查未利用地'] = st.text_input("调查未利用地(公顷)", value=st.session_state.land_right_form['批次调查未利用地'], key=generate_key("批次调查未利用地"))
            
            st.divider()
            
            # 实际申请用地情况
            st.subheader("实际申请用地情况")
            st.session_state.land_right_form['批次实际申请总面积'] = st.text_input("实际申请总面积(公顷)", value=st.session_state.land_right_form['批次实际申请总面积'], key=generate_key("批次实际申请总面积"))
            
            col7, col8 = st.columns(2)
            with col7:
                st.session_state.land_right_form['批次实际农用地'] = st.text_input("实际农用地(公顷)", value=st.session_state.land_right_form['批次实际农用地'], key=generate_key("批次实际农用地"))
                st.session_state.land_right_form['批次实际耕地'] = st.text_input("实际耕地(公顷)", value=st.session_state.land_right_form['批次实际耕地'], key=generate_key("批次实际耕地"))
            with col8:
                st.session_state.land_right_form['批次实际永久基本农田'] = st.text_input("实际永久基本农田(公顷)", value=st.session_state.land_right_form['批次实际永久基本农田'], key=generate_key("批次实际永久基本农田"))
                st.session_state.land_right_form['批次实际建设用地'] = st.text_input("实际建设用地(公顷)", value=st.session_state.land_right_form['批次实际建设用地'], key=generate_key("批次实际建设用地"))
            
            st.session_state.land_right_form['批次实际未利用地'] = st.text_input("实际未利用地(公顷)", value=st.session_state.land_right_form['批次实际未利用地'], key=generate_key("批次实际未利用地"))
            
            st.form_submit_button("生成模板")

    # 生成并显示模板
    if st.button("生成最终模板", key=generate_key("generate_final")):
        template = generate_template()
        st.text_area("生成的模板文本", value=template, height=400, key=generate_key("final_template"))

    # 调用lineinput组件
    try:
        from my_component import lineinput
        # 这里可以根据需要调用lineinput组件
        # lineinput(title="示例组件", default_text="默认文本")
    except ImportError:
        st.warning("无法导入lineinput组件")