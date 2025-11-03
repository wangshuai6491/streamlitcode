# 土地预审单元
import streamlit as st
from datetime import datetime

# 生成唯一的组件key
def generate_key(component_type, index=None):
    """为组件生成唯一的key"""
    timestamp = datetime.now().timestamp()
    if index is not None:
        return f"{component_type}_{index}_{timestamp}"
    return f"{component_type}_{timestamp}"
def page_4():
    # 页面标题
    st.title("土地预审单元")

    # 文件原文折叠面板
    with st.expander("文件原文", expanded=False):
        st.markdown("""### 一、业务指导处室
    行政审批管理处、国土空间用途管制处

    ### 二、审查标准
    1. 已按规定通过用地预审，预审层级应符合要求，应在预审批准后且有效期内批复可研报告或核准项目。
    2. 重新预审的符合有关规定。
    3. 用地规模和用地预审控制规模比对情况应符合有关要求。""")

    # 初始化默认值字典
    def get_default_values():
        return {
            "审批权是否下放": "否",
            "下放依据文件": "",
            "审批权下放部门": "",
            "预审通过年月": "",
            "预审自然资源主管部门": "",
            "预审文号": "",
            "占用永久基本农田且由省级自然资源主管部门预审": "否",
            "立项与预审层级一致": "是",
            "申报用地与预审控制用地规模": "一致",
            "贫困地区类型": "",
            "预审层级": "",
            "不一致原因": "",
            "预审总面积": "",
            "预审农用地": "",
            "预审耕地": "",
            "预审永农": "",
            "超出原因": "",
            "超出面积": "",
            "超出农用地": "",
            "超出耕地": "",
            "超出永农": "",
            "超出比例": "",
            "范围重合度": ""
        }

    # 初始化session_state
    if "pre_approval_form" not in st.session_state:
        st.session_state.pre_approval_form = get_default_values()

    # 动态更新表单值
    for key, default_value in get_default_values().items():
        if key not in st.session_state.pre_approval_form:
            st.session_state.pre_approval_form[key] = default_value

    # 审查内容模板
    st.subheader("三、审查内容模板")
    st.markdown("*土地预审单元不区分单选和批次，用的是同一套模板*")

    # 生成模板文本
    def generate_template():
        fixed_template = """
    〔用地预审情况〕
    该项目符合基本建设投资管理规定。
    """
        
        # 审批权是否下放
        if st.session_state.pre_approval_form['审批权是否下放'] == "是":
            fixed_template += f"按照{st.session_state.pre_approval_form['下放依据文件']}规定，{st.session_state.pre_approval_form['审批权下放部门']}办理，{st.session_state.pre_approval_form['预审通过年月']}，该项目通过{st.session_state.pre_approval_form['预审自然资源主管部门']}用地预审({st.session_state.pre_approval_form['预审文号']})。\n\n"
        else:
            fixed_template += f"{st.session_state.pre_approval_form['预审通过年月']}，{st.session_state.pre_approval_form['预审自然资源主管部门']}通过用地预审（文号：{st.session_state.pre_approval_form['预审文号']}）。\n\n"
        
        # 落实预审意见
        fixed_template += "〔落实预审意见〕\n"
        
        # 占用永久基本农田情况
        if st.session_state.pre_approval_form['占用永久基本农田且由省级自然资源主管部门预审'] == "是":
            fixed_template += f"该项目属于{st.session_state.pre_approval_form['贫困地区类型']}，符合占用永久基本农田条件，由省级自然资源主管部门通过预审。\n"
        else:
            fixed_template += f"该项目由{st.session_state.pre_approval_form['预审层级']}自然资源主管部门通过预审，\n"
        
        # 立项与预审层级一致性
        if st.session_state.pre_approval_form['立项与预审层级一致'] == "是":
            fixed_template += "与批准项目立项政府部门层级一致，用地预审层级符合有关规定。\n"
        else:
            fixed_template += f"立项与预审层级不一致，具体原因：{st.session_state.pre_approval_form['不一致原因']}\n"
        
        # 预审控制规模信息
        fixed_template += f"项目用地预审控制规模{st.session_state.pre_approval_form['预审总面积']}公顷，其中农用地{st.session_state.pre_approval_form['预审农用地']}公顷（耕地{st.session_state.pre_approval_form['预审耕地']}公顷、永久基本农田{st.session_state.pre_approval_form['预审永农']}公顷），\n"
        
        # 申报用地与预审控制用地规模比较
        if st.session_state.pre_approval_form['申报用地与预审控制用地规模'] == "一致":
            fixed_template += "申报用地与预审控制用地规模一致。\n"
        elif st.session_state.pre_approval_form['申报用地与预审控制用地规模'] == "基本一致":
            fixed_template += "申报用地与预审控制用地规模基本一致。\n"
        else:  # 超出规模
            fixed_template += f"因{st.session_state.pre_approval_form['超出原因']}，申报用地超出预审控制规模{st.session_state.pre_approval_form['超出面积']}公顷，其中农用地{st.session_state.pre_approval_form['超出农用地']}公顷（含耕地{st.session_state.pre_approval_form['超出耕地']}公顷、永久基本农田{st.session_state.pre_approval_form['超出永农']}公顷）。\n"
            
            # 超出比例和范围重合度
            if st.session_state.pre_approval_form['超出比例'] or st.session_state.pre_approval_form['范围重合度']:
                fixed_template += f"超出比例：{st.session_state.pre_approval_form['超出比例']}%，范围重合度：{st.session_state.pre_approval_form['范围重合度']}%\n"
            
            # 特殊说明
            try:
                超出比例 = float(st.session_state.pre_approval_form['超出比例'] or '0')
                范围重合度 = float(st.session_state.pre_approval_form['范围重合度'] or '100')
                if 超出比例 >= 10 or 范围重合度 < 80:
                    fixed_template += "（建设项目申请总面积超出用地预审总面积达到10%且范围重合度低于80%，需对用地变化情况的必要性、合理性作出说明。）\n"
            except:
                pass
        
        return fixed_template

    # 显示表单
    with st.form(key=generate_key("pre_approval_form")):
        # 用地预审情况
        st.subheader("用地预审情况")
        
        # 审批权是否下放
        st.session_state.pre_approval_form['审批权是否下放'] = st.radio(
            "审批权是否下放",
            options=["是", "否"],
            index=0 if st.session_state.pre_approval_form['审批权是否下放'] == "是" else 1,
            key=generate_key("审批权是否下放")
        )
        
        if st.session_state.pre_approval_form['审批权是否下放'] == "是":
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.pre_approval_form['下放依据文件'] = st.text_input("下放依据文件", value=st.session_state.pre_approval_form['下放依据文件'], key=generate_key("下放依据文件"))
                st.session_state.pre_approval_form['审批权下放部门'] = st.text_input("审批权下放至部门", value=st.session_state.pre_approval_form['审批权下放部门'], key=generate_key("审批权下放部门"))
            with col2:
                st.session_state.pre_approval_form['预审通过年月'] = st.text_input("预审通过年月（*年*月）", value=st.session_state.pre_approval_form['预审通过年月'], key=generate_key("预审通过年月"))
                st.session_state.pre_approval_form['预审自然资源主管部门'] = st.text_input("预审自然资源主管部门", value=st.session_state.pre_approval_form['预审自然资源主管部门'], key=generate_key("预审自然资源主管部门"))
            st.session_state.pre_approval_form['预审文号'] = st.text_input("预审文号", value=st.session_state.pre_approval_form['预审文号'], key=generate_key("预审文号"))
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.pre_approval_form['预审通过年月'] = st.text_input("预审通过年月（*年*月）", value=st.session_state.pre_approval_form['预审通过年月'], key=generate_key("预审通过年月"))
            with col2:
                st.session_state.pre_approval_form['预审自然资源主管部门'] = st.text_input("预审自然资源主管部门", value=st.session_state.pre_approval_form['预审自然资源主管部门'], key=generate_key("预审自然资源主管部门"))
            st.session_state.pre_approval_form['预审文号'] = st.text_input("预审文号", value=st.session_state.pre_approval_form['预审文号'], key=generate_key("预审文号"))
        
        st.divider()
        
        # 落实预审意见
        st.subheader("落实预审意见")
        
        # 用户选择判断区
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.pre_approval_form['占用永久基本农田且由省级自然资源主管部门预审'] = st.radio(
                "是否占用永久基本农田且由省级自然资源主管部门预审？",
                options=["是", "否"],
                index=0 if st.session_state.pre_approval_form['占用永久基本农田且由省级自然资源主管部门预审'] == "是" else 1,
                key=generate_key("占用永久基本农田且由省级自然资源主管部门预审"),
                horizontal=True
            )
        with col2:
            st.session_state.pre_approval_form['立项与预审层级一致'] = st.radio(
                "立项与预审层级一致：",
                options=["是", "否"],
                index=0 if st.session_state.pre_approval_form['立项与预审层级一致'] == "是" else 1,
                key=generate_key("立项与预审层级一致"),
                horizontal=True
            )
        
        st.session_state.pre_approval_form['申报用地与预审控制用地规模'] = st.radio(
            "申报用地与预审控制用地规模：",
            options=["一致", "基本一致", "超出规模"],
            index={
                "一致": 0,
                "基本一致": 1,
                "超出规模": 2
            }.get(st.session_state.pre_approval_form['申报用地与预审控制用地规模'], 0),
            key=generate_key("申报用地与预审控制用地规模"),
            horizontal=True
        )
        
        # 用户输入交互区
        if st.session_state.pre_approval_form['占用永久基本农田且由省级自然资源主管部门预审'] == "是":
            st.session_state.pre_approval_form['贫困地区类型'] = st.text_input(
                "贫困地区类型", 
                value=st.session_state.pre_approval_form['贫困地区类型'], 
                key=generate_key("贫困地区类型"),
                help="例如：深度贫困地区/集中连片特因地区/国家扶贫开发工作重点县省级以下基础设施、易地扶贫搬迁、民生发展项目"
            )
        else:
            st.session_state.pre_approval_form['预审层级'] = st.text_input(
                "预审层级", 
                value=st.session_state.pre_approval_form['预审层级'], 
                key=generate_key("预审层级")
            )
        
        if st.session_state.pre_approval_form['立项与预审层级一致'] == "否":
            st.session_state.pre_approval_form['不一致原因'] = st.text_input(
                "不一致原因", 
                value=st.session_state.pre_approval_form['不一致原因'], 
                key=generate_key("不一致原因")
            )
        
        # 预审控制规模
        st.markdown("#### 预审控制规模")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.session_state.pre_approval_form['预审总面积'] = st.text_input(
                "预审总面积（公顷）", 
                value=st.session_state.pre_approval_form['预审总面积'], 
                key=generate_key("预审总面积")
            )
        with col2:
            st.session_state.pre_approval_form['预审农用地'] = st.text_input(
                "预审农用地（公顷）", 
                value=st.session_state.pre_approval_form['预审农用地'], 
                key=generate_key("预审农用地")
            )
        with col3:
            st.session_state.pre_approval_form['预审耕地'] = st.text_input(
                "预审耕地（公顷）", 
                value=st.session_state.pre_approval_form['预审耕地'], 
                key=generate_key("预审耕地")
            )
        with col4:
            st.session_state.pre_approval_form['预审永农'] = st.text_input(
                "预审永农（公顷）", 
                value=st.session_state.pre_approval_form['预审永农'], 
                key=generate_key("预审永农")
            )
        
        # 超出规模情况
        if st.session_state.pre_approval_form['申报用地与预审控制用地规模'] == "超出规模":
            st.markdown("#### 超出规模情况")
            st.session_state.pre_approval_form['超出原因'] = st.text_input(
                "超出原因", 
                value=st.session_state.pre_approval_form['超出原因'], 
                key=generate_key("超出原因")
            )
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.session_state.pre_approval_form['超出面积'] = st.text_input(
                    "超出面积（公顷）", 
                    value=st.session_state.pre_approval_form['超出面积'], 
                    key=generate_key("超出面积")
                )
            with col2:
                st.session_state.pre_approval_form['超出农用地'] = st.text_input(
                    "超出农用地（公顷）", 
                    value=st.session_state.pre_approval_form['超出农用地'], 
                    key=generate_key("超出农用地")
                )
            with col3:
                st.session_state.pre_approval_form['超出耕地'] = st.text_input(
                    "超出耕地（公顷）", 
                    value=st.session_state.pre_approval_form['超出耕地'], 
                    key=generate_key("超出耕地")
                )
            with col4:
                st.session_state.pre_approval_form['超出永农'] = st.text_input(
                    "超出永农（公顷）", 
                    value=st.session_state.pre_approval_form['超出永农'], 
                    key=generate_key("超出永农")
                )
            
            # 超出比例和范围重合度
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.pre_approval_form['超出比例'] = st.text_input(
                    "超出比例（%）", 
                    value=st.session_state.pre_approval_form['超出比例'], 
                    key=generate_key("超出比例")
                )
            with col2:
                st.session_state.pre_approval_form['范围重合度'] = st.text_input(
                    "范围重合度（%）", 
                    value=st.session_state.pre_approval_form['范围重合度'], 
                    key=generate_key("范围重合度")
                )
        
        st.form_submit_button("更新表单")

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