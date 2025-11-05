# test_button_group.py
import streamlit as st
from typing import List, Dict, Any, Optional

def button_group(
    label: str,
    options: List[Dict[str, Any]],
    default: Optional[Any] = None,
    key: Optional[str] = None
) -> Any:
    """互斥按钮组，点击高亮（醒目蓝）"""
    if not options:
        raise ValueError("options 不能为空列表")
    for opt in options:
        if "label" not in opt or "value" not in opt:
            raise ValueError("每个 option 必须包含 'label' 和 'value'")

    if key is None:
        key = f"button_group_{label}"

    values = [opt["value"] for opt in options]
    if default is None:
        default = values[0]
    elif default not in values:
        raise ValueError(f"default 值 {default} 不在 options 的 value 中")

    if key not in st.session_state:
        st.session_state[key] = default

    if label:
        st.markdown(f"**{label}**")

    # ---------- 核心样式 ----------
    current_value = st.session_state[key]
    css = ""
    for opt in options:
        btn_key = f"{key}_{opt['value']}"
        is_active = opt["value"] == current_value
        bg_color   = "#0066ff" if is_active else "#f7f7f7"
        text_color = "#ffffff" if is_active else "#333333"
        border_color = bg_color
        weight     = "bold" if is_active else "normal"

        css += f"""
        /* 普通状态 */
        button[data-testid="baseButton-secondary"][data-key="{btn_key}"] {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            border-color: {border_color} !important;
            font-weight: {weight} !important;
            transition: all 0.2s ease;
        }}
        /* 点击/焦点状态：强制覆盖系统浅灰 */
        button[data-testid="baseButton-secondary"][data-key="{btn_key}"]:focus {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            border-color: {border_color} !important;
        }}
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # ---------- 创建按钮 ----------
    cols = st.columns(len(options))
    for col, opt in zip(cols, options):
        with col:
            if st.button(
                opt["label"],
                key=f"{key}_{opt['value']}",
                use_container_width=True
            ):
                st.session_state[key] = opt["value"]
                # 不手动 rerun，Streamlit 会自动 rerun
    return st.session_state[key]

# ------------------ 演示 ------------------
st.set_page_config(page_title="Button Group Demo", layout="centered")
st.title("🔘 Button Group 高亮测试")

choice = button_group(
    label="请选择你最喜欢的水果：",
    options=[
        {"label": "🍎 苹果", "value": "apple"},
        {"label": "🍌 香蕉", "value": "banana"},
        {"label": "🍇 葡萄", "value": "grape"},
    ],
    default="banana",
    key="fruit"
)
st.write("当前选中：", choice)