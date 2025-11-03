import streamlit as st
from datetime import datetime

# 生成唯一的组件key
def generate_key(component_type, index=None):
    """为组件生成唯一的key"""
    timestamp = datetime.now().timestamp()
    if index is not None:
        return f"{component_type}_{index}_{timestamp}"
    return f"{component_type}_{timestamp}"
def page_3():
    # 页面标题
    st.title("计划指标单元")

    # 文件原文折叠面板
    with st.expander("文件原文", expanded=False):
        st.markdown("""### 一、业务指导处室
    国土空间用途管制处

    ### 二、审查标准
    1. 土地利用计划指标安排应符合自然资源部和省自然资源厅年度土地利用计划管理规定。""")

    # 初始化默认值字典 - 单独选址
    def get_single_default_values():
        return {
            "转用总面积": "",
            "农用地面积": "",
            "未利用地面积": "",
            "列入重大项目清单": "否",
            "涉及违法用地": "否",
            "重大项目层级": "",
            "违法总面积": "",
            "违法农用地": "",
            "违法未利用地": "",
            "违法指标来源": "",
            "剩余总面积": "",
            "剩余农用地": "",
            "剩余未利用地": "",
            "县名称": "",
            "指标类型": ""
        }

    # 初始化默认值字典 - 批次用地
    def get_batch_default_values():
        return {
            "转用总面积": "",
            "农用地面积": "",
            "未利用地面积": "",
            "使用专项计划": "否",
            "专项指标类型": "",
            "县名称": ""
        }

    # 初始化session_state
    if "land_use_plan_single" not in st.session_state:
        st.session_state.land_use_plan_single = get_single_default_values()

    if "land_use_plan_batch" not in st.session_state:
        st.session_state.land_use_plan_batch = get_batch_default_values()

    # 动态更新表单值
    for key, default_value in get_single_default_values().items():
        if key not in st.session_state.land_use_plan_single:
            st.session_state.land_use_plan_single[key] = default_value

    for key, default_value in get_batch_default_values().items():
        if key not in st.session_state.land_use_plan_batch:
            st.session_state.land_use_plan_batch[key] = default_value

    # 审查内容模板
    st.subheader("三、审查内容模板")

    # 用地类型选择
    land_type = st.radio(
        "用地类型",
        options=["单独选址", "批次用地"],
        key=generate_key("land_type"),
        horizontal=True
    )

    # 生成单独选址模板文本
    def generate_single_template():
        template = "〔土地利用计划〕\n"
        template += f"项目用地符合土地利用计划管理规定。该项目用地中{st.session_state.land_use_plan_single['转用总面积']}公顷（农用地{st.session_state.land_use_plan_single['农用地面积']}公顷、未利用地{st.session_state.land_use_plan_single['未利用地面积']}公顷）需转为建设用地。\n\n"
        
        if st.session_state.land_use_plan_single['列入重大项目清单'] == "是":
            if st.session_state.land_use_plan_single['涉及违法用地'] == "是":
                template += f"已列入{st.session_state.land_use_plan_single['重大项目层级']}人民政府重大项目用地清单，因涉及违法用地{st.session_state.land_use_plan_single['违法总面积']}公顷（农用地{st.session_state.land_use_plan_single['违法农用地']}公顷、未利用地{st.session_state.land_use_plan_single['违法未利用地']}公顷），\n"
                template += f"按照年度计划管理文件要求，涉及违法用地的{st.session_state.land_use_plan_single['违法总面积']}公顷使用{st.session_state.land_use_plan_single['违法指标来源']}；\n"
                template += f"剩余部分{st.session_state.land_use_plan_single['剩余总面积']}公顷（农用地{st.session_state.land_use_plan_single['剩余农用地']}公顷、未利用地{st.session_state.land_use_plan_single['剩余未利用地']}公顷），\n"
                template += "申请由国家配置计划。"
            else:
                template += f"已列入{st.session_state.land_use_plan_single['重大项目层级']}人民政府重大项目用地清单，申请由国家配置计划。"
        else:
            template += "未列入国家重大项目清单和省级人民政府重大项目用地清单，\n"
            template += f"按规定使用{st.session_state.land_use_plan_single['县名称']}本年度存量土地处置规模为基础核定的{st.session_state.land_use_plan_single['指标类型']}。"
        
        return template

    # 生成批次用地模板文本
    def generate_batch_template():
        template = "〔土地利用计划〕\n"
        template += f"该批次用地符合土地利用计划管理规定。批次用地中{st.session_state.land_use_plan_batch['转用总面积']}公顷（农用地{st.session_state.land_use_plan_batch['农用地面积']}公顷、未利用地{st.session_state.land_use_plan_batch['未利用地面积']}公顷）需转为建设用地，\n"
        
        if st.session_state.land_use_plan_batch['使用专项计划'] == "是":
            template += f"使用{st.session_state.land_use_plan_batch['专项指标类型']}。"
        else:
            template += f"按规定使用{st.session_state.land_use_plan_batch['县名称']}以本年度存量土地处置规模为基础核定的计划指标。"
        
        return template

    # 显示表单
    if land_type == "单独选址":
        st.subheader("(一)单独选址")
        with st.form(key=generate_key("single_location_form")):
            # 内容块1
            st.markdown("#### 转用面积信息")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.land_use_plan_single['转用总面积'] = st.text_input(
                    "转用总面积（公顷）", 
                    value=st.session_state.land_use_plan_single['转用总面积'], 
                    key=generate_key("转用总面积")
                )
            with col2:
                st.session_state.land_use_plan_single['农用地面积'] = st.text_input(
                    "农用地面积（公顷）", 
                    value=st.session_state.land_use_plan_single['农用地面积'], 
                    key=generate_key("农用地面积")
                )
            with col3:
                st.session_state.land_use_plan_single['未利用地面积'] = st.text_input(
                    "未利用地面积（公顷）", 
                    value=st.session_state.land_use_plan_single['未利用地面积'], 
                    key=generate_key("未利用地面积")
                )
            
            # 条件判断选择区域
            st.markdown("#### 项目清单及违法用地情况")
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.land_use_plan_single['列入重大项目清单'] = st.radio(
                    "是否列入国家/省重大项目清单", 
                    options=["是", "否"],
                    index=0 if st.session_state.land_use_plan_single['列入重大项目清单'] == "是" else 1,
                    key=generate_key("列入重大项目清单"),
                    horizontal=True
                )
            with col2:
                st.session_state.land_use_plan_single['涉及违法用地'] = st.radio(
                    "是否涉及违法用地", 
                    options=["是", "否"],
                    index=0 if st.session_state.land_use_plan_single['涉及违法用地'] == "是" else 1,
                    key=generate_key("涉及违法用地"),
                    horizontal=True
                )
            
            # 如果列入重大项目清单
            if st.session_state.land_use_plan_single['列入重大项目清单'] == "是":
                st.markdown("#### 重大项目信息")
                st.session_state.land_use_plan_single['重大项目层级'] = st.text_input(
                    "重大项目层级", 
                    value=st.session_state.land_use_plan_single['重大项目层级'], 
                    key=generate_key("重大项目层级"),
                    help="例如：国家级、省级等"
                )
                
                # 如果涉及违法用地
                if st.session_state.land_use_plan_single['涉及违法用地'] == "是":
                    st.markdown("#### 违法用地情况")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.session_state.land_use_plan_single['违法总面积'] = st.text_input(
                            "违法总面积（公顷）", 
                            value=st.session_state.land_use_plan_single['违法总面积'], 
                            key=generate_key("违法总面积")
                        )
                    with col2:
                        st.session_state.land_use_plan_single['违法农用地'] = st.text_input(
                            "违法农用地（公顷）", 
                            value=st.session_state.land_use_plan_single['违法农用地'], 
                            key=generate_key("违法农用地")
                        )
                    with col3:
                        st.session_state.land_use_plan_single['违法未利用地'] = st.text_input(
                            "违法未利用地（公顷）", 
                            value=st.session_state.land_use_plan_single['违法未利用地'], 
                            key=generate_key("违法未利用地")
                        )
                    
                    st.session_state.land_use_plan_single['违法指标来源'] = st.text_input(
                        "违法指标来源", 
                        value=st.session_state.land_use_plan_single['违法指标来源'], 
                        key=generate_key("违法指标来源")
                    )
                    
                    st.markdown("#### 剩余面积信息")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.session_state.land_use_plan_single['剩余总面积'] = st.text_input(
                            "剩余总面积（公顷）", 
                            value=st.session_state.land_use_plan_single['剩余总面积'], 
                            key=generate_key("剩余总面积")
                        )
                    with col2:
                        st.session_state.land_use_plan_single['剩余农用地'] = st.text_input(
                            "剩余农用地（公顷）", 
                            value=st.session_state.land_use_plan_single['剩余农用地'], 
                            key=generate_key("剩余农用地")
                        )
                    with col3:
                        st.session_state.land_use_plan_single['剩余未利用地'] = st.text_input(
                            "剩余未利用地（公顷）", 
                            value=st.session_state.land_use_plan_single['剩余未利用地'], 
                            key=generate_key("剩余未利用地")
                        )
            # 如果未列入重大项目清单
            else:
                st.markdown("#### 县级指标信息")
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.land_use_plan_single['县名称'] = st.text_input(
                        "县名称", 
                        value=st.session_state.land_use_plan_single['县名称'], 
                        key=generate_key("县名称")
                    )
                with col2:
                    st.session_state.land_use_plan_single['指标类型'] = st.text_input(
                        "指标类型", 
                        value=st.session_state.land_use_plan_single['指标类型'], 
                        key=generate_key("指标类型")
                    )
            
            st.form_submit_button("更新表单")
    else:  # 批次用地
        st.subheader("(二)批次用地")
        with st.form(key=generate_key("batch_land_form")):
            # 内容块1
            st.markdown("#### 转用面积信息")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.land_use_plan_batch['转用总面积'] = st.text_input(
                    "转用总面积（公顷）", 
                    value=st.session_state.land_use_plan_batch['转用总面积'], 
                    key=generate_key("转用总面积")
                )
            with col2:
                st.session_state.land_use_plan_batch['农用地面积'] = st.text_input(
                    "农用地面积（公顷）", 
                    value=st.session_state.land_use_plan_batch['农用地面积'], 
                    key=generate_key("农用地面积")
                )
            with col3:
                st.session_state.land_use_plan_batch['未利用地面积'] = st.text_input(
                    "未利用地面积（公顷）", 
                    value=st.session_state.land_use_plan_batch['未利用地面积'], 
                    key=generate_key("未利用地面积")
                )
            
            # 是否使用专项计划
            st.markdown("#### 计划指标类型")
            st.session_state.land_use_plan_batch['使用专项计划'] = st.radio(
                "是否使用专项计划", 
                options=["是", "否"],
                index=0 if st.session_state.land_use_plan_batch['使用专项计划'] == "是" else 1,
                key=generate_key("使用专项计划"),
                horizontal=True
            )
            
            if st.session_state.land_use_plan_batch['使用专项计划'] == "是":
                st.session_state.land_use_plan_batch['专项指标类型'] = st.text_input(
                    "专项指标类型", 
                    value=st.session_state.land_use_plan_batch['专项指标类型'], 
                    key=generate_key("专项指标类型")
                )
            else:
                st.session_state.land_use_plan_batch['县名称'] = st.text_input(
                    "县名称", 
                    value=st.session_state.land_use_plan_batch['县名称'], 
                    key=generate_key("县名称")
                )
            
            st.form_submit_button("更新表单")

    # 生成并显示模板
    if st.button("生成最终模板", key=generate_key("generate_final")):
        if land_type == "单独选址":
            template = generate_single_template()
        else:
            template = generate_batch_template()
        st.text_area("生成的模板文本", value=template, height=400, key=generate_key("final_template"))

    # 调用lineinput组件
    try:
        from my_component import lineinput
        # 这里可以根据需要调用lineinput组件
        # lineinput(title="示例组件", default_text="默认文本")
    except ImportError:
        st.warning("无法导入lineinput组件")