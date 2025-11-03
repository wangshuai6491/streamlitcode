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
def page_2():
    # 页面标题
    st.title("审核许可单元")

    # 文件原文折叠面板
    with st.expander("文件原文", expanded=False):
        st.markdown("""### 一、业务指导处室
        国土空间用途管制处

        ### 二、审查标准
        1. 涉及占用林地的，应当取得使用林地审核同意书，且应当在有效期内。涉及占用各类保护地的，需取得相关主管部门同意的意见。
        2. 采矿用地需取得采矿许可证。""")

    # 初始化默认值字典 - 单独选址
    def get_single_default_values():
        return {
            "涉及占用林地": "否",
            "占用林地面积": "",
            "林地手续文号": "",
            "采矿许可年月": "",
            "核发部门": "",
            "矿种": "",
            "采矿许可证证号": "",
            "涉及保护地": "否",
            "保护地名称": "",
            "保护地面积": "",
            "保护地主管部门": "",
            "保护地同意文号": ""
        }

    # 初始化默认值字典 - 批次用地
    def get_batch_default_values():
        return {
            "涉及林地": "否",
            "林地面积": "",
            "林地审核状态": "已获批",
            "林草部门": "",
            "涉及保护地": "否",
            "保护地名称": "",
            "保护地面积": "",
            "保护地主管部门": "",
            "保护地同意文号": ""
        }

    # 初始化session_state
    if "approval_unit_single" not in st.session_state:
        st.session_state.approval_unit_single = get_single_default_values()

    if "approval_unit_batch" not in st.session_state:
        st.session_state.approval_unit_batch = get_batch_default_values()

    # 动态更新表单值
    for key, default_value in get_single_default_values().items():
        if key not in st.session_state.approval_unit_single:
            st.session_state.approval_unit_single[key] = default_value

    for key, default_value in get_batch_default_values().items():
        if key not in st.session_state.approval_unit_batch:
            st.session_state.approval_unit_batch[key] = default_value

    # 审查内容模板
    st.subheader("三、审查内容模板")

    # 用地类型选择
    land_type = button_group(
        label="",
        options=[{"label": "单独选址", "value": "单独选址"}, {"label": "批次用地", "value": "批次用地"}],
        default_value="单独选址",
        key=generate_key("land_type")
    )

    # 生成单独选址模板文本
    def generate_single_template():
        template = "〔有关审核许可手续〕\n\n"
        
        # 林地占用情况
        if st.session_state.approval_unit_single['涉及占用林地'] == "是":
            template += f"项目涉及占用林草部门管理范围内林地{st.session_state.approval_unit_single['占用林地面积']}公顷，已按要求办理林地相关手续（文号：{st.session_state.approval_unit_single['林地手续文号']}）。\n\n"
        else:
            template += "项目不涉及占用林草部门管理范围内林地。\n\n"
        
        # 采矿许可证信息
        template += "〔采矿许可证信息〕\n"
        template += f"建设单位已于{st.session_state.approval_unit_single['采矿许可年月']}取得{st.session_state.approval_unit_single['核发部门']}核发的{st.session_state.approval_unit_single['矿种']}采矿许可证（证号：{st.session_state.approval_unit_single['采矿许可证证号']}）。\n\n"
        
        # 保护地情况
        template += "〔保护地情况〕\n"
        if st.session_state.approval_unit_single['涉及保护地'] == "是":
            template += f"项目用地涉及{st.session_state.approval_unit_single['保护地名称']}，面积{st.session_state.approval_unit_single['保护地面积']}公顷，已取得{st.session_state.approval_unit_single['保护地主管部门']}同意的意见（文号：{st.session_state.approval_unit_single['保护地同意文号']}）。\n"
        else:
            template += "项目用地不涉及各类保护地。\n"
        
        return template

    # 生成批次用地模板文本
    def generate_batch_template():
        template = "〔林地审核情况〕\n"
        
        # 林地审核情况
        if st.session_state.approval_unit_batch['涉及林地'] == "是":
            template += f"该批次用地涉及林地{st.session_state.approval_unit_batch['林地面积']}公顷，\n"
            if st.session_state.approval_unit_batch['林地审核状态'] == "已获批":
                template += f"已取得{st.session_state.approval_unit_batch['林草部门']}《林地审核同意书》。\n\n"
            elif st.session_state.approval_unit_batch['林地审核状态'] == "正在办理":
                template += f"相关材料已报{st.session_state.approval_unit_batch['林草部门']}待批，我局承诺在用地上报省政府前补充《林地审核同意书》。\n\n"
        else:
            template += "该批次不涉及占用林草部门管理范围内林地。\n\n"
        
        # 保护地情况
        template += "〔保护地情况〕\n"
        if st.session_state.approval_unit_batch['涉及保护地'] == "是":
            template += f"项目用地涉及{st.session_state.approval_unit_batch['保护地名称']}，面积{st.session_state.approval_unit_batch['保护地面积']}公顷，已取得{st.session_state.approval_unit_batch['保护地主管部门']}同意的意见（文号：{st.session_state.approval_unit_batch['保护地同意文号']}）。\n"
        else:
            template += "项目用地不涉及各类保护地。\n"
        
        return template

    # 显示表单
    if land_type == "单独选址":
        st.subheader("(一)单独选址")
        with st.form(key=generate_key("single_location_form")):
            # 涉及占用林地判断选择区块
            st.markdown("#### 林地占用情况")
            st.session_state.approval_unit_single['涉及占用林地'] = button_group(
                label="",
                options=[{"label": "是", "value": "是"}, {"label": "否", "value": "否"}],
                default_value="否",
                key=generate_key("涉及占用林地")
            )
            
            if st.session_state.approval_unit_single['涉及占用林地'] == "是":
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.approval_unit_single['占用林地面积'] = st.text_input(
                        "占用林地面积（公顷）", 
                        value=st.session_state.approval_unit_single['占用林地面积'], 
                        key=generate_key("占用林地面积")
                    )
                with col2:
                    st.session_state.approval_unit_single['林地手续文号'] = st.text_input(
                        "林地手续文号", 
                        value=st.session_state.approval_unit_single['林地手续文号'], 
                        key=generate_key("林地手续文号")
                    )
            
            st.divider()
            
            # 采矿许可证信息区块
            st.markdown("#### 采矿许可证信息")
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.approval_unit_single['采矿许可年月'] = st.text_input(
                    "采矿许可年月（例如：2025年1月）", 
                    value=st.session_state.approval_unit_single['采矿许可年月'], 
                    key=generate_key("采矿许可年月")
                )
                st.session_state.approval_unit_single['核发部门'] = st.text_input(
                    "核发部门", 
                    value=st.session_state.approval_unit_single['核发部门'], 
                    key=generate_key("核发部门")
                )
            with col2:
                st.session_state.approval_unit_single['矿种'] = st.text_input(
                    "矿种", 
                    value=st.session_state.approval_unit_single['矿种'], 
                    key=generate_key("矿种")
                )
                st.session_state.approval_unit_single['采矿许可证证号'] = st.text_input(
                    "采矿许可证证号", 
                    value=st.session_state.approval_unit_single['采矿许可证证号'], 
                    key=generate_key("采矿许可证证号")
                )
            
            st.divider()
            
            # 涉及保护地判断选择区块
            st.markdown("#### 保护地情况")
            st.session_state.approval_unit_single['涉及保护地'] = button_group(
                label="",
                options=[{"label": "是", "value": "是"}, {"label": "否", "value": "否"}],
                default_value="否",
                key=generate_key("涉及保护地")
            )
            
            if st.session_state.approval_unit_single['涉及保护地'] == "是":
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.approval_unit_single['保护地名称'] = st.text_input(
                        "保护地名称", 
                        value=st.session_state.approval_unit_single['保护地名称'], 
                        key=generate_key("保护地名称")
                    )
                    st.session_state.approval_unit_single['保护地面积'] = st.text_input(
                        "保护地面积（公顷）", 
                        value=st.session_state.approval_unit_single['保护地面积'], 
                        key=generate_key("保护地面积")
                    )
                with col2:
                    st.session_state.approval_unit_single['保护地主管部门'] = st.text_input(
                        "保护地主管部门", 
                        value=st.session_state.approval_unit_single['保护地主管部门'], 
                        key=generate_key("保护地主管部门")
                    )
                    st.session_state.approval_unit_single['保护地同意文号'] = st.text_input(
                        "保护地同意文号", 
                        value=st.session_state.approval_unit_single['保护地同意文号'], 
                        key=generate_key("保护地同意文号")
                    )
            
            st.form_submit_button("更新表单")
    else:  # 批次用地
        st.subheader("(二)批次用地")
        with st.form(key=generate_key("batch_land_form")):
            # 林地审核情况区块
            st.markdown("#### 林地审核情况")
            st.session_state.approval_unit_batch['涉及林地'] = button_group(
                label="",
                options=[{"label": "是", "value": "是"}, {"label": "否", "value": "否"}],
                default_value="否",
                key=generate_key("涉及林地")
            )
            
            if st.session_state.approval_unit_batch['涉及林地'] == "是":
                st.session_state.approval_unit_batch['林地面积'] = st.text_input(
                    "林地面积（公顷）", 
                    value=st.session_state.approval_unit_batch['林地面积'], 
                    key=generate_key("林地面积")
                )
                
                st.markdown("**《林地审核同意书》状态：**")
                st.session_state.approval_unit_batch['林地审核状态'] = button_group(
                    label="",
                    options=[{"label": "已获批", "value": "已获批"}, {"label": "正在办理", "value": "正在办理"}],
                    default_value="已获批",
                    key=generate_key("林地审核状态")
                )
                
                st.session_state.approval_unit_batch['林草部门'] = st.text_input(
                    "林草部门", 
                    value=st.session_state.approval_unit_batch['林草部门'], 
                    key=generate_key("林草部门")
                )
            
            st.divider()
            
            # 保护地情况区块
            st.markdown("#### 保护地情况")
            st.session_state.approval_unit_batch['涉及保护地'] = button_group(
                label="",
                options=[{"label": "是", "value": "是"}, {"label": "否", "value": "否"}],
                default_value="否",
                key=generate_key("涉及保护地")
            )
            
            if st.session_state.approval_unit_batch['涉及保护地'] == "是":
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.approval_unit_batch['保护地名称'] = st.text_input(
                        "保护地名称", 
                        value=st.session_state.approval_unit_batch['保护地名称'], 
                        key=generate_key("保护地名称")
                    )
                    st.session_state.approval_unit_batch['保护地面积'] = st.text_input(
                        "保护地面积（公顷）", 
                        value=st.session_state.approval_unit_batch['保护地面积'], 
                        key=generate_key("保护地面积")
                    )
                with col2:
                    st.session_state.approval_unit_batch['保护地主管部门'] = st.text_input(
                        "保护地主管部门", 
                        value=st.session_state.approval_unit_batch['保护地主管部门'], 
                        key=generate_key("保护地主管部门")
                    )
                    st.session_state.approval_unit_batch['保护地同意文号'] = st.text_input(
                        "保护地同意文号", 
                        value=st.session_state.approval_unit_batch['保护地同意文号'], 
                        key=generate_key("保护地同意文号")
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