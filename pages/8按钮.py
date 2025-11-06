import streamlit as st

# 初始化 session_state（如果不存在）
if "is_active" not in st.session_state:
    st.session_state.is_active = False

# 定义按钮点击后的回调函数
def toggle_state():
    st.session_state.is_active = not st.session_state.is_active

# 根据状态决定按钮样式和文字
button_text = "✅ 已启用" if st.session_state.is_active else "🔴 已禁用"
button_type = "primary" if st.session_state.is_active else "secondary"

# 显示按钮
st.button(
    button_text,
    on_click=toggle_state,
    type=button_type,
    use_container_width=True
)

# 显示当前状态
st.write(f"当前状态: {'启用' if st.session_state.is_active else '禁用'}")