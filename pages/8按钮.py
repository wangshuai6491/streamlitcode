import streamlit as st

# 初始化 session_state（如果不存在）
if "selected_contact" not in st.session_state:
    st.session_state.selected_contact = None  # 初始状态：无选中

# 定义回调函数：点击按钮时更新选中状态
def set_selected(contact_type):
    st.session_state.selected_contact = contact_type

# 创建三列布局
col1, col2, col3 = st.columns(3)

# 1. 来信按钮
with col1:
    is_selected = st.session_state.selected_contact == "来信"
    st.button(
        "📧 来信",
        on_click=set_selected,
        args=("来信",),
        type="primary" if is_selected else "secondary",
        use_container_width=True
    )

# 2. 网络按钮
with col2:
    is_selected = st.session_state.selected_contact == "网络"
    st.button(
        "🌐 网络",
        on_click=set_selected,
        args=("网络",),
        type="primary" if is_selected else "secondary",
        use_container_width=True
    )

# 3. 电话按钮
with col3:
    is_selected = st.session_state.selected_contact == "电话"
    st.button(
        "📞 电话",
        on_click=set_selected,
        args=("电话",),
        type="primary" if is_selected else "secondary",
        use_container_width=True
    )

# 显示当前选中状态
if st.session_state.selected_contact:
    st.success(f"当前选中的联系方式：**{st.session_state.selected_contact}**")
else:
    st.info("请选择一种联系方式")

score = st.select_slider("选择分数", options=[0, 20, 40, 60, 80, 100])