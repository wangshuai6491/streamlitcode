# test_button_group.py
import streamlit as st
from typing import List, Dict, Any, Optional

def button_group(
    label: str,
    options: List[Dict[str, Any]],
    default: Optional[Any] = None,
    key: Optional[str] = None
) -> Any:
    """
    创建一组互斥的按钮，点击后自动高亮当前选中项。
    """
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

    # 动态 CSS
    current_value = st.session_state[key]
    css = ""
    for opt in options:
        btn_key = f"{key}_{opt['value']}"
        is_active = opt["value"] == current_value
        bg_color = "#3b82f6" if is_active else "#ffffff"
        text_color = "#ffffff" if is_active else "#374151"
        border_color = "#3b82f6" if is_active else "#d1d5db"

        css += f"""
        button[data-testid="baseButton-secondary"][data-key="{btn_key}"] {{
            background-color: {bg_color};
            color: {text_color};
            border-color: {border_color};
            transition: all 0.2s ease;
        }}
        button[data-testid="baseButton-secondary"][data-key="{btn_key}"]:hover {{
            background-color: {bg_color}dd;
        }}
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # 创建按钮
    cols = st.columns(len(options))
    for col, opt in zip(cols, options):
        with col:
            if st.button(
                opt["label"],
                key=f"{key}_{opt['value']}",
                use_container_width=True
            ):
                st.session_state[key] = opt["value"]

    return st.session_state[key]

# ------------------ 演示 ------------------
st.set_page_config(page_title="Button Group Demo", layout="centered")
st.title("🔘 Button Group 零刷新测试")

# 1. 单组
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

# 2. 多组并存，验证 key 隔离
st.subheader("第二组按钮（城市）")
city = button_group(
    label="请选择你所在的城市：",
    options=[
        {"label": "北京", "value": "bj"},
        {"label": "上海", "value": "sh"},
        {"label": "广州", "value": "gz"},
        {"label": "深圳", "value": "sz"},
    ],
    default="sh",
    key="city"
)
st.write("当前城市：", city)

# 3. 动态行为示例
if st.button("把水果重置为葡萄"):
    st.session_state["fruit"] = "grape"
    st.rerun()
