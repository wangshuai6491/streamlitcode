import streamlit as st

@st.fragment
def st_radio_buttons(
    options,
    state_key,
    label=None,
    key=None,
    use_container_width=True
):
    """
    显示一组按钮，支持单选，状态通过 st.session_state 管理。
    
    Args:
        options (list): 可以是字符串列表如 ["来信", "来访"] 或元组列表 [(display_text, value)]
        state_key (str): 用于 st.session_state 的键名，如 "selected_contact"
        label (str, optional): 整体标签，显示在按钮组上方
        key (str, optional): Streamlit 组件的唯一键（用于避免冲突）
        use_container_width (bool): 是否占满容器宽度
    
    Returns:
        str or None: 当前选中的值，未选中则为 None
    """
    # 初始化状态
    if state_key not in st.session_state:
        st.session_state[state_key] = None

    # 回调函数：更新选中状态
    def set_selected(value):
        st.session_state[state_key] = value
        # 在回调函数中，Streamlit会自动处理片段的重渲染

    # 显示标签（如果有）
    if label:
        st.markdown(f"**{label}**")

    # 处理不同格式的选项
    processed_options = []
    for opt in options:
        if isinstance(opt, tuple):
            # 如果是元组，直接使用
            processed_options.append(opt)
        else:
            # 如果是字符串，将其同时作为显示文本和值
            processed_options.append((opt, opt))

    # 创建列（按钮数量 = 选项数量）
    cols = st.columns(len(processed_options))

    # 为每个选项创建按钮
    for i, (display_text, value) in enumerate(processed_options):
        with cols[i]:
            is_selected = st.session_state[state_key] == value
            st.button(
                display_text,
                on_click=set_selected,
                args=(value,),
                type="primary" if is_selected else "secondary",
                use_container_width=use_container_width,
                key=f"{key}_{i}" if key else None
            )

    # 返回当前选中值
    return st.session_state[state_key]

# 创建结果显示的容器并使用fragment装饰
result_container = st.container()

# 使用fragment装饰器将结果显示部分也做成独立片段
@st.fragment
# 当session state更新时，通过fragment自动重渲染更新结果显示
def update_results():
    with result_container:
        result_container.empty()
        if st.session_state.get("payment_method"):
            st.write(f"支付方式已选：{st.session_state.payment_method}")
        if st.session_state.get("selected_contact"):
            st.success(f"你选择了：**{st.session_state.selected_contact}**")

# 初始化结果显示
update_results()

# 调用按钮组件（使用新的字符串列表格式）
selected_type = st_radio_buttons(
    options=["来信","来访","网上信访","电话信访"],
    state_key="petition_type",
    label="选择信访类型",
    use_container_width=True
)

selected_payment = st_radio_buttons(
    options=[
        ("💳 信用卡", "credit_card"),
        ("📱 支付宝", "alipay"),
        ("💰 现金", "cash")
    ],
    state_key="payment_method",
    label="选择支付方式",
    use_container_width=True
)

selected_mode = st_radio_buttons(
    options=[
        ("🔍 查看", "view"),
        ("✏️ 编辑", "edit"),
        ("🗑️ 删除", "delete")
    ],
    state_key="operation_mode",
    use_container_width=False  # 不占满宽度
)

# 调用通用函数
selected_contact = st_radio_buttons(
    options=[
        ("📧 来信", "来信"),
        ("🌐 网络", "网络"),
        ("📞 电话", "电话")
    ],
    state_key="selected_contact",
    label="请选择联系方式"
)