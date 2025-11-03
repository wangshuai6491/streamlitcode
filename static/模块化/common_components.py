import streamlit as st
from typing import List, Union, Dict, Any
import uuid

def button_group(
    label: str = "",
    options: List[Dict[str, Union[str, bool]]] = None,
    default_value: Union[str, bool] = None,
    key: str = None
) -> Union[str, bool]:
    """
    创建一个选择按钮组
    
    Args:
        label: 组件标签
        options: 选项列表，每个选项包含 label 和 value
        default_value: 默认选中的值
        key: 组件的唯一键
    
    Returns:
        当前选中的值
    """
    if options is None:
        options = [
            {"label": "是", "value": "是"},
            {"label": "否", "value": "否"}
        ]
    
    if default_value is None:
        default_value = options[0]["value"]
    
    # 生成唯一键
    if key is None:
        key = f"button_group_{label}_{uuid.uuid4().hex[:8]}"
    
    # 初始化 session state
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    # 显示标签
    if label:
        st.write(label)
    
    current_value = st.session_state[key]

    cols = st.columns(len(options))
    
    for i, option in enumerate(options):
        with cols[i]:
            is_selected = current_value == option["value"]
            
            # 创建按钮
            if st.button(
                option["label"],
                key=f"{key}_{i}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state[key] = option["value"]
                st.rerun()
    
    return st.session_state[key]

# 使用示例
def main():
    st.title("Streamlit 按钮组示例")
    
    # 示例1: 默认按钮组（表单外部）
    st.subheader("1. 默认按钮组（表单外部）")
    selected1 = button_group("请选择:", key="default_group")
    st.write(f"当前选择: {selected1}")

    # 示例2: 自定义选项
    st.subheader("2. 自定义选项")
    custom_options = [
        {"label": "选项A", "value": "A"},
        {"label": "选项B", "value": "B"},
        {"label": "选项C", "value": "C"}
    ]
    selected2 = button_group("请选择一个选项:", custom_options, "B", key="custom_group")
    st.write(f"当前选择: {selected2}")
    # 示例4: 多个按钮组
    st.subheader("4. 多个按钮组")
    col1, col2 = st.columns(2)
    
    with col1:
        choice1 = button_group("选择1:", [
            {"label": "上", "value": "up"}, 
            {"label": "下", "value": "down"}
        ], key="group1")
    
    with col2:
        choice2 = button_group("选择2:", [
            {"label": "左", "value": "left"}, 
            {"label": "右", "value": "right"}
        ], key="group2")
    
    st.write(f"选择结果: {choice1} + {choice2}")

if __name__ == "__main__":
    main()